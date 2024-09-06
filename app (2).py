from .custom_logger import log, chan, formatter

import logging
from time import time

loading_start = time()

# Server
from fastapi import FastAPI, WebSocket
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(_app: FastAPI):
    log.info("Starting the app")
    # Init custom loggers
    logger = logging.getLogger("uvicorn.access")
    logger.handlers[0].setFormatter(formatter)
    logger2 = logging.getLogger("uvicorn.error")

    # Remove default handlers and add ours
    logger2.handlers = []
    logger2.addHandler(chan)
    logger2.propagate = False

    logger3 = logging.getLogger("track.analysis")
    # Remove default handlers and add ours
    logger3.handlers = []
    logger3.addHandler(chan)
    logger3.handlers[0].setFormatter(formatter)
    logger3.propagate = False

    yield
    # Application shutdown procedure
    log.debug("Running shutdown procedures.")


app = FastAPI(debug=True, reload=True, lifespan=lifespan)

# Resolve CORS middleware issues
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health_check")
async def health_check() -> str:
    """
    Simple health check, can ping whenever you want to check if backend is healthy
    Returns: "OK" if everything is OK
    """
    return "OK"
