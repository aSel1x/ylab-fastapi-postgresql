from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api import depends
from app.schemas.submenu import SubmenuScheme, SubmenuSchemeAdd
from app.services import Services

router = APIRouter()


@router.get('', response_model=list[SubmenuScheme])
async def get(menu_id: int, service: Services = Depends(depends.get_services)):
    submenus = await service.submenu.get_by_menu_id(menu_id)
    return submenus


@router.post('', response_model=SubmenuScheme, status_code=status.HTTP_201_CREATED)
async def post(menu_id: int, submenu: SubmenuSchemeAdd, service: Services = Depends(depends.get_services)):
    new_submenu = await service.submenu.new(
        title=submenu.title,
        description=submenu.description,
        menu_id=menu_id,
    )
    return new_submenu


@router.get('/{submenu_id}', response_model=SubmenuScheme)
async def get_id(menu_id: int, submenu_id: int, service: Services = Depends(depends.get_services)):
    submenu = await service.submenu.get_id(submenu_id)
    if submenu is not None:
        return submenu
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')


@router.patch('/{submenu_id}', response_model=SubmenuScheme)
async def patch_id(menu_id: int, submenu_id: int, submenu: SubmenuSchemeAdd, service: Services = Depends(depends.get_services)):
    await service.submenu.update(submenu_id, submenu)
    updated_submenu = await service.submenu.get_id(submenu_id)
    return updated_submenu


@router.delete('/{submenu_id}', status_code=status.HTTP_200_OK)
async def delete_id(menu_id: int, submenu_id: int, service: Services = Depends(depends.get_services)):
    await service.submenu.delete(submenu_id)
