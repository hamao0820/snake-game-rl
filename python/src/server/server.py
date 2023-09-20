from websockets.sync.client import connect
from time import sleep

url = "ws://localhost:8080"

with connect(url) as ws:
    while True:
        sleep(0.5)
        ws.send("0")
        message = ws.recv()
        print(f"Received: {str(message)}")
