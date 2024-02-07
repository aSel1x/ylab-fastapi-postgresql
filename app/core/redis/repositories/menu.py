import pickle
from typing import Sequence

from app.database.models import Menu
from app.schemas import MenuScheme

from .abstract import RedisRepository


class MenuRedisRepository(RedisRepository[Menu]):
    def __init__(self):
        super().__init__(
            type_model=Menu,
            type_scheme=MenuScheme
        )

    async def save(self, menu: Menu) -> None:
        # Menu:1
        menu_key = f'{self.type_model.__name__}:{menu.id}'
        menu_decoded = MenuScheme(**menu.to_dict())
        await self.redis.set(menu_key, pickle.dumps(menu_decoded))

    async def get_all(self) -> Sequence[MenuScheme] | None:
        menu_list = []
        for key in await self.redis.keys(f'{self.type_model.__name__}:*'):
            menu_encoded = await self.redis.get(key)
            if isinstance(menu_encoded, bytes):
                menu_decoded = pickle.loads(menu_encoded)
                menu_list.append(menu_decoded)
        return menu_list if menu_list != [] else None

    async def delete(self, ident: int | str) -> None:
        deleted_object: MenuScheme | None = await self.pre_delete(ident)
        if deleted_object is None:
            return

        submenus_list_key = f'{deleted_object.id}:Submenus'
        dishes_list_keys = []

        for submenu_key in await self.redis.lrange(submenus_list_key, 0, -1):
            submenu_id = submenu_key.decode().split(':')[1]
            await self.redis.delete(submenu_key)

            submenu_dishes_list_key = f'{submenu_id}:Dishes'
            dishes_list_keys.append(submenu_dishes_list_key)
            for dish_key in await self.redis.lrange(submenu_dishes_list_key, 0, -1):
                await self.redis.delete(dish_key)

        await self.redis.delete(submenus_list_key)
        for dishes_list_key in dishes_list_keys:
            await self.redis.delete(dishes_list_key)
