from app.data.config import BASE_URL
from app.db.database import DataBase
from app.db.models import DishModel
from fastapi import APIRouter, status, HTTPException

dishes = APIRouter()
db = DataBase()
base_url = BASE_URL + "/menus/{menu_id}/submenus/{submenu_id}/dishes"


@dishes.get(base_url)
async def dishes_get(submenu_id: int):
    data = await db.dishes.get_all(submenu_id)
    return data


@dishes.post(base_url, status_code=status.HTTP_201_CREATED)
async def dishes_post(menu_id: int, submenu_id: int, dishes_model: DishModel):
    dishes_model.submenu_id = submenu_id
    dishes_model = await db.dishes.insert(menu_id, dishes_model)
    return dishes_model


@dishes.get(base_url+"/{_id}")
async def dishes_get_id(_id: int):
    data = await db.dishes.get_id(_id)
    if data is not None:
        return data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")


@dishes.patch(base_url+"/{_id}")
async def dishes_patch_id(submenu_id: int, _id: int, dishes_model: DishModel):
    dishes_model.submenu_id = submenu_id
    dishes_model.id = _id
    await db.dishes.update(dishes_model)
    dishes_model = await db.dishes.get_id(dishes_model.id)
    return dishes_model


@dishes.delete(base_url+"/{_id}")
async def dishes_delete_id(menu_id: int, submenu_id: int, _id: int):
    await db.dishes.delete(menu_id, submenu_id, _id)
    return status.HTTP_200_OK
