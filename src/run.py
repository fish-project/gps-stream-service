import uvicorn
import argparse
from dotenv import load_dotenv
import os
import threading
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from service.kafka_consumer import consume_and_save


parser = argparse.ArgumentParser()
parser.add_argument("-env", help="Chỉ định file .env để load", type=str)
parser.add_argument("--proto", action="store_true", help="biên dịch proto", required=False)
args = parser.parse_args()

env = ["kafka_host", "server_port", "grpc_host"]

def env_load():
    for item in env:
        os.getenv(item)
        if os.getenv(item) is None:
            raise Exception(f"missing .env configuration: {item}")
        print(f"Đã nạp biến môi trường: {item}={os.getenv(item)}")



def start_consumer():
    from service.kafka_consumer import consume_and_save
    thread = threading.Thread(target=consume_and_save, daemon=True)
    thread.start()


if __name__ == "__main__":
    try:
        if args.env:
            dotenv_path = args.env
            load_dotenv(dotenv_path)
            print(f"Loaded environment from {dotenv_path}")
        else:
            print("Using existing environment variables")

        env_load()
        #  # Start Kafka Consumer thread
        start_consumer()

        if args.proto:
            from .service.gen_proto import compile_proto
            compile_proto()
        else:
            from src.dependency.dependencyLoader import *

            uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("server_port")))
    except Exception as e:
        print(f"fail to start program, msg: {str(e)}")
