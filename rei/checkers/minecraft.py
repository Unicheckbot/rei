from typing import Optional, Union
from asyncio.exceptions import TimeoutError as AsyncTimeoutError
import socket

from core.coretypes import (
    Response,
    Error,
    ErrorCodes,
    MinecraftResponse,
    ResponseStatus,
    MinecraftDetails
)
from mcstatus import JavaServer, BedrockServer
from mcstatus.status_response import BaseStatusResponse

from rei.checkers.base import BaseChecker


class MinecraftChecker(BaseChecker[MinecraftResponse]):

    def __init__(self, target: str, port: Optional[int]):
        super().__init__(target)
        self.port = port
        if self.port is None:
            self.address = self.target
        else:
            self.address = f"{self.target}:{self.port}"

    async def _get_server_status(self) -> Union[None, BaseStatusResponse]:
        errors = (socket.gaierror, ConnectionRefusedError, TimeoutError, AsyncTimeoutError)

        try:
            java_server = await JavaServer.async_lookup(self.address)
            java_status = await java_server.async_status()
            return java_status
        except errors:
            pass

        try:
            bedrock_server = BedrockServer.lookup(self.address)
            bedrock_status = await bedrock_server.async_status()
            return bedrock_status
        except errors:
            pass

        return None

    async def check(self) -> Union[Response[Error], Response[MinecraftResponse]]:

        status = await self._get_server_status()
        if not status:
            return Response[Error](
                status=ResponseStatus.ERROR,
                payload=Error(
                    message="Сервер не отвечает",
                    code=ErrorCodes.ConnectError
                ),
            )
        return Response[MinecraftResponse](
            status=ResponseStatus.OK,
            payload=MinecraftResponse(
                latency=status.latency,
            ),
            details=MinecraftDetails(
                version=status.version.name,
                protocol=status.version.protocol,
                port=self.port,
                max_players=status.players.max,
                online=status.players.online
            )
        )



