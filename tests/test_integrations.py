import random
from tests.conftest import test_client


menus_store = []
submenus_store = []
dishes_store = []

cascades = {}


def search_by_id(_id: int, _list: list):
    _id = str(_id)
    for index, item in enumerate(_list):
        if item["id"] == _id:
            return index
    return None


# Menus operations
async def get_menus(test_client):
    response = await test_client.get("/menus")
    assert response.status_code == 200
    assert response.json() == menus_store


async def get_menu_id(test_client, menu_id: int):
    index = search_by_id(menu_id, menus_store)
    json = menus_store[index]
    response = await test_client.get(f"/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json() == json


async def post_menu(test_client, menu_id: int):
    json = {"title": f"My menu {menu_id}", "description": f"My description for menu {menu_id}]"}
    response = await test_client.post("/menus", json=json)
    json["id"] = str(menu_id)
    json["submenus_count"] = 0
    json["dishes_count"] = 0
    assert response.status_code == 201
    assert response.json() == json
    menus_store.append(json)

    cascades[menu_id] = {}


async def patch_menu(test_client, menu_id: int):
    title = f"My updated menu {menu_id}"
    description = f"My updated description for menu {menu_id}"
    response = await test_client.patch(f"/menus/{menu_id}", json={"title": title, "description": description})
    index = search_by_id(menu_id, menus_store)
    json = menus_store.pop(index)
    json["title"] = title
    json["description"] = description
    assert response.status_code == 200
    assert response.json() == json
    menus_store.insert(index, json)


async def delete_menu_id(test_client, menu_id: int):
    response = await test_client.delete(f"/menus/{menu_id}")
    assert response.status_code == 200

    index = search_by_id(menu_id, menus_store)
    menus_store.pop(index)

    for submenu in cascades[menu_id]:
        submenu_index = search_by_id(submenu, submenus_store)
        submenus_store.pop(submenu_index)
        for dish in cascades[menu_id][submenu]:
            dish_index = search_by_id(dish, dishes_store)
            dishes_store.pop(dish_index)

    cascades.pop(menu_id)


async def get_submenus(test_client, menu_id: int):
    response = await test_client.get(f"/menus/{menu_id}/submenus")
    assert response.status_code == 200
    submenus_list = [item for item in submenus_store if item["menu_id"] == menu_id]
    assert response.json() == submenus_list


async def get_submenu_id(test_client, menu_id: int, submenu_id: int):
    index = search_by_id(submenu_id, submenus_store)
    json = submenus_store[index]
    response = await test_client.get(f"/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert response.json() == json


async def post_submenu(test_client, menu_id: int, submenu_id: int):
    json = {"title": f"My submenu {submenu_id}", "description": f"My description for submenu {submenu_id}"}
    response = await test_client.post(f"/menus/{menu_id}/submenus", json=json)
    json["id"] = str(submenu_id)
    json["dishes_count"] = 0
    json["menu_id"] = menu_id
    assert response.status_code == 201
    assert response.json() == json
    submenus_store.append(json)
    menu_index = search_by_id(menu_id, menus_store)
    menus_store[menu_index]["submenus_count"] += 1

    cascades[menu_id].setdefault(submenu_id, [])


async def patch_submenu(test_client, menu_id: int, submenu_id: int):
    title = f"My updated submenu {submenu_id}"
    description = f"My updated description for submenu {submenu_id}"
    response = await test_client.patch(f"/menus/{menu_id}/submenus/{submenu_id}", json={"title": title, "description": description})
    index = search_by_id(submenu_id, submenus_store)
    json = submenus_store.pop(index)
    json["title"] = title
    json["description"] = description
    assert response.status_code == 200
    assert response.json() == json
    submenus_store.insert(index, json)


async def delete_submenu(test_client, menu_id: int, submenu_id: int):
    response = await test_client.delete(f"/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200

    index = search_by_id(submenu_id, submenus_store)
    submenu_json = submenus_store[index]

    menu_index = search_by_id(menu_id, menus_store)
    menus_store[menu_index]["submenus_count"] -= 1
    menus_store[menu_index]["dishes_count"] -= submenu_json["dishes_count"]

    submenus_store.pop(index)

    for dish in cascades[menu_id][submenu_id]:
        dish_index = search_by_id(dish, dishes_store)
        dishes_store.pop(dish_index)

    cascades[menu_id].pop(submenu_id)


async def get_dishes(test_client, menu_id: int, submenu_id: int):
    response = await test_client.get(f"/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.status_code == 200
    dishes_list = [item for item in dishes_store if item["submenu_id"] == submenu_id]
    assert response.json() == dishes_list


async def get_dish_id(test_client, menu_id: int, submenu_id: int, dish_id: int):
    index = search_by_id(dish_id, dishes_store)
    json = dishes_store[index]
    response = await test_client.get(f"/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200
    assert response.json() == json


async def post_dish(test_client, menu_id: int, submenu_id: int, dish_id: int):
    json = {"title": f"My dish {dish_id}", "description": f"My description for dish {dish_id}", "price": "10.00"}
    response = await test_client.post(f"/menus/{menu_id}/submenus/{submenu_id}/dishes", json=json)

    json["id"] = str(dish_id)
    json["submenu_id"] = submenu_id
    assert response.status_code == 201
    assert response.json() == json
    dishes_store.append(json)

    menu_index = search_by_id(menu_id, menus_store)
    menus_store[menu_index]["dishes_count"] += 1

    submenu_index = search_by_id(submenu_id, submenus_store)
    submenus_store[submenu_index]["dishes_count"] += 1

    cascades[menu_id][submenu_id].append(dish_id)


async def patch_dish(test_client, menu_id: int, submenu_id: int, dish_id: int):
    title = f"My updated dish {dish_id}"
    description = f"My updated description for dish {dish_id}"
    price = "100.00"
    response = await test_client.patch(f"/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", json={"title": title, "description": description, "price": price})
    assert response.status_code == 200
    index = search_by_id(dish_id, dishes_store)
    json = dishes_store.pop(index)
    json["title"] = title
    json["description"] = description
    json["price"] = price
    assert response.json() == json
    dishes_store.insert(index, json)


async def delete_dish(test_client, menu_id: int, submenu_id: int, dish_id: int):
    response = await test_client.delete(f"/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200

    index = search_by_id(dish_id, dishes_store)

    menu_index = search_by_id(menu_id, menus_store)
    menus_store[menu_index]["dishes_count"] -= 1
    submenu_index = search_by_id(submenu_id, submenus_store)
    submenus_store[submenu_index]["dishes_count"] -= 1

    dishes_store.pop(index)

    cascades[menu_id][submenu_id].remove(dish_id)


async def test_posts(test_client, server):
    last_submenu_id = 0
    last_dish_id = 0
    for menu_id in range(1, 3):
        await post_menu(test_client, menu_id)
        for submenu_id in range(1, 3):
            last_submenu_id += 1
            await post_submenu(test_client, menu_id, last_submenu_id)
            for dish_id in range(1, 3):
                last_dish_id += 1
                await post_dish(test_client, menu_id, last_submenu_id, last_dish_id)


async def test_get_all(test_client, server):
    await get_menus(test_client)
    for menu in cascades:
        await get_submenus(test_client, menu)
        for submenu in cascades[menu]:
            await get_dishes(test_client, menu, submenu)


async def test_patch_all(test_client, server):
    for menu in cascades:
        await patch_menu(test_client, menu)
        for submenu in cascades[menu]:
            await patch_submenu(test_client, menu, submenu)
            for dish in cascades[menu][submenu]:
                await patch_dish(test_client, menu, submenu, dish)


async def test_get_by_id(test_client, server):
    menu_id = random.choice(list(cascades.keys()))
    await get_menu_id(test_client, menu_id)

    menu_id = random.choice(list(cascades.keys()))
    submenu_id = random.choice(list(cascades[menu_id]))
    await get_submenu_id(test_client, menu_id, submenu_id)

    menu_id = random.choice(list(cascades.keys()))
    submenu_id = random.choice(list(cascades[menu_id]))
    dish_id = random.choice(cascades[menu_id][submenu_id])
    await get_dish_id(test_client, menu_id, submenu_id, dish_id)


async def test_deletes(test_client, server):
    menu_id = random.choice(list(cascades.keys()))
    await delete_menu_id(test_client, menu_id)

    menu_id = random.choice(list(cascades.keys()))
    submenu_id = random.choice(list(cascades[menu_id]))
    await delete_submenu(test_client, menu_id, submenu_id)

    menu_id = random.choice(list(cascades.keys()))
    submenu_id = random.choice(list(cascades[menu_id]))
    dish_id = random.choice(cascades[menu_id][submenu_id])
    await delete_dish(test_client, menu_id, submenu_id, dish_id)


async def test_get_all_after_delete(test_client, server):
    await test_get_all(test_client, server)
