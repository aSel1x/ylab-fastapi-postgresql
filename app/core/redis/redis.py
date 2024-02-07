from .repositories import (
    DishRedisRepository,
    MenuRedisRepository,
    SubmenuRedisRepository,
)


class Redis:

    menu: MenuRedisRepository
    submenu: SubmenuRedisRepository
    dish: DishRedisRepository

    def __init__(
            self,
            menu: MenuRedisRepository | None = None,
            submenu: SubmenuRedisRepository | None = None,
            dish: DishRedisRepository | None = None,
    ):
        self.menu = menu or MenuRedisRepository()
        self.submenu = submenu or SubmenuRedisRepository()
        self.dish = dish or DishRedisRepository()
