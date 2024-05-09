import socket
import asyncio
from typing import Tuple, Union

from core.coretypes import (
    Response,
    PortResponse,
    ResponseStatus,
    Error,
    ErrorCodes,
    PortDetails
)
from rei.checkers.base import BaseChecker

exceptions = {
    "ConnectionRefusedError": "Соединение сброшено",
    "TimeoutError": "Нет ответа или таймаут",
    "OSError": "Ошибка сети",
    "gaierror": "Ошибка определения"
}


class TCPPortChecker(BaseChecker[PortResponse]):

    def __init__(self, target: str, port: int):
        self.port = port
        self._loop = asyncio.get_event_loop()

        super().__init__(target)

    async def _check_target(self) -> Tuple[bool, str]:
        try:
            # TODO: timeout arg
            await asyncio.wait_for(
                asyncio.open_connection(
                    self.target, self.port, loop=self._loop
                ), timeout=10
            )
        except (ConnectionRefusedError, OSError, asyncio.TimeoutError, socket.gaierror) as err:
            return False, exceptions[err.__class__.__name__]
        try:
            service = socket.getservbyport(self.port)
        except OSError:
            # TODO: port service check
            return True, 'Неизвестно'
        return True, service

    async def check(self) -> Union[Response[Error], Response[PortResponse]]:
        port_opened, service = await self._check_target()
        if port_opened:
            return Response(
                status=ResponseStatus.OK,
                payload=PortResponse(
                    open=True,
                ),
                details=PortDetails(
                    service=service
                )
            )
        else:
            return Response(
                status=ResponseStatus.ERROR,
                payload=Error(
                    message=service,
                    code=ErrorCodes.InvalidHostname
                )
            )



