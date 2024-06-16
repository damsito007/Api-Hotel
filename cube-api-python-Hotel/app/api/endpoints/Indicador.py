from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from app.database import get_db_dw
from fastapi.responses import JSONResponse
from ...models.data_warehouse_models import FactTableReservaciones

router = APIRouter()

def calculate_growth(current_value, previous_value):
    if previous_value == 0:
        return float('inf') if current_value > 0 else 0
    return ((current_value - previous_value) / previous_value) * 100

def get_quarter(date):
    return (date.month - 1) // 3 + 1

def get_quarter_start_end(year, quarter):
    if quarter == 1:
        return datetime(year, 1, 1), datetime(year, 3, 31, 23, 59, 59)
    elif quarter == 2:
        return datetime(year, 4, 1), datetime(year, 6, 30, 23, 59, 59)
    elif quarter == 3:
        return datetime(year, 7, 1), datetime(year, 9, 30, 23, 59, 59)
    elif quarter == 4:
        return datetime(year, 10, 1), datetime(year, 12, 31, 23, 59, 59)

def queryGrowthData(db: Session, year: int, growth_threshold: float):
    data = []

    for quarter in range(1, 5):
        current_start, current_end = get_quarter_start_end(year, quarter)
        previous_start, previous_end = get_quarter_start_end(year - 1, quarter)

        # Current period
        current_period = db.query(
            func.count(FactTableReservaciones.Reservaciones_ID).label('num_reservations'),
            func.sum(FactTableReservaciones.Precio_Paquete).label('total_income')
        ).filter(FactTableReservaciones.Fecha_check_in.between(current_start, current_end)).first()

        # Previous period
        previous_period = db.query(
            func.count(FactTableReservaciones.Reservaciones_ID).label('num_reservations'),
            func.sum(FactTableReservaciones.Precio_Paquete).label('total_income')
        ).filter(FactTableReservaciones.Fecha_check_in.between(previous_start, previous_end)).first()

        # Calculate growth
        num_reservations_growth = calculate_growth(current_period.num_reservations, previous_period.num_reservations)
        total_income_growth = calculate_growth(current_period.total_income, previous_period.total_income)

        # Check against threshold
        quarter_data = {
            'quarter': f'Q{quarter} {year}',
            'num_reservations_growth': num_reservations_growth,
            'num_reservations_meets_threshold': num_reservations_growth >= growth_threshold,
            'total_income_growth': total_income_growth,
            'total_income_meets_threshold': total_income_growth >= growth_threshold
        }

        data.append(quarter_data)

    return data

@router.get("/growth-indicator")
async def get_growth_indicator(
    db: Session = Depends(get_db_dw),
    year: int = Query(..., description="Year to analyze"),
    growth_threshold: float = Query(5.0, description="Growth threshold percentage")
):
    data = queryGrowthData(db, year, growth_threshold)
    return JSONResponse(content=data)
