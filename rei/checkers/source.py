import asyncio
import socket
from typing import Union

import a2s  # type: ignore
from core.coretypes import (
    Response,
    Error,
    ResponseStatus,
    ErrorCodes,
    SourceServerResponse,
    SourceServerDetails,
    SourceServerPlayer
)

from rei.checkers.base import BaseChecker


def send_error(message: str) -> Response[Error]:
    return Response[Error](
        status=ResponseStatus.ERROR,
        payload=Error(
            message=message,
            code=ErrorCodes.ConnectError
        ),
    )


class SourceChecker(BaseChecker[SourceServerResponse]):

    def __init__(self, target: str, port: int):
        self.port = port
        super().__init__(target)
        self.address = (self.target, self.port)

    async def check(self) -> Union[Response[Error], Response[SourceServerResponse]]:
        try:
            info: a2s.SourceInfo = await a2s.ainfo(self.address)
        except a2s.BrokenMessageError:
            return send_error("Сервер вернул несериализуемый ответ")
        except socket.gaierror:
            return send_error("Неправильный или несуществующий адрес")
        except asyncio.TimeoutError:
            return send_error("Таймаут")

        try:
            players = [
                SourceServerPlayer(
                    name=player.name,
                    duration=player.duration,
                    score=player.score
                ) for player in await a2s.aplayers(self.address)
            ]
        except (socket.gaierror, asyncio.TimeoutError, a2s.BrokenMessageError):
            players = []

        try:
            rules = await a2s.arules(self.address)
        except (socket.gaierror, asyncio.TimeoutError, a2s.BrokenMessageError):
            rules = {}

        return Response[SourceServerResponse](
            status=ResponseStatus.OK,
            payload=SourceServerResponse(
                ping=info.ping
            ),
            details=SourceServerDetails(
                **dict(info), players=players, rules=rules
            )
        )
