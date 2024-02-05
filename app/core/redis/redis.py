from .repositories import *


class Redis:

    menu: MenuRedisRepository
    submenu: SubmenuRedisRepository
    dish: DishRedisRepository

    def __init__(
            self,
            menu: MenuRedisRepository = None,
            submenu: SubmenuRedisRepository = None,
            dish: DishRedisRepository = None,
    ):
        self.menu = menu or MenuRedisRepository()
        self.submenu = submenu or SubmenuRedisRepository()
        self.dish = dish or DishRedisRepository()
