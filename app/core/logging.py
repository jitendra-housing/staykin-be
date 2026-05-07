import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("staykin")

# Skip noisy or non-API paths from request logging entirely.
_SKIP_PATHS = {"/openapi.json", "/docs", "/redoc", "/docs/oauth2-redirect", "/health"}


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    """Log non-2xx responses with both the request body and response body so
    failures (especially 422 validation errors from the FE) are debuggable
    from `docker compose logs api` alone. 2xx requests get one concise line.
    """

    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        if request.url.path in _SKIP_PATHS:
            return await call_next(request)

        # Cache the body so downstream handlers can still read it.
        body_bytes = await request.body()

        async def receive():
            return {"type": "http.request", "body": body_bytes, "more_body": False}

        request._receive = receive  # type: ignore[attr-defined]

        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.exception(
                "500 %s %s | %.0fms | body=%s",
                request.method,
                request.url.path,
                elapsed_ms,
                _truncate(body_bytes),
            )
            raise

        elapsed_ms = (time.perf_counter() - start) * 1000
        status = response.status_code

        if status < 400:
            logger.info("%d %s %s | %.0fms", status, request.method, request.url.path, elapsed_ms)
            return response

        # Drain and rebuild the response so we can log the JSON body.
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        logger.warning(
            "%d %s %s | %.0fms | req=%s | resp=%s",
            status,
            request.method,
            request.url.path,
            elapsed_ms,
            _truncate(body_bytes),
            _truncate(response_body),
        )

        headers = dict(response.headers)
        headers.pop("content-length", None)  # let Response recompute
        return Response(
            content=response_body,
            status_code=status,
            headers=headers,
            media_type=response.media_type,
        )


def _truncate(b: bytes, limit: int = 1000) -> str:
    if not b:
        return ""
    s = b.decode("utf-8", errors="replace")
    if len(s) > limit:
        s = s[:limit] + f"…(+{len(s) - limit} more)"
    # Collapse newlines so each request stays on a single log line.
    return s.replace("\n", " ").replace("\r", " ")
