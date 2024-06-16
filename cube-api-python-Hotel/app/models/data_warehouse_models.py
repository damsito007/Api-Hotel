from sqlalchemy import Column, Integer, String, Float, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Por ver el día de manaña
class DimensionFecha(Base):
    __tablename__ = 'Dim_Fecha'
    Fecha_id = Column(Integer, primary_key=True, autoincrement=True)
    Fecha = Column(DateTime, default='Unknown')
    Dia = Column(Integer, default='Unknown')
    Nombre_dia = Column(String(100), nullable=False)
    Num_mes = Column(Integer, nullable=False)
    Nombre_mes = Column(String(100), default='Unknown')
    Anio = Column(Integer, default='Unknown')
    Temporada = Column(String(100), nullable=False)
    Festividad = Column(String(100), nullable=False)
    Periodo = Column(String(100), nullable=False)

class DimensionClientes(Base):
    __tablename__ = 'Dim_Clientes'
    Clientes_id = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100), default='Unknown')
    Apellidos = Column(String(100), default='Unknown')
    Nacionalidad = Column(String(100), default='Unknown')
    Tipo_Cliente = Column(String(100), default='Unknown')
    Metodo_Reserva = Column(String(100), default='Unknown')

class DimensionPaquete(Base):
    __tablename__ = 'Dim_Paquetes'
    Paquetes_ID = Column(Integer, primary_key=True, autoincrement=True)
    Nombre_Paquetes = Column(String(100), default='Unknown')
    Descripcion_Paquete = Column(String(100), default='Unknown')


class DimensionHabitaciones(Base):
    __tablename__ = 'Dim_Habitaciones'
    Habitaciones_ID = Column(Integer, primary_key=True, autoincrement=True)
    Tipo_Habitacion = Column(String(100), default='Unknown')
    Capacidad = Column(Integer, nullable=False)
    Disponibilidad = Column(String(100), default='Unknown')

class DimensionIntermediarios(Base):
    __tablename__ = 'Dim_Intermediarios'
    Intermediario_ID = Column(Integer, primary_key=True, autoincrement=True)
    Nombre_Intermediario = Column(String(100), default='Unknown')
    Tipo_Intermediario = Column(String(100), default='Unknown')

#Futura actualización por la dimensión fecha que esta pendiente a revisión
class FactTableReservaciones(Base):
    __tablename__ = 'FactTable_ActividadesHotel'
    Reservaciones_ID = Column(Integer, primary_key=True, autoincrement=True)
    Clientes_ID = Column(Integer, ForeignKey('Dim_Clientes.Cliente_id'))
    Paquetes_ID = Column(Integer, ForeignKey('Dim_Paquetes.Paquetes_ID'))
    Habitaciones_ID = Column(Integer, ForeignKey('Dim_Habitaciones.Habitaciones_ID'))
    Intermediarios_ID = Column(Integer, ForeignKey('Dim_Intermediarios.Intermediario_ID'))
    Fecha_Reservacion_ID = Column(DateTime)
    Fecha_check_in = Column(DateTime)
    Fecha_check_out = Column(DateTime)
    Precio_Noche = Column(DECIMAL)
    Precio_Paquete = Column(DECIMAL)
    Dias_ocupacion = Column(Integer)
    Metodo_Pago = Column(String(100), default='Unknown')
    ValidFrom = Column(DateTime)
    ValidTo = Column(DateTime)
