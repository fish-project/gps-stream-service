import json
import psycopg2
from kafka import KafkaConsumer
import os
import time

def consume_and_save():
    consumer = KafkaConsumer(
        '68207f1327928b148d3d7ac9',  
        bootstrap_servers=os.getenv("kafka_host", "localhost:9092"),
        auto_offset_reset="latest",
        group_id="fastapi-consumer-group"
    )

    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="gps",
        user="admin",
        password="root"
    )
    cursor = conn.cursor()

    for message in consumer:
        try:
            # Parse JSON bị escape 2 lần
            raw_str = message.value.decode("utf-8") if isinstance(message.value, bytes) else message.value
            json_str = json.loads(raw_str)   # lần 1: chuỗi JSON bị escape
            data = json.loads(json_str)      # lần 2: thành dict

            ship_id = str(message.key.decode() if message.key else "unknown")
            timestamp = int(time.time() * 1000)

            cursor.execute("""
                INSERT INTO kafka_data (ship_id, data, timestamp)
                VALUES (%s, %s, %s)
            """, (ship_id, json.dumps(data), timestamp))

            conn.commit()
            print("✅ Lưu thành công:", data)

        except Exception as e:
            print("❌ Lỗi lưu:", e)
