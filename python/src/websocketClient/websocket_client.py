from websockets.sync.client import connect
from time import sleep
import json

# import PIL.Image as Image
# import io

url = "ws://localhost:8080"

with connect(url) as ws:
    ws.recv()
    i = 0
    while True:
        sleep(0.3)
        ws.send("0")
        data = json.loads(ws.recv())
        # img = Image.open(io.BytesIO(bytes(data["img"]["data"])))
        # img.save(f"./img/{i}.png")
        # i += 1
        # print(data["done"], data["score"])
        if data["done"]:
            break
