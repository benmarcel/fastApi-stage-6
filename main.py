from dotenv import load_dotenv
load_dotenv()
from contextlib import asynccontextmanager
from fastapi import FastAPI
from db import init_db
from controller.auth import user_router, admin_router
from controller.product import router as product_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(product_router)