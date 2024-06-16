from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CMISetSchema(BaseModel):
    Id: Optional[int] = None
    Nombre: str
    Periodo: datetime
    Descripcion: str
    
    class Config:
        orm_mode = True


class ObjectiveSetSchema(BaseModel):
    Id: Optional[int] = None
    Descripcion: str
    Metrica: str
    Ponderacion: float
    CMI_Id: int
    Perspectiva_Id: int

    class Config:
        orm_mode = True


class PerspectiveSetSchema(BaseModel):
    Id: Optional[int] = None
    Nombre: str

    class Config:
        orm_mode = True


class IndicatorSetSchema(BaseModel):
    Id: Optional[int] = None
    Nombre: str
    Descripcion: str
    Frecuencia_Medida: str
    Unidad_Medida: str
    Objetivo_Id: int
    Tipo_Id: int

    class Config:
        orm_mode = True


class MetricTypeSetSchema(BaseModel):
    Id: Optional[int] = None
    Nombre: str

    class Config:
        orm_mode = True


class DataIndicatorSetSchema(BaseModel):
    Id: Optional[int] = None
    Valor: float
    Fecha: datetime
    Indicador_Id: int

    class Config:
        orm_mode = True


class TargetSetSchema(BaseModel):
    Id: Optional[int] = None
    Descripcion: str
    Valor_esperado: float
    Fecha_limite: datetime
    Indicador_Id: int

    class Config:
        orm_mode = True
