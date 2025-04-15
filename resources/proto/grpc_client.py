from . import main_pb2, main_pb2_grpc

def run(email:str, shipid:str):
    import grpc
    import os

    try:
        print("------------------------------------------------------------")
        channel = grpc.insecure_channel(os.getenv("grpc_host"))
        stub = main_pb2_grpc.ConfirmEmailStub(channel)

        request = main_pb2.Request(email=email, shipid=shipid)
        response = stub.checkEmail(request)

        print(f"Phản hồi từ server: {response.mess}")
        return response.mess == "success"
    except: return False
