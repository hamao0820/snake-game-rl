from websockets.sync.client import connect
from time import sleep
import json

url = "ws://localhost:8080"

with connect(url) as ws:
    ws.recv()
    while True:
        sleep(0.3)
        ws.send("0")
        data = json.loads(ws.recv())
        print(data["done"])
        if (data["done"]):
            break
