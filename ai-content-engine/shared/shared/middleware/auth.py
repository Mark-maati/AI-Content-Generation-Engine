"""JWT authentication middleware."""

import structlog
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

logger = structlog.get_logger(__name__)

security = HTTPBearer(auto_error=False)


class JWTAuthMiddleware:
    """JWT token verification dependency."""

    def __init__(self, secret: str, algorithm: str = "HS256") -> None:
        self._secret = secret
        self._algorithm = algorithm

    async def __call__(
        self, credentials: HTTPAuthorizationCredentials | None = Depends(security)
    ) -> dict:
        if credentials is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            payload = jwt.decode(
                credentials.credentials,
                self._secret,
                algorithms=[self._algorithm],
            )
            return payload
        except JWTError as e:
            logger.warning("jwt_validation_failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
