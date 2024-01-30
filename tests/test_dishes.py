async def test_post_menu(server, test_client, store):
    data = {
        "title": "My menu 1",
        "description": "My description for menu 1"
    }
    response = await test_client.post("/menus", json=data)
    response_json = response.json()
    assert response.status_code == 201
    assert response_json.get("id") is not None
    assert response_json.get("title") == data["title"]
    assert response_json.get("description") == data["description"]

    store.update(menu_id=response_json["id"])


async def test_post_submenu(server, test_client, store):
    data = {
        "title": "My submenu 1",
        "description": "My description for submenu 1"
    }
    response = await test_client.post(f"/menus/{store['menu_id']}/submenus", json=data)
    response_json = response.json()
    assert response.status_code == 201
    assert response_json.get("id") is not None
    assert response_json.get("title") == data["title"]
    assert response_json.get("description") == data["description"]

    store.update(submenu_id=response_json['id'])


async def test_get_empty_dishes(server, test_client, store):
    response = await test_client.get(f"/menus/{store['menu_id']}/submenus/{store['submenu_id']}/dishes")
    assert response.status_code == 200
    assert response.json() == []


async def test_post_dish(server, test_client, store):
    data = {
        "title": "My dish 1",
        "description": "My description for dish 1",
        "price": "15.00"
    }
    response = await test_client.post(f"/menus/{store['menu_id']}/submenus/{store['submenu_id']}/dishes", json=data)
    response_json = response.json()
    assert response.status_code == 201
    assert response_json.get("id") is not None
    assert response_json.get("title") == data["title"]
    assert response_json.get("description") == data["description"]

    store.update(dish=response_json)


async def test_get_dish_id(server, test_client, store):
    response = await test_client.get(f"/menus/{store['menu_id']}/submenus/{store['submenu_id']}/dishes/{store['dish']['id']}")
    assert response.status_code == 200
    assert response.json() == store['dish']


async def test_get_dishes(server, test_client, store):
    response = await test_client.get(f"/menus/{store['menu_id']}/submenus/{store['submenu_id']}/dishes")
    assert response.status_code == 200
    assert response.json() == [store["dish"]]


async def test_patch_dish(server, test_client, store):
    data = {
        "title": "My updated dish 1",
        "description": "My updated description for dish 1",
        "price": "30.00"
    }
    response = await test_client.patch(f"/menus/{store['menu_id']}/submenus/{store['submenu_id']}/dishes/{store['dish']['id']}", json=data)
    response_json = response.json()
    assert response.status_code == 200
    store["dish"]["title"] = data["title"]
    store["dish"]["description"] = data["description"]
    store["dish"]["price"] = data["price"]
    assert response_json == store["dish"]


async def test_get_dish_id_after_patch(server, test_client, store):
    response = await test_client.get(f"/menus/{store['menu_id']}/submenus/{store['submenu_id']}/dishes/{store['dish']['id']}")
    assert response.status_code == 200
    assert response.json() == store['dish']


async def test_get_dishes_after_patch(server, test_client, store):
    response = await test_client.get(f"/menus/{store['menu_id']}/submenus/{store['submenu_id']}/dishes")
    assert response.status_code == 200
    assert response.json() == [store["dish"]]


async def test_delete_dish(server, test_client, store):
    response = await test_client.delete(f"/menus/{store['menu_id']}/submenus/{store['submenu_id']}/dishes/{store['dish']['id']}")
    assert response.status_code == 200


async def test_get_dish_id_after_delete(server, test_client, store):
    response = await test_client.get(f"/menus/{store['menu_id']}/submenus/{store['submenu_id']}/dishes/{store['dish']['id']}")
    assert response.status_code == 404


async def test_get_dishes_after_delete(server, test_client, store):
    response = await test_client.get(f"/menus/{store['menu_id']}/submenus/{store['submenu_id']}/dishes")
    assert response.status_code == 200
    assert response.json() == []


async def test_delete_menu(server, test_client, store):
    response = await test_client.delete(f"/menus/{store['menu_id']}")
    assert response.status_code == 200
    store.clear()
