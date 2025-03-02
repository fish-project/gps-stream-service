import os
import subprocess

def compile_proto():
    proto_file = "resources/proto/main.proto"
    output="resources/proto"

    if not os.path.exists(proto_file):
        raise FileNotFoundError(f"❌ Không tìm thấy file: {proto_file}")

    output_dir = os.path.dirname(proto_file) 
    command = [
        "python", "-m", "grpc_tools.protoc",
        f"-I.", 
        f"--python_out=.",
        f"--grpc_python_out=.",
        proto_file
    ]

    print(f"🔄 Đang biên dịch: {proto_file} ...")
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Biên dịch thành công!")
    else:
        print("❌ Lỗi khi biên dịch:", result.stderr)
