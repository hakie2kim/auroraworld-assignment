from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.links import router as link_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(link_router)
