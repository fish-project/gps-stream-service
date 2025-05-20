from fastapi import APIRouter, HTTPException
import psycopg2
from typing import List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class KafkaData(BaseModel):
    id: int
    ship_id: str
    data: dict
    timestamp: str  # Trả về string thay vì int để chuyển sang dạng thời gian

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="gps",
        user="admin",
        password="root"
    )

@router.get("/data/{ship_id}", response_model=List[KafkaData])
def get_data_by_ship_id(ship_id: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, ship_id, data, timestamp
            FROM kafka_data
            WHERE ship_id = %s
            ORDER BY timestamp DESC
        """, (ship_id,))
        
        rows = cursor.fetchall()
        result = [
            KafkaData(
                id=row[0],
                ship_id=row[1],
                data=row[2],
                timestamp=datetime.fromtimestamp(row[3] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            )
            for row in rows
        ]

        cursor.close()
        conn.close()
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ShipIdResponse(BaseModel):
    ship_id: str

@router.get("/ships", response_model=List[ShipIdResponse])
def get_all_ship_ids():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT ship_id
            FROM kafka_data
            ORDER BY ship_id
        """)
        
        rows = cursor.fetchall()
        ship_ids = [{"ship_id": row[0]} for row in rows]

        cursor.close()
        conn.close()
        return ship_ids

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))