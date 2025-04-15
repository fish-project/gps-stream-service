from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from ..controller.user_controller import stream_data
import json
from fastapi.responses import StreamingResponse
from kafka import KafkaConsumer
from ..service.kafka import kafka_event_stream

router = APIRouter()

@router.websocket("/stream/{ship_id}/{email}")
async def get_user(websocket: WebSocket, ship_id:str, email:str):
    print(email)
    print(ship_id)
    
    await stream_data(websocket, ship_id, email)

@router.get("/stream/{ship_id}/{email}")
def stream_kafka_data(ship_id: str, email:str):
    from resources.proto.grpc_client import run
    if not run(email, ship_id):
        raise HTTPException(status_code=403, detail="Từ chối kết nối")
        return
    return StreamingResponse(kafka_event_stream(ship_id), media_type="text/event-stream")