from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db_dw
from ...models.data_warehouse_models import DimensionClientes
from ...schemas.data_warehouse_schemas import DimensionClientesSchema

router = APIRouter()

#Cambiar mañana este endpoint

@router.get("/", response_model=list[DimensionClientesSchema])
def read_dimension_Clientes(db: Session = Depends(get_db_dw)):
    clientes = db.query(DimensionClientes).all()
    return clientes


@router.get("/{clienteld}", response_model=DimensionClientesSchema)
def read_dimension_Clientes(clienteld: int, db: Session = Depends(get_db_dw)):
    cliente = db.query(DimensionClientes).filter(
        DimensionClientes.Clientes_id == clienteld).first()
    if not cliente:
        raise HTTPException(
            status_code=404, detail="DimensionCliente not found")
    return cliente


@router.post("/", response_model=DimensionClientesSchema)
def create_dimension_cliente(cliente: DimensionClientesSchema, db: Session = Depends(get_db_dw)):
    new_cliente = DimensionClientesSchema(**cliente.dict())
    db.add(new_cliente)
    db.commit()
    db.refresh(new_cliente)
    return new_cliente


@router.put("/{clienteld}", response_model=DimensionClientesSchema)
def update_dimension_cliente(clienteld: int, cliente: DimensionClientesSchema, db: Session = Depends(get_db_dw)):
    db_cliente= db.query(DimensionClientes).filter(
        DimensionClientes.Clientes_id == clienteld).first()
    if not db_cliente:
        raise HTTPException(
            status_code=404, detail="DimensionCliente not found")
    for var, value in cliente.dict().items():
        setattr(db_cliente, var, value)
    db.commit()
    return db_cliente


@router.delete("/{clienteld}", status_code=204)
def delete_dimension_cliente(clienteld: int, db: Session = Depends(get_db_dw)):
    db_cliente = db.query(DimensionClientes).filter(
        DimensionClientes.Clientes_id == clienteld).first()
    if not db_cliente:
        raise HTTPException(
            status_code=404, detail="DimensionCliente not found")
    db.delete(db_cliente)
    db.commit()
    return {"ok": True}
