from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.utils.jwt import verify_access_token


class AuthMiddleware(BaseHTTPMiddleware):

  async def dispatch(self, request: Request, call_next):
    try:
      public_routes = [
          "/",
          "/auth/login",
          "/auth/signup",
          "/auth/google",
          "/auth/google/callback",
          "/docs",
          "/pretty-docs",
          "/openapi.json",
          "/auth/forgot-password",
          "/auth/reset-password",
          "/otp/verify",
          "/otp/generate",
          "/users",
      ]
      if request.url.path in public_routes or request.method == "OPTIONS":
        return await call_next(request)

      auth_header = request.headers.get("Authorization")
      if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: Missing or invalid Authorization header",
        )

      token = auth_header.split(" ")[1]

      user = verify_access_token(token)
      request.state.user = user

      return await call_next(request)

    except HTTPException as http_exc:
      return JSONResponse(
          status_code=http_exc.status_code,
          content={"detail": http_exc.detail},
      )
    except Exception:
      return JSONResponse(
          status_code=500,
          content={"detail": "Internal Server Error. Please contact support."},
      )
