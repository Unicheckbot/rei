import logging

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware  # type: ignore

from rei.middleware import AuthMiddleware, NodeInfoMiddleware
from rei.routes.checkers import routes as checkers_routes
from rei.tasks import register_node

from rei.config import TOKEN, INFO, APP_PORT

logger = logging.getLogger("uvicorn.info")


async def info(_: Request) -> JSONResponse:
    return JSONResponse(INFO)

scheduler = AsyncIOScheduler()

middleware = [
    Middleware(NodeInfoMiddleware),
    Middleware(AuthMiddleware, auth_token=TOKEN),
    Middleware(ProxyHeadersMiddleware, trusted_hosts="*"),
]

routes = [
    Route('/info', info),
    Mount('/check', routes=checkers_routes)
]

scheduler.add_job(register_node, "interval", minutes=5)
app = Starlette(routes=routes, middleware=middleware, on_startup=[
    register_node,
    scheduler.start,
])
if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run(app=app, port=APP_PORT) # noqa
