from typing import Generic, TypeVar, Union

from core.coretypes import Response, Error

T = TypeVar("T")


class BaseChecker(Generic[T]):

    def __init__(self, target: str):
        self.target = target

    async def check(self) -> Union[Response[Error], Response[T]]:
        raise NotImplementedError
