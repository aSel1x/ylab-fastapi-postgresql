import pickle
from typing import Sequence

from app.database.models import Dish
from app.schemas import DishScheme, MenuScheme, SubmenuScheme

from .abstract import RedisRepository


class DishRedisRepository(RedisRepository[Dish]):
    def __init__(self):
        super().__init__(
            type_model=Dish,
            type_scheme=DishScheme
        )

    async def save(self, model: Dish) -> None:
        dish = model
        # Dish:1
        dish_key = f'{self.type_model.__name__}:{dish.id}'
        dish_decoded = DishScheme(**dish.to_dict())
        await self.redis.set(dish_key, pickle.dumps(dish_decoded))

        # Add dish to <submenu_id>:Dishes list
        await self.redis.lpush(
            f'{dish.submenu_id}:{self.type_model.__name__}es',
            dish_key
        )

        # Increase submenu dishes
        submenu_key = f'Submenu:{dish.submenu_id}'
        submenu_encoded = await self.redis.get(submenu_key)
        if isinstance(submenu_encoded, bytes):
            submenu_decoded: SubmenuScheme = pickle.loads(submenu_encoded)
            submenu_decoded.dishes_count += 1
            await self.redis.set(submenu_key, pickle.dumps(submenu_decoded))

            # Increase menu dishes
            menu_key = f'Menu:{submenu_decoded.menu_id}'
            menu_encoded = await self.redis.get(menu_key)
            if isinstance(menu_encoded, bytes):
                menu_decoded: MenuScheme = pickle.loads(menu_encoded)
                menu_decoded.dishes_count += 1
                await self.redis.set(menu_key, pickle.dumps(menu_decoded))

    async def get_by_submenu_id(self, submenu_id: str | int) -> Sequence[DishScheme]:
        dishes_list: list[DishScheme] = []

        dishes_key = f'{submenu_id}:{self.type_model.__name__}es'

        for dish_key in await self.redis.lrange(dishes_key, 0, -1):
            dish_encoded = await self.redis.get(dish_key)
            if isinstance(dish_encoded, bytes):
                dish_decoded = pickle.loads(dish_encoded)
                dishes_list.append(dish_decoded)

        return dishes_list

        # submenu_key = f'Submenu:{submenu_id}'
        # submenu_encoded = await self.redis.get(submenu_key)
        # if submenu_encoded is None:
        #     return dishes_list
        # submenu_decoded: SubmenuScheme = pickle.loads(submenu_encoded)
        #
        # for dish_key in await self.redis.keys('Dish:*'):
        #     dish_encoded = await self.redis.get(dish_key)
        #     if isinstance(dish_encoded, bytes):
        #         dish_decoded: DishScheme = pickle.loads(dish_encoded)
        #         if dish_decoded.submenu_id == submenu_decoded.id:
        #             dishes_list.append(dish_decoded)
        #
        # return dishes_list

    async def delete(self, ident: int | str) -> None:
        deleted_object: DishScheme | None = await self.pre_delete(ident)
        if deleted_object is None:
            return

        # Remove from dishes list
        await self.redis.lrem(
            name=f'{deleted_object.submenu_id}:{self.type_model.__name__}es',
            count=1,
            value=f'{self.type_model.__name__}:{deleted_object.id}'
        )

        # Decrease submenu dishes
        submenu_key = f'Submenu:{deleted_object.submenu_id}'
        submenu_encoded = await self.redis.get(submenu_key)
        if isinstance(submenu_encoded, bytes):
            submenu_decoded: SubmenuScheme = pickle.loads(submenu_encoded)
            submenu_decoded.dishes_count -= 1
            await self.redis.set(submenu_key, pickle.dumps(submenu_decoded))

            # Decrease menu dishes
            menu_key = f'Menu:{submenu_decoded.menu_id}'
            menu_encoded = await self.redis.get(menu_key)
            if isinstance(menu_encoded, bytes):
                menu_decoded: MenuScheme = pickle.loads(menu_encoded)
                menu_decoded.dishes_count -= 1
                await self.redis.set(menu_key, pickle.dumps(menu_decoded))
