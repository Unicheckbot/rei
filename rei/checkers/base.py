from core.coretypes import Response
from abc import ABC


class BaseChecker(ABC):

    def __init__(self, target: str):
        self.target = target

    async def check(self) -> Response:
        raise NotImplementedError
