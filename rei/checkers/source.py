import asyncio
import socket

import a2s
from core.coretypes import (
    Response, Error, ResponseStatus, ErrorCodes, SourceServerResponse, SourceServerDetails
)

from rei.checkers.base import BaseChecker


class SourceChecker(BaseChecker):

    def __init__(self, target: str, port: int):
        self.port = port
        super().__init__(target)
        self.address = (self.target, self.port)

    def send_error(self, message: str):
        return Response[Error](
            status=ResponseStatus.ERROR,
            payload=Error(
                message=message,
                code=ErrorCodes.ConnectError
            ),
        )

    async def check(self) -> Response:

        try:
            info: a2s.SourceInfo = await a2s.ainfo(self.address)
            players = await a2s.aplayers(self.address)
            rules = await a2s.arules(self.address)
        except a2s.BrokenMessageError:
            return self.send_error("Сервер вернул несериализуемый ответ")
        except socket.gaierror:
            return self.send_error("Неправильный или несуществующий адрес")
        except asyncio.TimeoutError:
            return self.send_error("Таймаут")
        else:
            return Response[SourceServerResponse](
                status=ResponseStatus.OK,
                payload=SourceServerResponse(
                    ping=info.ping
                ),
                details=SourceServerDetails(
                    **dict(info), players=players, rules=rules
                )
            )
