from fastapi import FastAPI

from src.routers import admin, address, auth, todo, user

app = FastAPI(title="Todo")


app.include_router(router=address.router)
app.include_router(router=admin.router)
app.include_router(router=auth.router)
app.include_router(router=todo.router)
app.include_router(router=user.router)
