import uvicorn

if __name__ == "__main__":
    from src.dependency.dependencyLoader import *

    uvicorn.run(app, host="0.0.0.0", port=config['server_port'])
