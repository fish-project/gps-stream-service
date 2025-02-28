from fastapi import WebSocket, WebSocketDisconnect
import json
from fastapi.websockets import WebSocketState
import time
import json
from kafka import KafkaProducer, KafkaConsumer
import time
from src.dependency.dependencyLoader import config

async def stream_data(websocket: WebSocket, ship_id:str):
    await websocket.accept()
    await websocket.send_text(f"Gửi dữ liệu từ client {ship_id}")
    timestamp = int(time.time() * 1000)

    producer = KafkaProducer(
        bootstrap_servers=config['kafka_host'],
        key_serializer=lambda k: str(k).encode("utf-8"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    try:
        while True:
            data = await websocket.receive_text()
            try:
                producer.send(ship_id, data, key=timestamp)
                await websocket.send_json({
                    "sent": data,
                    "state": "success"
                })
            except Exception as e:
                await websocket.send_json({
                    "sent": str(e),
                    "state": "fail"
                })
                
    except WebSocketDisconnect:
        print("⚠️ Client đã ngắt kết nối")
    except Exception as e:
        print(str(e))
    finally:
        # producer.flush() 
        # producer.close() 
        try:
            await websocket.close()
        except RuntimeError as e:
            print(f"⚠️ WebSocket đã đóng hoặc không thể đóng lại: {e}")