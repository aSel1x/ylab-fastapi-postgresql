import pickle
from typing import Sequence

from app.database.models import Menu, Submenu
from app.schemas import DishScheme, MenuScheme, SubmenuScheme

from .abstract import RedisRepository


class SubmenuRedisRepository(RedisRepository[Submenu]):
    def __init__(self):
        super().__init__(type_model=Submenu)

    async def save(self, submenu: Submenu) -> None:
        # Submenu:1
        submenu_key = f'{submenu.__class__.__name__}:{submenu.id}'
        submenu_decoded = SubmenuScheme(**submenu.to_dict())
        await self.redis.set(submenu_key, pickle.dumps(submenu_decoded))

        # Increase menu submenus
        menu_key = f'Menu:{submenu.menu_id}'
        menu_encoded = await self.redis.get(menu_key)
        menu_decoded: MenuScheme = pickle.loads(menu_encoded)
        menu_decoded.submenus_count += 1
        await self.redis.set(menu_key, pickle.dumps(menu_decoded))
        await self.redis.save()

    async def get_by_menu_id(self, menu_id: str | int) -> Sequence[SubmenuScheme]:
        submenus_list = []

        menu_key = f'Menu:{menu_id}'
        menu_encoded = await self.redis.get(menu_key)
        if menu_encoded is None:
            return submenus_list
        menu_decoded: MenuScheme = pickle.loads(menu_encoded)

        for submenu_key in await self.redis.keys('Submenu:*'):
            submenu_encoded = await self.redis.get(submenu_key)
            submenu_decoded: SubmenuScheme = pickle.loads(submenu_encoded)
            if submenu_decoded.menu_id == menu_decoded.id:
                submenus_list.append(submenu_decoded)

        return submenus_list

    async def delete(self, ident: int | str) -> None:
        deleted_object: SubmenuScheme | None = await self._delete(ident)
        if deleted_object is None:
            return

        # Dishes remove
        for dish_key in await self.redis.keys('Dish:*'):
            dish_encoded = await self.redis.get(dish_key)
            dish_decoded: DishScheme = pickle.loads(dish_encoded)
            if dish_decoded.submenu_id == deleted_object.id:
                await self.redis.delete(dish_key)

        # Menu decrease
        menu_key = f'Menu:{deleted_object.menu_id}'
        menu_encoded = await self.redis.get(menu_key)
        menu_decoded: MenuScheme = pickle.loads(menu_encoded)
        menu_decoded.submenus_count -= 1
        menu_decoded.dishes_count -= deleted_object.dishes_count
        await self.redis.set(menu_key, pickle.dumps(menu_decoded))
