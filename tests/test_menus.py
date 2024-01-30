async def test_get_empty_menus(server, test_client):
    response = await test_client.get("/menus")
    assert response.status_code == 200
    assert response.json() == []


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

    store.update(menu=response_json)


async def test_get_menu_id(server, test_client, store):
    response = await test_client.get(f"/menus/{store['menu']['id']}")
    assert response.status_code == 200
    assert response.json() == store["menu"]


async def test_get_menus(server, test_client, store):
    response = await test_client.get("/menus")
    assert response.status_code == 200
    assert response.json() == [store["menu"]]


async def test_patch_menu(server, test_client, store):
    data = {
        "title": "My updated menu 1",
        "description": "My updated description for menu 1"
    }
    response = await test_client.patch(f"/menus/{store['menu']['id']}", json=data)
    response_json = response.json()
    assert response.status_code == 200
    store["menu"]["title"] = data["title"]
    store["menu"]["description"] = data["description"]
    assert response_json == store["menu"]


async def test_get_menu_id_after_patch(server, test_client, store):
    response = await test_client.get(f"/menus/{store['menu']['id']}")
    assert response.status_code == 200
    assert response.json() == store['menu']


async def test_get_menus_after_patch(server, test_client, store):
    response = await test_client.get("/menus")
    assert response.status_code == 200
    assert response.json() == [store["menu"]]


async def test_delete_menu(server, test_client, store):
    response = await test_client.delete(f"/menus/{store['menu']['id']}")
    assert response.status_code == 200


async def test_get_menu_id_after_delete(server, test_client, store):
    response = await test_client.get(f"/menus/{store['menu']['id']}")
    assert response.status_code == 404
    store.clear()


async def test_get_menus_after_delete(server, test_client):
    response = await test_client.get("/menus")
    assert response.status_code == 200
    assert response.json() == []
