from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from app.api import depends
from app.schemas.menu import MenuNotFound, MenuScheme, MenuSchemeAdd
from app.services import Services

router = APIRouter()

responses = {
    404: {
        'description': 'Not found',
        'model': MenuNotFound
    }
}


@router.get('', response_model=list[MenuScheme])
async def get_menus(service: Services = Depends(depends.get_services)):
    return await service.menu.get_all()


@router.post('', response_model=MenuScheme, status_code=status.HTTP_201_CREATED)
async def post_menu(menu: MenuSchemeAdd, service: Services = Depends(depends.get_services)):
    return await service.menu.new(
        title=menu.title,
        description=menu.description,
    )


@router.get('/{menu_id}', response_model=MenuScheme, responses={**responses})
async def get_menu_id(menu_id: int, service: Services = Depends(depends.get_services)):
    menu = await service.menu.get_id(menu_id)
    if menu is not None:
        return menu
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')


@router.patch('/{menu_id}', response_model=MenuScheme)
async def patch_menu_id(menu_id: int, menu: MenuSchemeAdd, service: Services = Depends(depends.get_services)):
    await service.menu.update(menu_id, menu)
    return await service.menu.get_id(menu_id)


@router.delete('/{menu_id}', status_code=status.HTTP_200_OK)
async def delete_menu_id(menu_id: int, service: Services = Depends(depends.get_services)):
    await service.menu.delete(menu_id)
