import asyncio
import logging

from httpx import AsyncClient
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware  # type: ignore

from rei.middleware import AuthMiddleware, NodeInfoMiddleware
from rei.routes.checkers import routes as checkers_routes
from rei.tasks import register_node

from rei.config import TOKEN, INFO, APP_PORT

logger = logging.getLogger("uvicorn.info")


async def info(_: Request) -> JSONResponse:
    return JSONResponse(INFO)


middleware = [
    Middleware(NodeInfoMiddleware),
    Middleware(AuthMiddleware, auth_token=TOKEN),
    Middleware(ProxyHeadersMiddleware, trusted_hosts="*"),
]

routes = [
    Route('/info', info),
    Mount('/check', routes=checkers_routes)
]
http_client = AsyncClient()

background_tasks = set()


async def register_node_task() -> None:
    # keeping reference to task to avoid a task disappearing mid-execution
    task = asyncio.create_task(register_node(http_client))
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)


app = Starlette(
    routes=routes,
    middleware=middleware,
    on_startup=[
        register_node_task
    ],
    on_shutdown=[
        http_client.aclose,
        background_tasks.discard
    ]
)
app.state.http_client = http_client  # type: ignore
if __name__ == "__main__":
    import uvicorn  # type: ignore

    uvicorn.run(app=app, port=APP_PORT)  # noqa
