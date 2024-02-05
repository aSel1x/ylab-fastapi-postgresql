import pickle

from app.database.models import Menu
from app.schemas import DishScheme, MenuScheme, SubmenuScheme

from .abstract import RedisRepository


class MenuRedisRepository(RedisRepository[Menu]):
    def __init__(self):
        super().__init__(type_model=Menu)

    async def save(self, menu: Menu) -> None:
        # Menu:1
        menu_key = f'{menu.__class__.__name__}:{menu.id}'
        menu_decoded = MenuScheme(**menu.to_dict())
        await self.redis.set(menu_key, pickle.dumps(menu_decoded))

    async def delete(self, ident: int | str) -> None:
        deleted_object: MenuScheme | None = await self._delete(ident)
        if deleted_object is None:
            return

        for submenu_key in await self.redis.keys('Submenu:*'):
            submenu_encoded = await self.redis.get(submenu_key)
            submenu_decoded: SubmenuScheme = pickle.loads(submenu_encoded)
            if submenu_decoded.menu_id == deleted_object.id:
                await self.redis.delete(submenu_key)

                for dish_key in await self.redis.keys('Dish:*'):
                    dish_encoded = await self.redis.get(dish_key)
                    dish_decoded: DishScheme = pickle.loads(dish_encoded)
                    if dish_decoded.submenu_id == submenu_decoded.id:
                        await self.redis.delete(dish_key)
