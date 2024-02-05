from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api import depends
from app.schemas.dish import DishScheme, DishSchemeAdd
from app.services import Services

router = APIRouter()


@router.get('', response_model=list[DishScheme])
async def get(menu_id, submenu_id: int, service: Services = Depends(depends.get_services)):
    dishes = await service.dish.get_by_submenu_id(submenu_id)
    return dishes


@router.post('', response_model=DishScheme, status_code=status.HTTP_201_CREATED)
async def post(menu_id: int, submenu_id: int, dish: DishSchemeAdd, service: Services = Depends(depends.get_services)):
    new_dish = await service.dish.new(
        title=dish.title,
        description=dish.description,
        price=dish.price,
        submenu_id=submenu_id,
    )
    return new_dish


@router.get('/{dish_id}', response_model=DishScheme)
async def get_id(menu_id: int, submenu_id: int, dish_id: int, service: Services = Depends(depends.get_services)):
    dish = await service.dish.get_id(dish_id)
    if dish is not None:
        return dish
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')


@router.patch('/{dish_id}', response_model=DishScheme)
async def patch_id(menu_id: int, submenu_id: int, dish_id: int, dish: DishSchemeAdd, service: Services = Depends(depends.get_services)):
    await service.dish.update(dish_id, dish)
    updated_dish = await service.dish.get_id(dish_id)
    return updated_dish


@router.delete('/{dish_id}', status_code=status.HTTP_200_OK)
async def dishes_delete_id(menu_id: int, submenu_id: int, dish_id: int, service: Services = Depends(depends.get_services)):
    await service.dish.delete(dish_id)
