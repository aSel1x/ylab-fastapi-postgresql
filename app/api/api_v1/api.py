"""
Module for connect all endpoints
"""

from fastapi import APIRouter

from app.api.api_v1.endpoints import dishes, menus, submenus

api_router = APIRouter()
api_router.include_router(
    menus.router,
    prefix='/menus',
    tags=['menus'],
)
api_router.include_router(
    submenus.router,
    prefix='/menus/{menu_id}/submenus',
    tags=['submenus']
)
api_router.include_router(
    dishes.router,
    prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['dishes']
)
