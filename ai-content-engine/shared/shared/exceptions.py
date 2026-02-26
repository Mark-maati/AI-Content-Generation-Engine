"""Application-wide exception hierarchy."""


class AppError(Exception):
    """Base application error."""

    def __init__(
        self,
        message: str,
        code: str,
        status_code: int = 500,
        details: list | None = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or []
        super().__init__(message)


class ValidationError(AppError):
    """Raised when input validation fails."""

    def __init__(
        self,
        message: str = "Validation failed",
        details: list | None = None,
    ):
        super().__init__(
            message=message,
            code="validation_error",
            status_code=422,
            details=details,
        )


class AuthenticationError(AppError):
    """Raised when authentication is required or fails."""

    def __init__(self, message: str = "Authentication required"):
        super().__init__(message=message, code="unauthorized", status_code=401)


class AuthorizationError(AppError):
    """Raised when the user lacks sufficient permissions."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message=message, code="forbidden", status_code=403)


class NotFoundError(AppError):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            message=f"{resource} with id '{resource_id}' not found",
            code="not_found",
            status_code=404,
        )


class ConflictError(AppError):
    """Raised when a resource conflict occurs."""

    def __init__(self, message: str = "Resource conflict"):
        super().__init__(message=message, code="conflict", status_code=409)


class RateLimitError(AppError):
    """Raised when a rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: int = 60,
    ):
        super().__init__(
            message=message,
            code="rate_limit_exceeded",
            status_code=429,
        )
        self.retry_after = retry_after


class UpstreamError(AppError):
    """Raised when an upstream service returns an error."""

    def __init__(self, message: str = "Upstream service error"):
        super().__init__(message=message, code="upstream_error", status_code=502)


class ServiceUnavailableError(AppError):
    """Raised when the service is temporarily unavailable."""

    def __init__(self, message: str = "Service temporarily unavailable"):
        super().__init__(
            message=message,
            code="service_unavailable",
            status_code=503,
        )
