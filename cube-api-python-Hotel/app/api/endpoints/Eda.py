import pandas as pd
import numpy as np
from scipy import stats
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response
from app.database import get_db_dw
from fastapi.responses import JSONResponse
from io import BytesIO
from ...models.data_warehouse_models import (
    FactTableReservaciones, DimensionClientes, DimensionPaquete, DimensionHabitaciones, DimensionIntermediarios, DimensionFecha
)

router = APIRouter()

def queryData(db: Session):
    return db.query(
        FactTableReservaciones.Reservaciones_ID.label('Reservaciones ID'),
        (DimensionClientes.Nombre + " " + DimensionClientes.Apellidos).label('Full Name'),
        DimensionClientes.Nacionalidad.label('Nacionalidad'),
        DimensionClientes.Tipo_Cliente.label('Tipo Cliente'),
        DimensionClientes.Metodo_Reserva.label('Metodo Reserva'),
        DimensionPaquete.Nombre_Paquetes.label('Nombre Paquete'),
        DimensionPaquete.Descripcion_Paquete.label('Descripcion Paquete'),
        DimensionHabitaciones.Tipo_Habitacion.label('Tipo Habitacion'),
        DimensionHabitaciones.Capacidad,
        DimensionIntermediarios.Nombre_Intermediario.label('Nombre Intermediario'),
        FactTableReservaciones.Fecha_Reservacion_ID.label('Fecha Reservacion'),
        FactTableReservaciones.Fecha_check_in.label('Fecha Check In'),
        FactTableReservaciones.Fecha_check_out.label('Fecha Check Out'),
        FactTableReservaciones.Precio_Noche.label('Precio Noche'),
        FactTableReservaciones.Precio_Paquete.label('Precio Paquete'),
        FactTableReservaciones.Dias_ocupacion.label('Dias Ocupacion'),
        FactTableReservaciones.Metodo_Pago.label('Metodo Pago'),
        FactTableReservaciones.ValidFrom.label('Valid From'),
        FactTableReservaciones.ValidTo.label('Valid To')
    ).join(DimensionClientes, FactTableReservaciones.Clientes_ID == DimensionClientes.Clientes_id) \
     .join(DimensionPaquete, FactTableReservaciones.Paquetes_ID == DimensionPaquete.Paquetes_ID) \
     .join(DimensionHabitaciones, FactTableReservaciones.Habitaciones_ID == DimensionHabitaciones.Habitaciones_ID) \
     .join(DimensionIntermediarios, FactTableReservaciones.Intermediarios_ID == DimensionIntermediarios.Intermediario_ID).all()

def createDataframe(result):
    df = pd.DataFrame(result).set_index("Reservaciones ID")
    df['Precio Noche'] = pd.to_numeric(df['Precio Noche'], errors='coerce')
    df['Precio Paquete'] = pd.to_numeric(df['Precio Paquete'], errors='coerce')
    df['Dias Ocupacion'] = pd.to_numeric(df['Dias Ocupacion'], errors='coerce')

    df['Tipo Habitacion'] = df['Tipo Habitacion'].astype('category')
    df['Metodo Pago'] = df['Metodo Pago'].astype('category')
    df['Nombre Paquete'] = df['Nombre Paquete'].astype('category')

    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    return df

def getDataFrame(db: Session):
    result = queryData(db)
    return createDataframe(result)

@router.get("/df/test-schema")
def dfTest(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    print(df.dtypes)
    return {"message": "Test result printed in the terminal"}

@router.get("/df", response_model=list)
def ViewDf(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    return df.to_dict(orient='records')

@router.get("/histograma-precio-noche")
async def get_histograma_precio_noche(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    data = df['Precio Noche'].to_list()
    return JSONResponse(content=data)

@router.get("/box-plot")
async def get_boxplot(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)

    columns = ['Precio Noche', 'Precio Paquete', 'Dias Ocupacion']
    data = {}

    for column in columns:
        if column in df:
            values = df[column]

            min_val = np.min(values).item()
            q1 = np.percentile(values, 25).item()
            median = np.percentile(values, 50).item()
            q3 = np.percentile(values, 75).item()
            max_val = np.max(values).item()
            mean_val = np.mean(values).item()

            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = values[(values < lower_bound) |
                              (values > upper_bound)].tolist()

            data[column] = {
                "boxplot": [min_val, q1, median, q3, max_val],
                "mean": mean_val,
                "outliers": [[0, outlier] for outlier in outliers]
            }

    return JSONResponse(content=data)

@router.get("/scatter-precio-paquete")
async def get_scatter_precio_paquete(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)

    precio_paquete = df['Precio Paquete'].to_list()
    data = [[i, val] for i, val in enumerate(precio_paquete)]
    return JSONResponse(content=data)

@router.get("/heat-map")
async def get_heat_map(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    heatmap_data = df[['Precio Noche', 'Precio Paquete', 'Dias Ocupacion']]

    correlation_matrix = heatmap_data.corr()
    heatmapJson = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(len(correlation_matrix.columns)):
            heatmapJson.append([i, j, correlation_matrix.iat[i, j]])

    return JSONResponse(content={
        "xAxisCategories": correlation_matrix.columns.tolist(),
        "yAxisCategories": correlation_matrix.index.tolist(),
        "heatmapData": heatmapJson
    })

@router.get("/correlation")
async def get_correlation(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    contingency_table = pd.crosstab(df['Tipo Habitacion'], df['Metodo Pago'])
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

    heatmapJson = []
    for i in range(len(contingency_table.index)):
        for j in range(len(contingency_table.columns)):
            heatmapJson.append(
                [int(i), int(j), int(contingency_table.iat[i, j])])

    return JSONResponse(content={
        "xAxisCategories": contingency_table.columns.astype(str).tolist(),
        "yAxisCategories": contingency_table.index.astype(str).tolist(),
        "heatmapData": heatmapJson
    })

@router.get("/summary-statistics")
async def get_summary_statistics(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    summary = df.describe().to_dict()
    return JSONResponse(content=summary)
