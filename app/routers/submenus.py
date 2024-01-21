from data.config import BASE_URL
from db.database import DataBase
from db.models import SubMenuModel
from fastapi import APIRouter, status

submenus = APIRouter()
db = DataBase()
base_url = BASE_URL + "/menus/{menu_id}/submenus"


@submenus.get(base_url)
async def submenus_get(menu_id: int):
    data = await db.submenus.get_all(menu_id)
    return data


@submenus.post(base_url)
async def submenus_post(menu_id: int, submenu_model: SubMenuModel):
    submenu_model.menu_id = menu_id
    await db.submenus.insert(submenu_model)
    return submenu_model


@submenus.get(base_url+"/{_id}")
async def submenus_get_id(_id: int):
    data = await db.submenus.get_id(_id)
    return data


@submenus.patch(base_url+"/{_id}")
async def submenus_patch_id(menu_id: int, _id: int, submenu_model: SubMenuModel):
    submenu_model.menu_id = menu_id
    submenu_model.id = _id
    await db.submenus.update(submenu_model)
    return submenu_model


@submenus.delete(base_url+"/{_id}")
async def submenus_delete_id(_id: int):
    await db.submenus.delete(_id)
    return status.HTTP_200_OK
