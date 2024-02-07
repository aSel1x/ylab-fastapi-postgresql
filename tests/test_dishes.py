from app.api.api_v1.endpoints.dishes import (
    delete_dish_id,
    get_dish_id,
    get_dishes,
    patch_dish_id,
    post_dish,
)
from app.api.api_v1.endpoints.menus import delete_menu_id, post_menu
from app.api.api_v1.endpoints.submenus import post_submenu

from .conftest import reverse


async def test_post_menu(test_client, store):
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


async def test_post_submenu(test_client, store):
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

    store.update(submenu_id=response_json['id'])


async def test_get_empty_dishes(test_client, store):
    response = await test_client.get(
        reverse(
            get_dishes,
            menu_id=store['menu_id'],
            submenu_id=store['submenu_id']
        )
    )
    assert response.status_code == 200
    assert response.json() == []


async def test_post_dish(test_client, store):
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
    assert response_json.get('id') is not None
    assert response_json.get('title') == data['title']
    assert response_json.get('description') == data['description']

    store.update(dish=response_json)


async def test_get_dish_id(test_client, store):
    response = await test_client.get(
        reverse(
            get_dish_id,
            menu_id=store['menu_id'],
            submenu_id=store['submenu_id'],
            dish_id=store['dish']['id']
        )
    )
    assert response.status_code == 200
    assert response.json() == store['dish']


async def test_get_dishes(test_client, store):
    response = await test_client.get(
        reverse(
            get_dishes,
            menu_id=store['menu_id'],
            submenu_id=store['submenu_id'],
        )
    )
    assert response.status_code == 200
    assert response.json() == [store['dish']]


async def test_patch_dish(test_client, store):
    data = {
        'title': 'My updated dish 1',
        'description': 'My updated description for dish 1',
        'price': '30.00'
    }
    response = await test_client.patch(
        reverse(
            patch_dish_id,
            menu_id=store['menu_id'],
            submenu_id=store['submenu_id'],
            dish_id=store['dish']['id']
        ),
        json=data
    )
    response_json = response.json()
    assert response.status_code == 200
    store['dish']['title'] = data['title']
    store['dish']['description'] = data['description']
    store['dish']['price'] = data['price']
    assert response_json == store['dish']


async def test_get_dish_id_after_patch(test_client, store):
    response = await test_client.get(
        reverse(
            get_dish_id,
            menu_id=store['menu_id'],
            submenu_id=store['submenu_id'],
            dish_id=store['dish']['id']
        )
    )
    assert response.status_code == 200
    assert response.json() == store['dish']


async def test_get_dishes_after_patch(test_client, store):
    response = await test_client.get(
        reverse(
            get_dishes,
            menu_id=store['menu_id'],
            submenu_id=store['submenu_id'],
        )
    )
    assert response.status_code == 200
    assert response.json() == [store['dish']]


async def test_delete_dish(test_client, store):
    response = await test_client.delete(
        reverse(
            delete_dish_id,
            menu_id=store['menu_id'],
            submenu_id=store['submenu_id'],
            dish_id=store['dish']['id']
        )
    )
    assert response.status_code == 200


async def test_get_dish_id_after_delete(test_client, store):
    response = await test_client.get(
        reverse(
            get_dish_id,
            menu_id=store['menu_id'],
            submenu_id=store['submenu_id'],
            dish_id=store['dish']['id']
        )
    )
    assert response.status_code == 404


async def test_get_dishes_after_delete(test_client, store):
    response = await test_client.get(
        reverse(
            get_dishes,
            menu_id=store['menu_id'],
            submenu_id=store['submenu_id'],
        )
    )
    assert response.status_code == 200
    assert response.json() == []


async def test_delete_menu(test_client, store):
    response = await test_client.delete(
        reverse(
            delete_menu_id,
            menu_id=store['menu_id'],
        )
    )
    assert response.status_code == 200
    store.clear()
