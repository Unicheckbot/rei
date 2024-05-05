import json
import zlib

from core.coretypes import Response, ResponseStatus, Error, ErrorCodes
from pydantic import BaseModel, Field
from requests import Session

from rei.checkers.base import BaseChecker


class SPTConfig(BaseModel):
    backend_url: str = Field(alias="backendUrl")
    name: str
    editions: list[str]


class SPTMod(BaseModel):
    name: str
    version: str
    author: str
    license: str


class SPTServerResponse(BaseModel):
    aki_version: str
    game_version: str
    config: SPTConfig
    mods: list[SPTMod]


class SPTChecker(BaseChecker):

    def __init__(self, target: str, session: Session):
        super().__init__(target)
        self._session = session

    def _send_request(self, path: str) -> str:
        response = self._session.get(f"{self.target}/{path}")
        response.raise_for_status()
        return zlib.decompress(response.content).decode("utf-8")

    def _get_ping(self) -> bool:
        result = self._send_request("launcher/ping")
        return True if result == "pong!" else None

    def _get_server_version(self) -> str:
        return self._send_request("launcher/server/version").replace('"', '')

    def _get_game_version(self) -> str:
        return self._send_request("launcher/profile/compatibleTarkovVersion").replace('"', '')

    def _get_server_connect_info(self) -> SPTConfig:
        response = json.loads(self._send_request("launcher/server/connect"))
        return SPTConfig(**response)

    def _get_server_mods(self):
        response = json.loads(self._send_request("launcher/server/loadedServerMods"))
        return [
            SPTMod(
                name=response[key]["name"],
                version=response[key]["version"],
                author=response[key]["author"],
                license=response[key]["license"]
            )
            for key in response.keys()
        ]

    async def check(self) -> Response:
        try:
            self._get_ping()
        except: # noqa
            return Response[Error](
                status=ResponseStatus.ERROR,
                payload=Error(
                    message="Сервер не отвечает",
                    code=ErrorCodes.ConnectError
                ),
            )

        payload = SPTServerResponse(
            aki_version=self._get_server_version(),
            game_version=self._get_game_version(),
            config=self._get_server_connect_info(),
            mods=self._get_server_mods()
        )

        self._get_server_mods()

        return Response[SPTServerResponse](
            status=ResponseStatus.OK,
            payload=payload
        )
