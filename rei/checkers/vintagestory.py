from typing import Union

from core.coretypes import Response, Error, ResponseStatus, ErrorCodes
from httpx import AsyncClient
from pydantic import BaseModel, Field

from rei.checkers.base import BaseChecker, T


class VSMod(BaseModel):
    id: str
    version: str


class VSPlayStyle(BaseModel):
    id: str
    lang_code: str = Field(alias="langCode")


class VSServer(BaseModel):
    server_name: str = Field(alias="serverName")
    server_ip: str = Field(alias="serverIP")
    mods: list[VSMod]
    max_players: int = Field(alias="maxPlayers")
    players: int
    game_version: str = Field(alias="gameVersion")
    has_password: bool = Field(alias="hasPassword")
    whitelisted: str = Field(alias="whitelisted")
    game_description: str = Field(alias="gameDescription")


class VintageStoryChecker(BaseChecker[VSServer]):
    def __init__(self, target: str, port: int, client: AsyncClient):
        super().__init__(target)
        self.port = port
        self._client = client

    async def _get_servers_from_masterserver(self) -> list[VSServer]:
        response = await self._client.get("https://masterserver.vintagestory.at/api/v1/")
        data = response.json()
        return [VSServer(**server) for server in data["data"]]

    async def check(self) -> Union[Response[Error], Response[VSServer]]:
        servers = await self._get_servers_from_masterserver()
        server: list[VSServer] = list(filter(lambda x: x.server_ip == f"{self.target}:{self.port}", servers))
        if not server:
            return Response[Error](
                status=ResponseStatus.ERROR,
                payload=Error(
                    message="Сервер не найден в мастер-сервере",
                    code=ErrorCodes.InvalidHostname,
                ),
            )
        return Response[VSServer](
            status=ResponseStatus.OK,
            payload=server[0]
        )
