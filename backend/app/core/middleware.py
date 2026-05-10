from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Match
from fastapi.responses import JSONResponse

class InputSanitizerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Ограничить размер query-параметров
        if len(str(request.url)) > 2000:
            return JSONResponse({"detail": "URL too long"}, status_code=414)
        return await call_next(request)