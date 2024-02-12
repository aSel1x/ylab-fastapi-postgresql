from typing import Any

from httpx import AsyncClient

from app.api.api_v1.endpoints.dishes import post_dish
from app.api.api_v1.endpoints.extra import get_all
from app.api.api_v1.endpoints.menus import delete_menu_id, post_menu
from app.api.api_v1.endpoints.submenus import post_submenu

from .conftest import reverse


async def test_post_menu(test_client: AsyncClient, store: dict[str, Any]) -> None:
    data = {
        'title': 'My menu 1',
        'description': 'My description for menu 1'
    }
    response = await test_client.post(
        reverse(post_menu),
        json=data
    )
    response_json = response.json()
    assert response.status_code == 201

    store.update(menus=[response_json])


async def test_post_submenu(test_client: AsyncClient, store: dict[str, Any]) -> None:
    menu = store['menus'][0]
    data = {
        'title': 'My submenu 1',
        'description': 'My description for submenu 1'
    }
    response = await test_client.post(
        reverse(
            post_submenu,
            menu_id=menu['id']
        ),
        json=data
    )
    response_json = response.json()
    assert response.status_code == 201

    menu['submenus_count'] += 1
    menu.update(submenus=[response_json])


async def test_post_dish(test_client: AsyncClient, store: dict[str, Any]) -> None:
    menu = store['menus'][0]
    submenu = menu['submenus'][0]
    data = {
        'title': 'My dish 1',
        'description': 'My description for dish 1',
        'price': '15.00'
    }
    response = await test_client.post(
        reverse(
            post_dish,
            menu_id=menu['id'],
            submenu_id=submenu['id']
        ),
        json=data
    )
    response_json = response.json()
    assert response.status_code == 201
    assert response_json.get('id') is not None
    assert response_json.get('title') == data['title']
    assert response_json.get('description') == data['description']

    menu['dishes_count'] += 1
    submenu['dishes_count'] += 1
    submenu.update(dishes=[response_json])


async def test_get_all(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.get(
        reverse(get_all)
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json == store


async def test_delete_menu(test_client: AsyncClient, store: dict[str, Any]) -> None:
    menu = store['menus'][0]
    response = await test_client.delete(
        reverse(
            delete_menu_id,
            menu_id=menu['id'],
        )
    )
    assert response.status_code == 200
    store.clear()
