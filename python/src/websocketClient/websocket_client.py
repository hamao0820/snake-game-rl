import json
from typing import Any, Generic, Literal, Tuple, TypeAlias, TypedDict, TypeVar, Union, cast

from websockets import client

# import asyncio


class ImageMessage(TypedDict):
    type: str
    data: bytes


class SendMessage(TypedDict):
    method: str
    data: dict


class ResetResponse(TypedDict):
    state: Any
    info: dict


class StepResponse(TypedDict):
    observation: Any
    reward: float
    terminated: bool
    truncated: bool
    info: dict


ObsType = TypeVar("ObsType")

# 0:straight, 1:left, 2:right
Action: TypeAlias = Union[Literal[0], Literal[1], Literal[2]]


class WebsocketClient(Generic[ObsType]):
    def __init__(self) -> None:
        self.__server_address = "ws://localhost:8080"
        self.__ws: Union[client.WebSocketClientProtocol, None] = None
        self.__is_closed: bool = False

    async def connect(self) -> None:
        self.__ws = await client.connect(self.__server_address)
        print(await self.__ws.recv())
        print("connected")
        return

    async def send(self, data: Union[str, int]):
        if self.__ws is None:
            raise Exception("Not connected to server")
        await self.__ws.send(str(data))
        data = json.loads(await self.__ws.recv())
        return data

    async def reset(self) -> Tuple[ObsType, dict]:
        send_message: SendMessage = {"method": "reset", "data": {}}
        data = cast(ResetResponse, await self.send(json.dumps(send_message)))
        return cast(ObsType, data["state"]), data["info"]

    async def step(self, action: Action) -> Tuple[ObsType, float, bool, bool, dict]:
        send_message: SendMessage = {"method": "step", "data": {"action": action}}
        data = cast(StepResponse, await self.send(json.dumps(send_message)))
        return data["observation"], data["reward"], data["terminated"], data["truncated"], data["info"]

    async def close(self) -> None:
        if not self.__ws:
            return

        await self.__ws.close()
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
