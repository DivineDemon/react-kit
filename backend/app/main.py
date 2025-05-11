import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.database.db_config import close_database, create_database
from app.logging_config import setup_logging
from app.middlewares.auth_middleware import AuthMiddleware
from app.routes import auth, otp, user


@asynccontextmanager
async def lifespan(app: FastAPI):
  setup_logging()
  create_database()
  try:
    yield
  finally:
    close_database()
    logging.info("Database engine disposed.")


app = FastAPI(
    lifespan=lifespan,
    title="React Kit BE",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/pretty-docs",
)

logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(otp.router)


@app.get("/", tags=["Health Check"])
async def health_check():
  logger.info("Health check endpoint called")
  return {"status": "ok"}


@app.middleware("http")
async def log_requests(request: Request, call_next):
  logger.info(f"→ {request.method} {request.url.path} started")
  response = await call_next(request)
  logger.info(
      f"← {request.method} {request.url.path}. Status: {response.status_code}")
  return response
