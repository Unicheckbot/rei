from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route

from rei.routes.utils import check_target_port, Counter
from rei.checkers.http import HttpChecker
from rei.checkers.icmp import ICMPChecker
from rei.checkers.minecraft import MinecraftChecker
from rei.checkers.tcp import TCPPortChecker
from rei.checkers.source import SourceChecker


@Counter('http')
async def http(request: Request):
    target, port = check_target_port(request)
    checker = HttpChecker(target, port)
    return JSONResponse((await checker.check()).dict())


@Counter('icmp')
async def icmp(request: Request):
    target = request.query_params.get("target")
    checker = ICMPChecker(target)
    return JSONResponse((await checker.check()).dict())


@Counter('minecraft')
async def minecraft(request: Request):
    target = request.query_params.get("target")
    port = request.query_params.get("port", None)
    checker = MinecraftChecker(target, port)
    return JSONResponse((await checker.check()).dict())


@Counter('tcp')
async def tcp(request: Request):
    target, port = check_target_port(request)
    checker = TCPPortChecker(target, port)
    return JSONResponse((await checker.check()).dict())


@Counter('source')
async def source(request: Request):
    target, port = check_target_port(request)
    checker = SourceChecker(target, port)
    return JSONResponse((await checker.check()).dict())

routes = [
    Route('/http', http),
    Route('/icmp', icmp),
    Route('/minecraft', minecraft),
    Route('/tcp', tcp),
    Route('/source', source)
]
