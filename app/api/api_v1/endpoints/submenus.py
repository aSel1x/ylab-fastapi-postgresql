from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import DBAPIError

from app.api import depends
from app.database.models import Submenu
from app.schemas.submenu import SubmenuNotFound, SubmenuScheme, SubmenuSchemeAdd
from app.services import Services

router = APIRouter()

responses = {
    404: {
        'description': 'Not found',
        'model': SubmenuNotFound
    }
}


@router.get('', response_model=list[SubmenuScheme])
async def get_submenus(
        menu_id: int,
        service: Services = Depends(depends.get_services)
) -> Sequence[SubmenuScheme | Submenu]:
    return await service.submenu.get_by_menu_id(menu_id)


@router.post('', response_model=SubmenuScheme, status_code=status.HTTP_201_CREATED)
async def post_submenu(
        menu_id: int,
        submenu: SubmenuSchemeAdd,
        service: Services = Depends(depends.get_services)
) -> SubmenuScheme | Submenu:
    return await service.submenu.new(
        title=submenu.title,
        description=submenu.description,
        menu_id=menu_id,
    )


@router.get('/{submenu_id}', response_model=SubmenuScheme, responses={**responses})
async def get_submenu_id(
        submenu_id: int,
        service: Services = Depends(depends.get_services)
) -> SubmenuScheme | Submenu | HTTPException:
    if submenu := await service.submenu.get_id(submenu_id):
        return submenu
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')


@router.patch('/{submenu_id}', response_model=SubmenuScheme)
async def patch_submenu_id(
        submenu_id: int,
        submenu: SubmenuSchemeAdd,
        service: Services = Depends(depends.get_services)
) -> SubmenuScheme | Submenu | HTTPException:
    try:
        return await service.submenu.update(submenu_id, submenu)
    except DBAPIError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')


@router.delete('/{submenu_id}', status_code=status.HTTP_200_OK)
async def delete_submenu_id(submenu_id: int, service: Services = Depends(depends.get_services)) -> None:
    await service.submenu.delete(submenu_id)
