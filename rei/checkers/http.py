import re
from typing import Union

from core.coretypes import (
    Response,
    HttpCheckerResponse,
    ResponseStatus,
    ErrorCodes,
    Error,
)
from httpx import AsyncClient, ConnectTimeout, ConnectError

from rei.checkers.base import BaseChecker


class HttpChecker(BaseChecker[HttpCheckerResponse]):

    default_schema = "http://"
    default_schema_re = re.compile("^[hH][tT][tT][pP].*")

    def __init__(self, target: str, port: int, client: AsyncClient):
        super(HttpChecker, self).__init__(target)
        self.port = port
        self._client = client

    async def check(self) -> Union[Response[Error], Response[HttpCheckerResponse]]:

        url = f"{self.target}:{self.port}"
        if not self.default_schema_re.match(url):
            url = f"{self.default_schema}{url}"

        try:
            response = await self._client.get(url, follow_redirects=True)
        except (ConnectError, ConnectTimeout):
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
                time=response.elapsed.total_seconds(),
                status_code=response.status_code
            ),
        )
