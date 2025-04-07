# backend/src/app.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import engine, check_db_connection, Base
from src.routes.api import router
import logging
from concurrent.futures import ThreadPoolExecutor
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a thread pool executor
executor = ThreadPoolExecutor(max_workers=3)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Starting up the application...")
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(executor, check_db_connection)
        # Create all tables defined in models
        Base.metadata.create_all(bind=engine)
        logger.info("Database schema initialized successfully")
    except Exception as e:
        logger.error(f"Database connection or schema initialization failed: {e}")
        raise

    yield  # Application runs here

    # Shutdown logic
    logger.info("Shutting down the application...")
    executor.shutdown()

# Initialize FastAPI app with lifespan handler (only once)
app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)