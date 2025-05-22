from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from api.routes import router
from starlette.middleware.base import BaseHTTPMiddleware
import datetime
import json
import logging
import sys
from core.config import settings
import traceback

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name
        }
        if record.exc_info:
             log_entry["exception"] = self.formatException(record.exc_info)
        if record.__dict__.get('extra'):
            log_entry.update(record.__dict__['extra'])
        return json.dumps(log_entry)

def setup_logging():
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger.setLevel(logging.INFO)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)
    return logger

logger = setup_logging()
app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)


instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, endpoint="/metrics")

class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = datetime.datetime.utcnow()
        response = await call_next(request)
        process_time = (datetime.datetime.utcnow() - start_time).total_seconds()

        if request.url.path != "/health":
            log_data = {
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time": f"{process_time:.4f}s"
            }
            logger.info("Request served", extra=log_data)
        else:
            pass
        return response

app.add_middleware(LogMiddleware)
app.include_router(router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_traceback = traceback.format_exc()

    error_data = {
        "error": "Internal Server Error",
        "status_code": 500,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "path": str(request.url),
        "message": str(exc), 
        "traceback": error_traceback 
    }

    logger.error("Unhandled Exception", extra=error_data, exc_info=True)

    public_error_data = {
        "error": "Internal Server Error",
        "status_code": 500,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "path": str(request.url),
        "message": "An unexpected error occurred. Please try again later."
    }

    return JSONResponse(status_code=500, content=public_error_data)

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    error_data = {
        "error": "El endpoint al que intentas acceder no existe.",
        "status_code": 404,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "path": str(request.url)
    }

    logger.info("Not Found", extra=error_data)
    return JSONResponse(status_code=404, content=error_data)
