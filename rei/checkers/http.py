import re
from typing import Union

from requests import Session, Response as RequestResponse
from requests.exceptions import ConnectionError

from rei.checkers.base import BaseChecker
from rei.utils import run_in_eventloop
from core.coretypes import (
    Response,
    HttpCheckerResponse,
    ResponseStatus,
    ErrorCodes,
    Error,
)


class HttpChecker(BaseChecker[HttpCheckerResponse]):

    default_schema = "http://"
    default_schema_re = re.compile("^[hH][tT][tT][pP].*")

    def __init__(self, target: str, port: int):
        super(HttpChecker, self).__init__(target)
        self.port = port
        self.session = Session()

    def request(self, url: str) -> RequestResponse:
        return self.session.head(
            url,
            allow_redirects=True,
        )

    async def check(self) -> Union[Response[Error], Response[HttpCheckerResponse]]:

        url = f"{self.target}:{self.port}"
        if not self.default_schema_re.match(url):
            url = f"{self.default_schema}{url}"

        try:
            request: RequestResponse = await run_in_eventloop(self.request, url)
        except ConnectionError:
            return Response[Error](
                status=ResponseStatus.ERROR,
                payload=Error(
                    message="Ошибка при установлении подключения",
                    code=ErrorCodes.ConnectError,
                ),
            )

        return Response[HttpCheckerResponse](
            status=ResponseStatus.OK,
            payload=HttpCheckerResponse(
                time=request.elapsed.total_seconds(),
                status_code=request.status_code
            ),
        )
