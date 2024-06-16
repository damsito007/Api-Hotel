from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class CMISet(Base):
    __tablename__ = 'CMI'
    Id = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String, nullable=False)
    Periodo = Column(DateTime, nullable=False)
    Descripcion = Column(String, nullable=False)
    # definir relaciones ()
    Objetivo = relationship("Objetivo", back_populates="cmi")


class ObjectiveSet(Base):
    __tablename__ = 'Objetivo'
    Id = Column(Integer, primary_key=True, index=True)
    Descripcion = Column(String, nullable=False)
    Metrica = Column(String, nullable=False)
    Ponderacion = Column(DECIMAL, nullable=False)
    CMI_Id = Column(Integer, ForeignKey('CMI.Id'), nullable=False)
    Perspectiva_Id = Column(Integer, ForeignKey('Perspectiva.Id'), nullable=False)

    cmi = relationship("CMI", back_populates="objetivos")
    perspectiva = relationship("Perspectiva", back_populates="objetivos")
    indicador = relationship("Indicador", back_populates="objetivo")


class PerspectiveSet(Base):
    __tablename__ = 'Perspectiva'
    Id = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String, nullable=False)

    objetivos = relationship("Objectivo", back_populates="perspectiva")


class IndicatorSet(Base):
    __tablename__ = 'Indicador'
    Id = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String, nullable=False)
    Descripcion = Column(String, nullable=False)
    Frecuencia_Medida = Column(String, nullable=False)
    Unidad_Medida = Column(String, nullable=False)
    Objetivo_Id = Column(Integer, ForeignKey('Objetivo.Id'), nullable=False)
    Tipo_Id = Column(Integer, ForeignKey('Tipo.Id'), nullable=False)

    objective = relationship("Objetivo", back_populates="indicadores")
    metric_type = relationship("Tipo", back_populates="indicadores")
    data_indicators = relationship("Indicador_Dato", back_populates="indicador")
    targets = relationship("Meta", back_populates="indicador")


class MetricTypeSet(Base):
    __tablename__ = 'Tipo'
    Id = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String, nullable=False)

    indicadores = relationship("Indicador", back_populates="tipo")


class DataIndicatorSet(Base):
    __tablename__ = 'Indicador_Dato'
    Id = Column(Integer, primary_key=True, index=True)
    Valor = Column(DECIMAL, nullable=False)
    Fecha = Column(DateTime, nullable=False)
    Indicador_Id = Column(Integer, ForeignKey('Indicador.Id'), nullable=False)

    indicator = relationship("Indicador", back_populates="indicador_datos")


class TargetSet(Base):
    __tablename__ = 'Meta'
    Id = Column(Integer, primary_key=True, index=True)
    Descripcion = Column(String, nullable=False)
    Valor_esperado = Column(DECIMAL, nullable=False)
    Fecha_limite = Column(DateTime, nullable=False)
    Indicador_Id = Column(Integer, ForeignKey('Indicador.Id'), nullable=False)

    indicator = relationship("Indicador", back_populates="metas")
