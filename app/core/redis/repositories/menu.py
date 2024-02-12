import pickle
from typing import Sequence

from app.database.models import Menu
from app.schemas import MenuScheme
from app.schemas.extra import MenuPlus, SubmenuPlus

from .abstract import RedisRepository


class MenuRedisRepository(RedisRepository[Menu]):
    def __init__(self):
        super().__init__(
            type_model=Menu,
            type_scheme=MenuScheme
        )

    async def save(self, model: Menu) -> None:
        menu = model
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

    async def get_all_extra(self) -> Sequence[MenuPlus] | None:
        response_list = []
        for menu_key in await self.redis.keys(f'{self.type_model.__name__}:*'):
            menu_encoded = await self.redis.get(menu_key)
            if isinstance(menu_encoded, bytes):
                menu_decoded = pickle.loads(menu_encoded)
                menu_decoded = MenuPlus(**menu_decoded.__dict__, submenus=[])

                submenus_list_key = f'{menu_decoded.id}:Submenus'
                for submenu_key in await self.redis.lrange(submenus_list_key, 0, -1):
                    submenu_encoded = await self.redis.get(submenu_key)
                    if isinstance(submenu_encoded, bytes):
                        submenu_decoded = pickle.loads(submenu_encoded)
                        submenu_decoded = SubmenuPlus(**submenu_decoded.__dict__, dishes=[])

                        dishes_list_key = f'{submenu_decoded.id}:Dishes'
                        for dish_key in await self.redis.lrange(dishes_list_key, 0, -1):
                            dish_encoded = await self.redis.get(dish_key)
                            if isinstance(dish_encoded, bytes):
                                dish_decoded = pickle.loads(dish_encoded)

                                submenu_decoded.dishes.append(dish_decoded)
                        menu_decoded.submenus.append(submenu_decoded)
                response_list.append(menu_decoded)
        return response_list
