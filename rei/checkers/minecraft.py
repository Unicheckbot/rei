from typing import Optional

from core.coretypes import (
    Response, Error, ErrorCodes, MinecraftResponse, ResponseStatus, MinecraftDetails
)
from mcstatus import MinecraftServer
from .base import BaseChecker
import socket


class MinecraftChecker(BaseChecker):

    def __init__(self, target: str, port: Optional[int]):
        super().__init__(target)
        self.port = port
        if self.port is None:
            self.address = self.target
        else:
            self.address = f"{self.target}:{self.port}"

    async def check(self) -> Response:

        try:
            server = MinecraftServer.lookup(self.address)
            status = await server.async_status()
        except (socket.gaierror, ConnectionRefusedError, TimeoutError):
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
                port=server.port if self.port is None else None,
                max_players=status.players.max,
                online=status.players.online
            )
        )



