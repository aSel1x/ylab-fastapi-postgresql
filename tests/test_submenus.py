from typing import Any

from httpx import AsyncClient

from app.api.api_v1.endpoints.menus import delete_menu_id, post_menu
from app.api.api_v1.endpoints.submenus import (
    delete_submenu_id,
    get_submenu_id,
    get_submenus,
    patch_submenu_id,
    post_submenu,
)

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
    assert response_json.get('id') is not None
    assert response_json.get('title') == data['title']
    assert response_json.get('description') == data['description']

    store.update(menu_id=response_json['id'])


async def test_get_empty_submenus(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.get(
        reverse(
            get_submenus,
            menu_id=store['menu_id']
        )
    )
    assert response.status_code == 200
    assert response.json() == []


async def test_post_submenu(test_client: AsyncClient, store: dict[str, Any]) -> None:
    data = {
        'title': 'My submenu 1',
        'description': 'My description for submenu 1'
    }
    response = await test_client.post(
        reverse(
            post_submenu,
            menu_id=store['menu_id']
        ),
        json=data
    )
    response_json = response.json()
    assert response.status_code == 201
    assert response_json.get('id') is not None
    assert response_json.get('title') == data['title']
    assert response_json.get('description') == data['description']

    store.update(submenu=response_json)


async def test_get_submenu_id(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.get(
        reverse(
            get_submenu_id,
            menu_id=store['menu_id'],
            submenu_id=store['submenu']['id']
        )
    )
    assert response.status_code == 200
    assert response.json() == store['submenu']


async def test_get_submenus(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.get(
        reverse(
            get_submenus,
            menu_id=store['menu_id'],
        )
    )
    assert response.status_code == 200
    assert response.json() == [store['submenu']]


async def test_patch_submenu(test_client: AsyncClient, store: dict[str, Any]) -> None:
    data = {
        'title': 'My updated submenu 1',
        'description': 'My updated description for submenu 1'
    }
    response = await test_client.patch(
        reverse(
            patch_submenu_id,
            menu_id=store['menu_id'],
            submenu_id=store['submenu']['id']
        ),
        json=data
    )
    response_json = response.json()
    assert response.status_code == 200
    store['submenu']['title'] = data['title']
    store['submenu']['description'] = data['description']
    assert response_json == store['submenu']


async def test_get_submenu_id_after_patch(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.get(
        reverse(
            get_submenu_id,
            menu_id=store['menu_id'],
            submenu_id=store['submenu']['id']
        )
    )
    assert response.status_code == 200
    assert response.json() == store['submenu']


async def test_get_submenus_after_patch(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.get(
        reverse(
            get_submenus,
            menu_id=store['menu_id'],
        )
    )
    assert response.status_code == 200
    assert response.json() == [store['submenu']]


async def test_delete_submenu(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.delete(
        reverse(
            delete_submenu_id,
            menu_id=store['menu_id'],
            submenu_id=store['submenu']['id']
        )
    )
    assert response.status_code == 200


async def test_get_submenu_id_after_delete(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.get(
        reverse(
            get_submenu_id,
            menu_id=store['menu_id'],
            submenu_id=store['submenu']['id']
        )
    )
    assert response.status_code == 404


async def test_get_submenus_after_delete(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.get(
        reverse(
            get_submenus,
            menu_id=store['menu_id'],
        )
    )
    assert response.status_code == 200
    assert response.json() == []


async def test_delete_menu(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.delete(
        reverse(
            delete_menu_id,
            menu_id=store['menu_id'],
        )
    )
    assert response.status_code == 200
    store.clear()
