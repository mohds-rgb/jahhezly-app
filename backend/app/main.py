import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .api.routes import auth, merchant, public
from .domain.errors import DomainError

logger = logging.getLogger("jahhezly.api")

app = FastAPI(
    title="Jahhezly API",
    version="0.2.0",
    description="Offline-first Click & Collect portfolio API.",
)

@app.middleware("http")
async def request_context(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-Id") or uuid.uuid4().hex
    request.state.correlation_id = correlation_id
    response = await call_next(request)
    response.headers["X-Correlation-Id"] = correlation_id
    return response

@app.exception_handler(DomainError)
async def domain_error_handler(_: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status,
        content={"code": exc.code, "message": exc.message, "details": exc.details},
    )

@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, exc: Exception):
    logger.exception("unhandled_error correlation_id=%s", request.state.correlation_id)
    return JSONResponse(
        status_code=500,
        content={"code":"SERVICE_UNAVAILABLE","message":"The service could not complete the request.","details":{}},
    )

@app.get("/health", tags=["ops"])
def health():
    return {"status":"ok","service":"jahhezly-api"}

app.include_router(auth.router)
app.include_router(public.router)
app.include_router(merchant.router)
