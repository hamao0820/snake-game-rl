import asyncio
import json
from typing import List, Literal, Tuple, TypeAlias, TypedDict, Union, cast

from websockets import client


class ImageMessage(TypedDict):
    type: str
    data: bytes


class SendMessage(TypedDict):
    method: str
    data: dict


class Observation(TypedDict):
    type: Literal["Buffer"]
    data: List[int]


class ResetResponse(TypedDict):
    state: Observation
    info: dict


class StepResponse(TypedDict):
    observation: Observation
    reward: float
    terminated: bool
    truncated: bool
    info: dict


# 0:straight, 1:left, 2:right
Action: TypeAlias = Union[Literal[0], Literal[1], Literal[2]]


class WebsocketClient:
    def __init__(self) -> None:
        self.__server_address = "ws://localhost:8080"
        self.__ws: Union[client.WebSocketClientProtocol, None] = None
        self.__is_closed: bool = False
        asyncio.set_event_loop(asyncio.new_event_loop())

    def connect(self) -> None:
        async def async_connect():
            self.__ws = await client.connect(self.__server_address)
            print(await self.__ws.recv())
            print("connected")
            return

        return asyncio.get_event_loop().run_until_complete(async_connect())

    def send(self, data: Union[str, int]):
        if self.__ws is None:
            raise Exception("Not connected to server")

        async def async_send():
            await self.__ws.send(str(data))
            return json.loads(await self.__ws.recv())

        return asyncio.get_event_loop().run_until_complete(async_send())

    def reset(self) -> Tuple[Observation, dict]:
        send_message: SendMessage = {"method": "reset", "data": {}}
        res = cast(ResetResponse, self.send(json.dumps(send_message)))
        return res["state"], res["info"]

    def step(self, action: Action, count: int) -> Tuple[Observation, float, bool, bool, dict]:
        send_message: SendMessage = {"method": "step", "data": {"action": str(action), "count": count}}
        res = cast(StepResponse, self.send(json.dumps(send_message)))
        return res["observation"], res["reward"], res["terminated"], res["truncated"], res["info"]

    def close(self) -> None:
        if not self.__ws:
            return

        async def async_close():
            await self.__ws.close()
            self.__is_closed = True
            return

        asyncio.get_event_loop().run_until_complete(async_close())
        asyncio.get_event_loop().close()

        return

    @property
    def is_closed(self) -> bool:
        return self.__is_closed


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
