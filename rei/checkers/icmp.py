from typing import Union

from icmplib import async_ping  # type: ignore
from icmplib.exceptions import NameLookupError  # type: ignore

from core.coretypes import (
    Response,
    Error,
    ErrorCodes,
    ResponseStatus,
    ICMPCheckerResponse,
    ICMPDetails
)
from rei.checkers.base import BaseChecker
from rei.config import ICMP_PRIVILEGED


def create_not_alive_response() -> Response[Error]:
    return Response[Error](
        status=ResponseStatus.ERROR,
        payload=Error(
            code=ErrorCodes.ICMPHostNotAlive,
            message="Хост не доступен для ICMP проверки"
        )
    )


class ICMPChecker(BaseChecker[ICMPCheckerResponse]):

    def __init__(self, target: str):
        super().__init__(target)

    async def check(self) -> Union[Response[Error], Response[ICMPCheckerResponse]]:

        try:
            host = await async_ping(self.target, privileged=ICMP_PRIVILEGED)
        except NameLookupError:
            return create_not_alive_response()
        if not host.is_alive:
            return create_not_alive_response()
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
