from contextlib import closing
import json
from kafka import KafkaProducer, KafkaConsumer
import time
import os

def kafka_event_stream(ship_id: str):
    with closing(KafkaConsumer(
        ship_id,
        bootstrap_servers=os.getenv("kafka_host"),
        auto_offset_reset="latest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )) as consumer:
        try:
            for message in consumer:
                data = json.dumps(message.value)
                yield f"data: {data}\n\n"
        except Exception as e:
            print(f"❌ Lỗi Kafka: {e}")
            yield f"data: {json.dumps({'error': 'Kafka consumer error'})}\n\n"