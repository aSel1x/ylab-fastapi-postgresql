import json
from typing import Any

from httpx import AsyncClient
from redis.client import Redis

from app.api.api_v1.endpoints.dishes import get_dish_id, post_dish
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

    store.update(menu_id=response_json['id'])


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

    store.update(submenu_id=response_json['id'])


async def test_post_dish_and_set_discount(
        test_client: AsyncClient,
        store: dict[str, Any],
        prepare_redis: Redis,
) -> None:
    data = {
        'title': 'My dish 1',
        'description': 'My description for dish 1',
        'price': '15.00'
    }
    response = await test_client.post(
        reverse(
            post_dish,
            menu_id=store['menu_id'],
            submenu_id=store['submenu_id']
        ),
        json=data
    )
    response_json = response.json()
    assert response.status_code == 201

    store.update(dish=response_json)
    prepare_redis.set('dishes_discounts', json.dumps({response_json['id']: 5}))


async def test_get_dish_with_discount(test_client: AsyncClient, store: dict[str, Any], prepare_redis: Redis) -> None:
    response = await test_client.get(
        reverse(
            get_dish_id,
            menu_id=store['menu_id'],
            submenu_id=store['submenu_id'],
            dish_id=store['dish']['id']
        ),
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['price'] == str(15 - (15 * 0.05))
    prepare_redis.delete('dishes_discounts')


async def test_get_dish_without_discount(test_client: AsyncClient, store: dict[str, Any], prepare_redis: Redis) -> None:
    response = await test_client.get(
        reverse(
            get_dish_id,
            menu_id=store['menu_id'],
            submenu_id=store['submenu_id'],
            dish_id=store['dish']['id']
        ),
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['price'] == '15.00'


async def test_delete_menu(test_client: AsyncClient, store: dict[str, Any]) -> None:
    response = await test_client.delete(
        reverse(
            delete_menu_id,
            menu_id=store['menu_id'],
        )
    )
    assert response.status_code == 200
    store.clear()
