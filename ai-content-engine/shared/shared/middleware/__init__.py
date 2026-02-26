"""FastAPI middleware components."""

from shared.middleware.auth import JWTAuthMiddleware
from shared.middleware.correlation import CorrelationIDMiddleware
from shared.middleware.error_handler import register_error_handlers

__all__ = ["JWTAuthMiddleware", "CorrelationIDMiddleware", "register_error_handlers"]
