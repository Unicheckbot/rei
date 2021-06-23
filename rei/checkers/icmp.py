from icmplib import async_ping
from icmplib.exceptions import NameLookupError

from core.coretypes import (
    Response, Error, ErrorCodes, ResponseStatus, ICMPCheckerResponse, ICMPDetails
)
from rei.checkers.base import BaseChecker


class ICMPChecker(BaseChecker):

    def __init__(self, target: str):
        super().__init__(target)

    def create_not_alive_response(self):
        return Response[Error](
            status=ResponseStatus.ERROR,
            payload=Error(
                code=ErrorCodes.ICMPHostNotAlive,
                message="Хост не доступен для ICMP проверки"
            )
        )

    async def check(self) -> Response:

        try:
            host = await async_ping(self.target)
        except NameLookupError:
            return self.create_not_alive_response()

        if not host.is_alive:
            return self.create_not_alive_response()
        return Response[ICMPCheckerResponse](
            status=ResponseStatus.OK,
            payload=ICMPCheckerResponse(
                min_rtt=host.min_rtt,
                max_rtt=host.max_rtt,
                avg_rtt=host.avg_rtt,
                packets_sent=host.packets_sent,
                packets_received=host.packets_received,
            ),
            details=ICMPDetails(
                rtts=host.rtts,
                jitter=host.jitter,
                loss=host.packet_loss,
            )
        )
