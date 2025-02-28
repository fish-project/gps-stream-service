from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..controller.user_controller import stream_data
import json
from fastapi.responses import StreamingResponse
from kafka import KafkaConsumer
from ..service.kafka import kafka_event_stream

router = APIRouter()

@router.websocket("/stream/{ship_id}")
async def get_user(websocket: WebSocket, ship_id:str):
    await stream_data(websocket, ship_id)

@router.get("/stream/{ship_id}")
def stream_kafka_data(ship_id: str):
    return StreamingResponse(kafka_event_stream(ship_id), media_type="text/event-stream")