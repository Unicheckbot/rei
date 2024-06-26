from typing import Union

from core.coretypes import (
    Response,
    Error,
    ResponseStatus,
    ErrorCodes,
    VintageStoryResponse,
    VintageStoryDetails
)
from httpx import AsyncClient, ConnectError, ConnectTimeout

from rei.checkers.base import BaseChecker


class VintageStoryChecker(BaseChecker[VintageStoryResponse]):
    def __init__(self, target: str, port: int, client: AsyncClient):
        super().__init__(target)
        self.port = port
        self._client = client

    async def _get_servers_from_masterserver(self) -> list[VintageStoryDetails]:
        response = await self._client.get("https://masterserver.vintagestory.at/api/v1/")
        data = response.json()
        return [VintageStoryDetails(**server) for server in data["data"]]

    async def check(self) -> Union[Response[Error], Response[VintageStoryResponse]]:
        try:
            servers = await self._get_servers_from_masterserver()
        except (ConnectError, ConnectTimeout):
            return Response[Error](
                status=ResponseStatus.ERROR,
                payload=Error(
                    message="Мастер-сервер не доступен",
                    code=ErrorCodes.ConnectError,
                ),
            )
        server: list[VintageStoryDetails] = list(filter(lambda x: x.server_ip == f"{self.target}:{self.port}", servers))
        if not server:
            return Response[Error](
                status=ResponseStatus.ERROR,
                payload=Error(
                    message="Сервер не найден в мастер-сервере",
                    code=ErrorCodes.InvalidHostname,
                ),
            )
        return Response[VintageStoryResponse](
            status=ResponseStatus.OK,
            payload=VintageStoryResponse(),
            details=server[0]
        )
