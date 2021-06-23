from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from rei.config import NODE_NAME, NODE_TOWN, NODE_COUNTRY


class AuthMiddleware(BaseHTTPMiddleware):

    def __init__(self, auth_token: str, app: ASGIApp):
        super().__init__(app)
        self.auth_token = auth_token

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.headers.get('Token', None) == self.auth_token:
            response = await call_next(request)
            return response
        else:
            return Response(status_code=403)


class NodeInfoMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        response.headers['x-node-name'] = NODE_NAME
        response.headers['x-node-town'] = NODE_TOWN
        response.headers['x-node-country'] = NODE_COUNTRY
        return response
