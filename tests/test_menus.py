from typing import Any

from httpx import AsyncClient

from app.api.api_v1.endpoints.menus import (
    delete_menu_id,
    get_menu_id,
    get_menus,
    patch_menu_id,
    post_menu,
)

from .conftest import reverse


async def test_get_empty_menus(test_client: AsyncClient) -> None:
    response = await test_client.get(
        reverse(get_menus)
    )
    assert response.status_code == 200
    assert response.json() == []


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

    store.update(menu=response_json)


async def test_get_menu_id(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.get(
        reverse(
            get_menu_id,
            menu_id=store['menu']['id']
        )
    )
    assert response.status_code == 200
    assert response.json() == store['menu']


async def test_get_menus(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.get(
        reverse(get_menus)
    )
    assert response.status_code == 200
    assert response.json() == [store['menu']]


async def test_patch_menu(test_client: AsyncClient, store: dict[str, Any]) -> None:
    data = {
        'title': 'My updated menu 1',
        'description': 'My updated description for menu 1'
    }
    response = await test_client.patch(
        reverse(
            patch_menu_id,
            menu_id=store['menu']['id']
        ),
        json=data
    )
    response_json = response.json()
    assert response.status_code == 200
    store['menu']['title'] = data['title']
    store['menu']['description'] = data['description']
    assert response_json == store['menu']


async def test_get_menu_id_after_patch(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.get(
        reverse(
            get_menu_id,
            menu_id=store['menu']['id']
        )
    )
    assert response.status_code == 200
    assert response.json() == store['menu']


async def test_get_menus_after_patch(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.get(
        reverse(get_menus)
    )
    assert response.status_code == 200
    assert response.json() == [store['menu']]


async def test_delete_menu(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.delete(
        reverse(
            delete_menu_id,
            menu_id=store['menu']['id']
        )
    )
    assert response.status_code == 200


async def test_get_menu_id_after_delete(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.get(
        reverse(
            get_menu_id,
            menu_id=store['menu']['id']
        )
    )
    assert response.status_code == 404
    store.clear()


async def test_get_menus_after_delete(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.get(
        reverse(get_menus)
    )
    assert response.status_code == 200
    assert response.json() == []
