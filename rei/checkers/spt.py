import json
import zlib
from typing import Union

from core.coretypes import (
    Response,
    ResponseStatus,
    Error,
    ErrorCodes,
    SPTConfig,
    SPTMod,
    SPTServerResponse
)
from httpx import AsyncClient

from rei.checkers.base import BaseChecker


class SPTChecker(BaseChecker[SPTServerResponse]):

    def __init__(self, target: str, client: AsyncClient):
        super().__init__(target)
        self._client = client

    async def _send_request(self, path: str) -> str:
        response = await self._client.get(f"{self.target}/{path}")
        response.raise_for_status()
        return zlib.decompress(response.content).decode("utf-8")

    async def _get_ping(self) -> bool:
        result = await self._send_request("launcher/ping")
        return True if result == "pong!" else False

    async def _get_server_version(self) -> str:
        return (await self._send_request("launcher/server/version")).replace('"', '')

    async def _get_game_version(self) -> str:
        return (await self._send_request("launcher/profile/compatibleTarkovVersion")).replace('"', '')

    async def _get_server_connect_info(self) -> SPTConfig:
        response = json.loads(await self._send_request("launcher/server/connect"))
        return SPTConfig(**response)

    async def _get_server_mods(self) -> list[SPTMod]:
        response = json.loads(await self._send_request("launcher/server/loadedServerMods"))
        return [
            SPTMod(
                name=response[key]["name"],
                version=response[key]["version"],
                author=response[key]["author"],
                license=response[key]["license"]
            )
            for key in response.keys()
        ]

    async def check(self) -> Union[Response[Error], Response[SPTServerResponse]]:
        try:
            await self._get_ping()
        except:  # noqa
            return Response[Error](
                status=ResponseStatus.ERROR,
                payload=Error(
                    message="Сервер не отвечает",
                    code=ErrorCodes.ConnectError
                ),
            )

        payload = SPTServerResponse(
            aki_version=await self._get_server_version(),
            game_version=await self._get_game_version(),
            config=await self._get_server_connect_info(),
            mods=await self._get_server_mods()
        )

        return Response[SPTServerResponse](
            status=ResponseStatus.OK,
            payload=payload
        )
