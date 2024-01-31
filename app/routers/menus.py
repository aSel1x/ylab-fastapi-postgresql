from sqlalchemy.orm import joinedload

from app.data.config import BASE_URL
from app.db.database import DataBase
from app.db.database_orm import get_async_session
from app.db.models import MenuModel, SubMenuModel, DishModel

from app.db.models_orm import (
    MenusORM,
    SubmenusORM,
    DishesORM
)

from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, func

menus = APIRouter()
db = DataBase()
base_url = BASE_URL + "/menus"


@menus.get(base_url)
async def menus_get():
    data = await db.menus.get_all()
    return data


@menus.post(base_url, status_code=status.HTTP_201_CREATED)
async def menus_post(menu_model: MenuModel):
    menu_model = await db.menus.insert(menu_model)
    return menu_model


@menus.get(base_url + "/{_id}")
async def menus_get_id(_id: int, session: AsyncSession = Depends(get_async_session)):
    query = (
        select(MenusORM)
        .options(
            joinedload(MenusORM.submenus).options(
                joinedload(SubmenusORM.dishes)
            )
        )
        .where(MenusORM.id == _id)
    )
    cursor = await session.execute(query)
    data = cursor.scalars().first()

    if data is not None:
        data = {
            **data.dict(),
            "submenus_count": len(data.submenus),
            "dishes_count": sum(len(submenu.dishes) for submenu in data.submenus)
        }
        return data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")


@menus.patch(base_url + "/{_id}")
async def menus_patch_id(_id: int, menu_model: MenuModel):
    menu_model.id = _id
    await db.menus.update(menu_model)
    menu_model = await db.menus.get_id(menu_model.id)
    return menu_model


@menus.delete(base_url + "/{_id}")
async def menus_delete_id(_id: int):
    await db.menus.delete(_id)
    return status.HTTP_200_OK
