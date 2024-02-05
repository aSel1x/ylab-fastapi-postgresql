import random


async def test_post_menu_and_zero_counts(test_client, cascades):
    data = {
        'title': f'My menu 1',
        'description': f'My description for menu 1'
    }
    response = await test_client.post('/menus', json=data)
    response_json = response.json()
    assert response.status_code == 201
    assert response_json.get('id') is not None
    assert response_json.get('submenus_count') == 0
    assert response_json.get('dishes_count') == 0

    menu_id = int(response_json['id'])
    cascades[menu_id] = {}


async def test_post_submenus_and_zero_dishes(test_client, cascades):
    for menu_id in cascades:
        for x in range(1, 4):
            data = {
                'title': f'My submenu {x}',
                'description': f'My description for submenu {x}'
            }
            response = await test_client.post(f'/menus/{menu_id}/submenus', json=data)
            response_json = response.json()
            assert response.status_code == 201
            assert response_json.get('id') is not None
            assert response_json.get('dishes_count') == 0

            submenu_id = int(response_json['id'])
            cascades[menu_id][submenu_id] = []


async def test_post_dishes(test_client, cascades):
    for menu_id in cascades:
        for submenu_id in cascades[menu_id]:
            for x in range(1, random.randint(3, 10)):
                data = {
                    'title': f'My dish {x}',
                    'description': f'My description for dish {x}',
                    'price': '10.00'
                }
                response = await test_client.post(f'/menus/{menu_id}/submenus/{submenu_id}/dishes', json=data)
                response_json = response.json()
                assert response.status_code == 201
                assert response_json.get('id') is not None

                dish_id = int(response_json['id'])
                cascades[menu_id][submenu_id].append(dish_id)


async def test_menu_counts(test_client, cascades):

    for menu_id in cascades:
        dishes_count = 0
        for submenu_id in cascades[menu_id]:
            dishes_count += len(cascades[menu_id][submenu_id])

        response = await test_client.get(f'/menus/{menu_id}')
        response_json = response.json()
        assert response.status_code == 200
        assert response_json.get('submenus_count') == len(cascades[menu_id])
        assert response_json.get('dishes_count') == dishes_count


async def test_submenu_counts(test_client, cascades):
    for menu_id in cascades:
        for submenu_id in cascades[menu_id]:
            response = await test_client.get(f'/menus/{menu_id}/submenus/{submenu_id}')
            response_json = response.json()
            assert response.status_code == 200
            assert response_json.get('dishes_count') == len(cascades[menu_id][submenu_id])


async def test_delete_random_submenu(test_client, cascades):
    for menu_id in cascades:
        submenu_id = random.choice(list(cascades[menu_id].keys()))
        response = await test_client.delete(f'/menus/{menu_id}/submenus/{submenu_id}')
        assert response.status_code == 200
        cascades[menu_id].pop(submenu_id)


async def test_menu_counts_after_submenu_delete(test_client, cascades):
    for menu_id in cascades:
        dishes_count = 0
        for submenu_id in cascades[menu_id]:
            dishes_count += len(cascades[menu_id][submenu_id])

        response = await test_client.get(f'/menus/{menu_id}')
        response_json = response.json()
        assert response.status_code == 200
        assert response_json.get('submenus_count') == len(cascades[menu_id])
        assert response_json.get('dishes_count') == dishes_count


async def test_random_dishes_delete(test_client, cascades):
    for menu_id in cascades:
        for submenu_id in cascades[menu_id]:
            dishes_ids = random.choices(cascades[menu_id][submenu_id], k=2)
            for dish_id in dishes_ids:
                response = await test_client.delete(f'/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
                assert response.status_code == 200
                try:
                    cascades[menu_id][submenu_id].remove(dish_id)
                except ValueError:
                    #  Потому что dishes_ids иногда возвращает 2 одинаковых числа
                    pass


async def test_menu_counts_after_random_dishes_delete(test_client, cascades):
    for menu_id in cascades:
        dishes_count = 0
        for submenu_id in cascades[menu_id]:
            dishes_count += len(cascades[menu_id][submenu_id])

        response = await test_client.get(f'/menus/{menu_id}')
        response_json = response.json()
        assert response.status_code == 200
        assert response_json.get('submenus_count') == len(cascades[menu_id])
        assert response_json.get('dishes_count') == dishes_count


async def test_submenu_counts_after_random_dishes_delete(test_client, cascades):
    for menu_id in cascades:
        for submenu_id in cascades[menu_id]:
            response = await test_client.get(f'/menus/{menu_id}/submenus/{submenu_id}')
            response_json = response.json()
            assert response.status_code == 200
            assert response_json.get('dishes_count') == len(cascades[menu_id][submenu_id])


async def test_delete_menu(test_client, cascades):
    for menu_id in cascades:
        response = await test_client.delete(f'/menus/{menu_id}')
        assert response.status_code == 200
    cascades.clear()
