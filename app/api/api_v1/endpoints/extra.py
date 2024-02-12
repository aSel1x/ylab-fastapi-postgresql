from fastapi import APIRouter, Depends

from app.api import depends
from app.schemas.extra import ExtraScheme
from app.services import Services

router = APIRouter()


@router.get('/all', response_model=ExtraScheme)
async def get_all(service: Services = Depends(depends.get_services)):
    return ExtraScheme(menus=await service.menu.get_all_extra())
