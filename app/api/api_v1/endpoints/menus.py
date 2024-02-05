from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api import depends
from app.schemas.menu import MenuScheme, MenuSchemeAdd
from app.services import Services

router = APIRouter()


@router.get('', response_model=list[MenuScheme])
async def get(service: Services = Depends(depends.get_services)):
    menus = await service.menu.get_all()
    return menus


@router.post('', response_model=MenuScheme, status_code=status.HTTP_201_CREATED)
async def post(menu: MenuSchemeAdd, service: Services = Depends(depends.get_services)):
    new_menu = await service.menu.new(
        title=menu.title,
        description=menu.description,
    )
    return new_menu


@router.get('/{menu_id}', response_model=MenuScheme)
async def get_id(menu_id: int, service: Services = Depends(depends.get_services)):
    menu = await service.menu.get_id(menu_id)
    if menu is not None:
        return menu
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')


@router.patch('/{menu_id}', response_model=MenuScheme)
async def patch_id(menu_id: int, menu: MenuSchemeAdd, service: Services = Depends(depends.get_services)):
    await service.menu.update(menu_id, menu)
    updated_menu = await service.menu.get_id(menu_id)
    return updated_menu


@router.delete('/{menu_id}', status_code=status.HTTP_200_OK)
async def delete_id(menu_id: int, service: Services = Depends(depends.get_services)):
    await service.menu.delete(menu_id)
