from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DimensionFechaSchema(BaseModel):
    PedidFecha_id: Optional[int] = None
    Fecha: datetime
    Dia: str = int
    Nombre_dia: str = 'Unknown'
    Num_mes: int
    Nombre_mes: str = 'Unknown'
    Anio: int
    Temporada: str = 'Unknown'
    Festividad: str = 'Unknown'
    Periodo: str = 'Unknown'

    class Config:
        orm_mode = True


class DimensionClientesSchema(BaseModel):
    Cliente_id: Optional[int] = None
    Nombre: str = 'Unknown'
    Apellidos: str = 'Unknown'
    Nacionalidad: str = 'Unknown'
    Tipo_Cliente: str = 'Unknown'
    Metodo_Reserva: str = 'Unknown'

    class Config:
        orm_mode = True


class DimensionPaqueteSchema(BaseModel):
    Paquetes_ID: Optional[int] = None
    Nombre_Paquetes: str = 'Unknown'
    Descripcion_Paquete: str = 'Unknown'

    class Config:
        orm_mode = True


class DimensionHabitacionesSchema(BaseModel):
    Habitaciones_ID: Optional[int] = None
    Tipo_Habitacion: str = 'Unknown'
    Capacidad: int
    Disponibilidad: str = 'Unknown'

    class Config:
        orm_mode = True


class DimensionIntermediariosSchema(BaseModel):
    Intermediario_ID: Optional[int] = None
    Nombre_Intermediario: str = 'Unknown'
    Tipo_Intermediario: str = 'Unknown'

    class Config:
        orm_mode = True


class FactTableReservacionesSchema(BaseModel):
    EnviosID: Optional[int] = None
    Reservaciones_ID: int
    Clientes_ID: int
    Paquetes_ID: int
    Habitaciones_ID: int
    Intermediarios_ID: int
    Fecha_Reservaciones: datetime
    Fecha_check_in: datetime
    Fecha_check_out: datetime
    Precio_Noche: float
    Precio_Paquete: float
    Dias_ocupacion: int
    Metodo_Pago : str
    ValidFrom: datetime
    ValidTo: datetime

    class Config:
        orm_mode = True
