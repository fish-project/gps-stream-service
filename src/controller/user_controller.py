from fastapi import WebSocket, WebSocketDisconnect
import json
from fastapi.websockets import WebSocketState
import time
import json
from kafka import KafkaProducer, KafkaConsumer
import time
import os

async def stream_data(websocket: WebSocket, ship_id:str, email:str):
    from resources.proto.grpc_client import run
    # if not run(email, ship_id):
    #     print("Từ chối kết nối")
    #     await websocket.close()
    #     return

    await websocket.accept()
    await websocket.send_text(f"Gửi dữ liệu từ client {ship_id}")
    timestamp = int(time.time() * 1000)

    producer = KafkaProducer(
        bootstrap_servers=os.getenv("kafka_host"),
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
        # TODO
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