import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.database import get_db_dw
from fastapi.responses import JSONResponse
from ...models.data_warehouse_models import (
    FactTableReservaciones, DimensionClientes, DimensionPaquete, DimensionHabitaciones, DimensionIntermediarios, DimensionFecha
)

router = APIRouter()

def queryDashboardData(db: Session):
    data = {}

    # Número de habitaciones
    num_habitaciones = db.query(DimensionHabitaciones).count()
    data['num_habitaciones'] = num_habitaciones

    # Número de clientes
    num_clientes = db.query(DimensionClientes).count()
    data['num_clientes'] = num_clientes

    # Número de intermediarios
    num_intermediarios = db.query(DimensionIntermediarios).count()
    data['num_intermediarios'] = num_intermediarios

    # Número de paquetes
    num_paquetes = db.query(DimensionPaquete).count()
    data['num_paquetes'] = num_paquetes

    # Paquete más solicitado
    paquete_mas_solicitado = db.query(
        DimensionPaquete.Nombre_Paquetes, 
        db.func.count(FactTableReservaciones.Paquetes_ID).label('cantidad')
    ).join(FactTableReservaciones, DimensionPaquete.Paquetes_ID == FactTableReservaciones.Paquetes_ID)\
    .group_by(DimensionPaquete.Nombre_Paquetes)\
    .order_by(db.desc('cantidad')).first()
    
    data['paquete_mas_solicitado'] = {
        'nombre': paquete_mas_solicitado.Nombre_Paquetes,
        'cantidad': paquete_mas_solicitado.cantidad
    }

    # Cantidad de clientes por método de pago
    clientes_por_metodo_pago = db.query(
        FactTableReservaciones.Metodo_Pago, 
        db.func.count(FactTableReservaciones.Clientes_ID).label('cantidad')
    ).group_by(FactTableReservaciones.Metodo_Pago)\
    .all()

    data['clientes_por_metodo_pago'] = [
        {'metodo_pago': item.Metodo_Pago, 'cantidad': item.cantidad}
        for item in clientes_por_metodo_pago
    ]

    return data

@router.get("/dashboard-general")
async def get_dashboard_general(db: Session = Depends(get_db_dw)):
    data = queryDashboardData(db)

    # Diagrama de barras para el paquete más solicitado
    paquetes = [data['paquete_mas_solicitado']['nombre']]
    cantidades_paquetes = [data['paquete_mas_solicitado']['cantidad']]

    # Diagrama de barras para clientes por método de pago
    metodos_pago = [item['metodo_pago'] for item in data['clientes_por_metodo_pago']]
    cantidades_metodos_pago = [item['cantidad'] for item in data['clientes_por_metodo_pago']]

    return JSONResponse(content={
        'num_habitaciones': data['num_habitaciones'],
        'num_clientes': data['num_clientes'],
        'num_intermediarios': data['num_intermediarios'],
        'num_paquetes': data['num_paquetes'],
        'paquete_mas_solicitado': {
            'nombre': paquetes,
            'cantidad': cantidades_paquetes
        },
        'clientes_por_metodo_pago': {
            'metodo_pago': metodos_pago,
            'cantidad': cantidades_metodos_pago
        }
    })

# Distribución de clientes por nacionalidad
@router.get("/clientes-por-nacionalidad")
async def get_clientes_por_nacionalidad(db: Session = Depends(get_db_dw)):
    result = db.query(
        DimensionClientes.Nacionalidad,
        db.func.count(DimensionClientes.Clientes_id).label('cantidad')
    ).group_by(DimensionClientes.Nacionalidad).all()

    data = [{'nacionalidad': item.Nacionalidad, 'cantidad': item.cantidad} for item in result]

    return JSONResponse(content=data)

# Distribución de habitaciones por capacidad
@router.get("/habitaciones-por-capacidad")
async def get_habitaciones_por_capacidad(db: Session = Depends(get_db_dw)):
    result = db.query(
        DimensionHabitaciones.Capacidad,
        db.func.count(DimensionHabitaciones.Habitaciones_ID).label('cantidad')
    ).group_by(DimensionHabitaciones.Capacidad).all()

    data = [{'capacidad': item.Capacidad, 'cantidad': item.cantidad} for item in result]

    return JSONResponse(content=data)

# Precio promedio por noche por tipo de habitación
@router.get("/precio-promedio-por-tipo-habitacion")
async def get_precio_promedio_por_tipo_habitacion(db: Session = Depends(get_db_dw)):
    result = db.query(
        DimensionHabitaciones.Tipo_Habitacion,
        db.func.avg(FactTableReservaciones.Precio_Noche).label('precio_promedio')
    ).join(FactTableReservaciones, DimensionHabitaciones.Habitaciones_ID == FactTableReservaciones.Habitaciones_ID)\
    .group_by(DimensionHabitaciones.Tipo_Habitacion).all()

    data = [{'tipo_habitacion': item.Tipo_Habitacion, 'precio_promedio': float(item.precio_promedio)} for item in result]

    return JSONResponse(content=data)

# Número de reservas por intermediario
@router.get("/reservas-por-intermediario")
async def get_reservas_por_intermediario(db: Session = Depends(get_db_dw)):
    result = db.query(
        DimensionIntermediarios.Nombre_Intermediario,
        db.func.count(FactTableReservaciones.Reservaciones_ID).label('cantidad')
    ).join(FactTableReservaciones, DimensionIntermediarios.Intermediario_ID == FactTableReservaciones.Intermediarios_ID)\
    .group_by(DimensionIntermediarios.Nombre_Intermediario).all()

    data = [{'intermediario': item.Nombre_Intermediario, 'cantidad': item.cantidad} for item in result]

    return JSONResponse(content=data)

# Ingresos totales por paquete
@router.get("/ingresos-por-paquete")
async def get_ingresos_por_paquete(db: Session = Depends(get_db_dw)):
    result = db.query(
        DimensionPaquete.Nombre_Paquetes,
        db.func.sum(FactTableReservaciones.Precio_Paquete).label('ingresos_totales')
    ).join(FactTableReservaciones, DimensionPaquete.Paquetes_ID == FactTableReservaciones.Paquetes_ID)\
    .group_by(DimensionPaquete.Nombre_Paquetes).all()

    data = [{'paquete': item.Nombre_Paquetes, 'ingresos_totales': float(item.ingresos_totales)} for item in result]

    return JSONResponse(content=data)
