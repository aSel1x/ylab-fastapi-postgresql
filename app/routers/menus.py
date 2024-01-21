from data.config import BASE_URL
from db.database import DataBase
from db.models import MenuModel
from fastapi import APIRouter, status

menus = APIRouter()
db = DataBase()
base_url = BASE_URL + "/menus"


@menus.get(base_url)
async def menus_get():
    data = await db.menus.get_all()
    return data


@menus.post(base_url)
async def menus_post(menu_model: MenuModel):
    await db.menus.insert(menu_model)
    return menu_model


@menus.get(base_url+"/{_id}")
async def menus_get_id(_id: int):
    data = await db.menus.get_id(_id)
    return data


@menus.patch(base_url+"/{_id}")
async def menus_patch_id(_id: int, menu_model: MenuModel):
    menu_model.id = _id
    await db.menus.update(menu_model)
    return menu_model


@menus.delete(base_url+"/{_id}")
async def menus_delete_id(_id: int):
    await db.menus.delete(_id)
    return status.HTTP_200_OK
