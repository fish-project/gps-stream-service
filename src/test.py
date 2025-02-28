import websocket
import json
import time
import random

# Định nghĩa WebSocket URL
ws_url = "ws://127.0.0.1:8000/stream/ship_test_gps"

def on_open(ws):
    print("Connected to WebSocket server")

    def send_data():
        while True:
            data = {
                "latitude": round(random.uniform(-90, 90), 6),
                "longitude": round(random.uniform(-180, 180), 6)
            }
            ws.send(json.dumps(data))
            print("Sent:", data)
            time.sleep(2)  # Gửi mỗi 2 giây

    send_data()

def on_message(ws, message):
    print("Received:", message)

def on_error(ws, error):
    print("WebSocket error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Disconnected from WebSocket server")

if __name__ == "__main__":
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close
                                )
    ws.run_forever()
