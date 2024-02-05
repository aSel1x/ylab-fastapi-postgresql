async def test_post_menu(test_client, store):
    data = {
        'title': 'My menu 1',
        'description': 'My description for menu 1'
    }
    response = await test_client.post('/menus', json=data)
    response_json = response.json()
    assert response.status_code == 201
    assert response_json.get('id') is not None
    assert response_json.get('title') == data['title']
    assert response_json.get('description') == data['description']

    store.update(menu_id=response_json['id'])


async def test_get_empty_submenus(test_client, store):
    response = await test_client.get(f"/menus/{store['menu_id']}/submenus")
    assert response.status_code == 200
    assert response.json() == []


async def test_post_submenu(test_client, store):
    data = {
        'title': 'My submenu 1',
        'description': 'My description for submenu 1'
    }
    response = await test_client.post(f"/menus/{store['menu_id']}/submenus", json=data)
    response_json = response.json()
    assert response.status_code == 201
    assert response_json.get('id') is not None
    assert response_json.get('title') == data['title']
    assert response_json.get('description') == data['description']

    store.update(submenu=response_json)


async def test_get_submenu_id(test_client, store):
    response = await test_client.get(f"/menus/{store['menu_id']}/submenus/{store['submenu']['id']}")
    assert response.status_code == 200
    assert response.json() == store['submenu']


async def test_get_submenus(test_client, store):
    response = await test_client.get(f"/menus/{store['menu_id']}/submenus")
    assert response.status_code == 200
    assert response.json() == [store['submenu']]


async def test_patch_submenu(test_client, store):
    data = {
        'title': 'My updated submenu 1',
        'description': 'My updated description for submenu 1'
    }
    response = await test_client.patch(f"/menus/{store['menu_id']}/submenus/{store['submenu']['id']}", json=data)
    response_json = response.json()
    assert response.status_code == 200
    store['submenu']['title'] = data['title']
    store['submenu']['description'] = data['description']
    assert response_json == store['submenu']


async def test_get_submenu_id_after_patch(test_client, store):
    response = await test_client.get(f"/menus/{store['menu_id']}/submenus/{store['submenu']['id']}")
    assert response.status_code == 200
    assert response.json() == store['submenu']


async def test_get_submenus_after_patch(test_client, store):
    response = await test_client.get(f"/menus/{store['menu_id']}/submenus")
    assert response.status_code == 200
    assert response.json() == [store['submenu']]


async def test_delete_submenu(test_client, store):
    response = await test_client.delete(f"/menus/{store['menu_id']}/submenus/{store['submenu']['id']}")
    assert response.status_code == 200


async def test_get_submenu_id_after_delete(test_client, store):
    response = await test_client.get(f"/menus/{store['menu_id']}/submenus/{store['submenu']['id']}")
    assert response.status_code == 404


async def test_get_submenus_after_delete(test_client, store):
    response = await test_client.get(f"/menus/{store['menu_id']}/submenus")
    assert response.status_code == 200
    assert response.json() == []


async def test_delete_menu(test_client, store):
    response = await test_client.delete(f"/menus/{store['menu_id']}")
    assert response.status_code == 200
    store.clear()
