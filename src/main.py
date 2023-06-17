from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import admin, address, auth, todo, user

app = FastAPI(title="Todo")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=address.router)
app.include_router(router=admin.router)
app.include_router(router=auth.router)
app.include_router(router=todo.router)
app.include_router(router=user.router)
