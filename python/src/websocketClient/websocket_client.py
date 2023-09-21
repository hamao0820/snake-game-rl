from websockets import client
import json
# import asyncio

from typing import Union, TypedDict


class ImageMessage(TypedDict):
    type: str
    data: bytes


class Message(TypedDict):
    done: bool
    score: int
    img: ImageMessage


async def f():
    ws = await client.connect("ws://localhost:8080")
    print(await ws.recv()) 

    while True:
        await ws.send("0")
        message = await ws.recv()
        data: Message = json.loads(message)
        if data["done"]:
            break
        print(data["score"])

    await ws.close()
    return


class WebsocketClient:
    def __init__(self) -> None:
        self.__server_address = "ws://localhost:8080"
        self.__ws: Union[client.WebSocketClientProtocol, None] = None
        self.__message: Union[Message, None] = None
        self.__is_closed: bool = False

    async def connect(self) -> None:
        self.__ws = await client.connect(self.__server_address)
        print(await self.__ws.recv())
        print("connected")
        return

    async def send(self, data: Union[str, int]) -> None:
        if self.__ws is None:
            raise Exception("Not connected to server")
        print("sending" + str(data))
        await self.__ws.send(str(data))
        print("sent")
        self.__message = json.loads(await self.__ws.recv())
        print("received")
        return

    async def close(self) -> None:
        if not self.__ws:
            return

        await self.__ws.close()
        return

    @property
    def is_closed(self) -> bool:
        return self.__is_closed

    @property
    def message(self) -> Union[Message, None]:
        return self.__message


# if __name__ == "__main__":
#     ws_client = WebsocketClient()
#     asyncio.get_event_loop().run_until_complete(ws_client.connect())
#     print("connected to server")
#     while True:
#         print("sending message")
#         asyncio.get_event_loop().run_until_complete(ws_client.send(0))
#         message = ws_client.message
#         if message is not None:
#             print(message["img"]["data"])
#             if message["done"]:
#                 break
