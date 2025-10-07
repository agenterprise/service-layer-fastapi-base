import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)


class BaseHttpMiddleware():
    """Middleware to validate Origin header according to MCP specification.
    This prevents DNS rebinding attacks by ensuring requests come from trusted origins."""



    def define_middleware(self, app: FastAPI):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        @app.middleware("http")
        async def origin_validation_middleware(request: Request, call_next):
            """
            Middleware to validate Origin header according to MCP specification.
            This prevents DNS rebinding attacks by ensuring requests come from trusted origins.
            """
            # Skip validation for health check endpoint (optional)
            if request.url.path == "/health":
                response = await call_next(request)
                return response
            
            # Get the Origin header
            origin = request.headers.get("origin")
            
            if not origin:
                logger.info("✅ No Origin header")
                response = await call_next(request)
                return response
            # Validate the origin - allow localhost and 127.0.0.1 on any port
            if not origin or (not origin.startswith("http://localhost") and not origin.startswith("http://127.0.0.1") and not origin.startswith("http://0.0.0.0")):
                return JSONResponse(
                    status_code=403,
                    content={"detail": f"Origin '{origin}' is not allowed. Only localhost and 127.0.0.1 are permitted."}
                )
            
            response = await call_next(request)
            return response


                