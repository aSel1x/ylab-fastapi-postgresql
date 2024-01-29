import asyncio
import uvicorn

from app.db.database import DataBase

from app.routers.menus import menus
from app.routers.submenus import submenus
from app.routers.dishes import dishes

from fastapi import FastAPI

db = DataBase()
app = FastAPI()
app.include_router(menus)
app.include_router(submenus)
app.include_router(dishes)


if __name__ == "__main__":
    asyncio.run(db.connection.setup())
    uvicorn.run(app, host="0.0.0.0")
