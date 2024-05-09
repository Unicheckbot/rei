from typing import Tuple, Callable, TypeVar, Any, cast, Awaitable

from starlette.requests import Request

from rei.routes.exceptions import TargetOrPortInvalid
from rei.config import METHODS_COUNTER

FuncT = TypeVar('FuncT', bound=Callable[..., Awaitable[Any]])


def check_target_port(request: Request) -> Tuple[str, int]:
    target = request.query_params.get("target", None)
    try:
        port = int(request.query_params.get("port", None))
    except TypeError:
        raise TargetOrPortInvalid
    if not target or not port:
        raise TargetOrPortInvalid
    return target, port


class Counter:

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def __call__(self, func: FuncT) -> FuncT:
        async def wrapped(*args: object, **kwargs: object) -> Any:
            METHODS_COUNTER[self.endpoint] += 1
            return await func(*args, **kwargs)
        return cast(FuncT, wrapped)

