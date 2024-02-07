import pickle
from typing import Sequence

from app.database.models import Submenu
from app.schemas import MenuScheme, SubmenuScheme

from .abstract import RedisRepository


class SubmenuRedisRepository(RedisRepository[Submenu]):
    def __init__(self):
        super().__init__(
            type_model=Submenu,
            type_scheme=SubmenuScheme
        )

    async def save(self, submenu: Submenu) -> None:
        # Submenu:1
        submenu_key = f'{self.type_model.__name__}:{submenu.id}'
        submenu_decoded = SubmenuScheme(**submenu.to_dict())
        await self.redis.set(submenu_key, pickle.dumps(submenu_decoded))

        # Add submenu to <menu_id>:Submenus list
        await self.redis.lpush(
            f'{submenu.menu_id}:{self.type_model.__name__}s',
            submenu_key
        )

        # Increase menu submenus
        menu_key = f'Menu:{submenu.menu_id}'
        menu_encoded = await self.redis.get(menu_key)
        if isinstance(menu_encoded, bytes):
            menu_decoded: MenuScheme = pickle.loads(menu_encoded)
            # Refresh menu
            menu_decoded.submenus_count += 1
            menu_encoded = pickle.dumps(menu_decoded)
            await self.redis.set(menu_key, menu_encoded)

    async def get_by_menu_id(self, menu_id: str | int) -> Sequence[SubmenuScheme]:
        submenus_list: list[SubmenuScheme] = []

        # menu_key = f'Menu:{menu_id}'
        submenus_key = f'{menu_id}:{self.type_model.__name__}s'

        for submenu_key in await self.redis.lrange(submenus_key, 0, -1):
            submenu_encoded = await self.redis.get(submenu_key.decode())
            if isinstance(submenu_encoded, bytes):
                submenu_decoded = pickle.loads(submenu_encoded)
                submenus_list.append(submenu_decoded)

        return submenus_list

        # menu_encoded = await self.redis.get(menu_key)
        # if menu_encoded is None:
        #     return submenus_list
        # menu_decoded: MenuScheme = pickle.loads(menu_encoded)
        #
        # for submenu_key in await self.redis.keys('Submenu:*'):
        #     submenu_encoded = await self.redis.get(submenu_key)
        #     if isinstance(submenu_encoded, bytes):
        #         submenu_decoded: SubmenuScheme = pickle.loads(submenu_encoded)
        #         if submenu_decoded.menu_id == menu_decoded.id:
        #             submenus_list.append(submenu_decoded)
        #
        # return submenus_list

    async def delete(self, ident: int | str) -> None:
        deleted_object: SubmenuScheme | None = await self.pre_delete(ident)
        if deleted_object is None:
            return None

        # Remove from submenus list
        submenus_keys = f'{deleted_object.menu_id}:{self.type_model.__name__}s'
        await self.redis.lrem(
            name=submenus_keys,
            count=1,
            value=f'{self.type_model.__name__}:{deleted_object.id}'
        )

        dishes_keys = f'{deleted_object.id}:Dishes'
        for dish_key in await self.redis.lrange(dishes_keys, 0, -1):
            await self.redis.delete(dish_key)

        # # Dishes remove
        # for dish_key in await self.redis.keys('Dish:*'):
        #     dish_encoded = await self.redis.get(dish_key)
        #     if isinstance(dish_encoded, bytes):
        #         dish_decoded: DishScheme = pickle.loads(dish_encoded)
        #         if dish_decoded.submenu_id == deleted_object.id:
        #             await self.redis.delete(dish_key)

        # Menu decrease
        menu_key = f'Menu:{deleted_object.menu_id}'
        menu_encoded = await self.redis.get(menu_key)
        if isinstance(menu_encoded, bytes):
            menu_decoded: MenuScheme = pickle.loads(menu_encoded)
            menu_decoded.submenus_count -= 1
            menu_decoded.dishes_count -= deleted_object.dishes_count
            await self.redis.set(menu_key, pickle.dumps(menu_decoded))
