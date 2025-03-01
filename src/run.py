import uvicorn
import argparse
from dotenv import load_dotenv
import os

parser = argparse.ArgumentParser()
parser.add_argument("-env", help="Chỉ định file .env để load", type=str)
args = parser.parse_args()

if __name__ == "__main__":
    try:
        if args.env:
            dotenv_path = args.env
            load_dotenv(dotenv_path)
            print(f"Loaded environment from {dotenv_path}")
        else:
            print("Using existing environment variables")

        kafka_host = os.getenv("kafka_host")
        server_port = os.getenv("server_port")
        
        if(kafka_host is None or server_port is None):
            raise Exception("missing .env configuration")
        
        print(f"kafka host: {kafka_host}")
        print(f"server port: {server_port}\n")

        from src.dependency.dependencyLoader import *

        uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("server_port")))
    except Exception as e:
        print(f"fail to start program, msg: {str(e)}")
