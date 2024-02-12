from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import DBAPIError

from app.api import depends
from app.schemas.dish import DishNotFound, DishScheme, DishSchemeAdd
from app.services import Services

router = APIRouter()


responses = {
    404: {
        'description': 'Not found',
        'model': DishNotFound
    }
}


@router.get('', response_model=list[DishScheme])
async def get_dishes(submenu_id: int, service: Services = Depends(depends.get_services)):
    return await service.dish.get_by_submenu_id(submenu_id)


@router.post('', response_model=DishScheme, status_code=status.HTTP_201_CREATED)
async def post_dish(submenu_id: int, dish: DishSchemeAdd, service: Services = Depends(depends.get_services)):
    return await service.dish.new(
        title=dish.title,
        description=dish.description,
        price=dish.price,
        submenu_id=submenu_id,
    )


@router.get('/{dish_id}', response_model=DishScheme, responses={**responses})
async def get_dish_id(dish_id: int, service: Services = Depends(depends.get_services)):
    if dish := await service.dish.get_id(dish_id):
        return dish
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')


@router.patch('/{dish_id}', response_model=DishScheme)
async def patch_dish_id(dish_id: int, dish: DishSchemeAdd, service: Services = Depends(depends.get_services)):
    try:
        return await service.dish.update(dish_id, dish)
    except DBAPIError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')


@router.delete('/{dish_id}', status_code=status.HTTP_200_OK)
async def delete_dish_id(dish_id: int, service: Services = Depends(depends.get_services)):
    await service.dish.delete(dish_id)
