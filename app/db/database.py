from typing import Dict, Tuple, List, Optional

from app.data.config import DB_URL
from app.db.queries import *
from app.db.models import (
    MenuModel,
    SubMenuModel,
    DishModel
)

import asyncpg


class DBConnect:

    @staticmethod
    async def _fetchone(query: str, params: Optional[Tuple] = None) -> asyncpg.Record:
        conn: asyncpg.Connection = await asyncpg.connect(DB_URL)
        if params:
            data = await conn.fetchrow(query, *params, timeout=1000)
        else:
            data = await conn.fetchrow(query, timeout=1000)
        await conn.close()
        return data

    @staticmethod
    async def _fetchall(query: str, params: Optional[Tuple] = None) -> List[asyncpg.Record]:
        conn: asyncpg.Connection = await asyncpg.connect(DB_URL)
        if params:
            data = await conn.fetch(query, *params, timeout=1000)
        else:
            data = await conn.fetch(query, timeout=1000)
        await conn.close()
        return data

    @staticmethod
    async def _serial_insert(query: str, params: Optional[Tuple] = None) -> int:
        conn: asyncpg.Connection = await asyncpg.connect(DB_URL)
        if params:
            _id = await conn.fetchval(query, *params, timeout=1000)
        else:
            _id = await conn.fetchval(query, timeout=1000)
        await conn.close()
        return _id

    @staticmethod
    async def _change(query: str, params: Optional[Tuple] = None) -> None:
        conn: asyncpg.Connection = await asyncpg.connect(DB_URL)
        if params:
            await conn.execute(query, *params)
        else:
            await conn.execute(query)
        await conn.close()

    async def setup(self) -> None:
        await self._change(CREATE_MENUS_TABLE)
        await self._change(CREATE_SUBMENUS_TABLE)
        await self._change(CREATE_DISHES_TABLE)


class Menus(DBConnect):
    cache: Dict[int, MenuModel] = {}

    async def get_id(self, _id: int) -> MenuModel | None:
        if _id in self.cache:
            return self.cache[_id]
        data = await self._fetchone(MENU_FETCH_ID, (_id,))
        if data is not None:
            _m = MenuModel(**data)
            self.cache[_id] = _m
            return _m
        return None

    async def get_all(self) -> List[MenuModel]:
        data = await self._fetchall(MENU_FETCH_ALL)
        _ms = []
        for menu in data:
            _m = MenuModel(**menu)
            submenus_count = await self._fetchone(MENU_SUBMENUS_COUNT, (_m.id,))
            dishes_count = await self._fetchone(MENU_DISHES_COUNT, (_m.id,))
            _m.submenus_count = submenus_count[0] or 0
            _m.dishes_count = dishes_count[0] or 0
            self.cache[_m.id] = _m
            _ms.append(_m)
        return _ms

    async def insert(self, menu_model: MenuModel) -> MenuModel:
        _id = await self._serial_insert(MENU_INSERT, (*menu_model.to_tuple()[1:],))
        menu_model.id = _id
        self.cache[_id] = menu_model
        return menu_model

    async def update(self, menu_model: MenuModel) -> None:
        await self._change(MENU_UPDATE_ID, (*menu_model.to_tuple(),))
        if menu_model.id in self.cache:
            self.cache[menu_model.id] = menu_model

    async def delete(self, _id: int) -> None:
        await self._change(MENU_DELETE_ID, (_id,))
        if _id in self.cache:
            self.cache.pop(_id)


class SubMenus(DBConnect):
    cache: Dict[int, SubMenuModel] = {}

    async def get_id(self, _id: int) -> SubMenuModel | None:
        if _id in self.cache:
            return self.cache[_id]
        data = await self._fetchone(SUBMENU_FETCH_ID, (_id,))
        if data is not None:
            _sm = SubMenuModel(**data)
            self.cache[_id] = _sm
            return _sm
        return None

    async def get_all(self, _id: int) -> List[SubMenuModel]:
        data = await self._fetchall(SUBMENU_FETCH_MENU_ID, (_id,))
        _sms = []
        for submenu in data:
            _sm = SubMenuModel(**submenu)
            dishes_count = await self._fetchone(SUBMENU_DISHES_COUNT, (_sm.id,))
            _sm.dishes_count = dishes_count[0] or 0
            self.cache[_sm.id] = _sm
            _sms.append(_sm)
        return _sms

    async def insert(self, submenu_model: SubMenuModel) -> SubMenuModel:
        _id = await self._serial_insert(SUBMENU_INSERT, (*submenu_model.to_tuple()[1:],))
        submenu_model.id = _id
        self.cache[_id] = submenu_model
        if Menus.cache[submenu_model.menu_id]:
            Menus.cache[submenu_model.menu_id].submenus_count += 1
        return submenu_model

    async def update(self, submenu_model: SubMenuModel) -> None:
        await self._change(SUBMENU_UPDATE_ID, (*submenu_model.to_tuple(),))
        self.cache[submenu_model.id] = submenu_model

    async def delete(self, menu_id, _id: int) -> None:
        await self._change(SUBMENU_DELETE_ID, (_id,))
        if Menus.cache[menu_id]:
            Menus.cache.pop(menu_id)
        if _id in self.cache:
            self.cache.pop(_id)


class Dishes(DBConnect):
    cache: Dict[int, DishModel] = {}

    async def get_id(self, _id: int) -> DishModel | None:
        if _id in self.cache:
            return self.cache[_id]
        data = await self._fetchone(DISHES_FETCH_ID, (_id,))
        if data is not None:
            _d = DishModel(**data)
            self.cache[_id] = _d
            return _d
        return None

    async def get_all(self, _id: int) -> List[DishModel]:
        data = await self._fetchall(DISHES_FETCH_SUBMENU_ID, (_id,))
        _ds = []
        for dish in data:
            _d = DishModel(**dish)
            self.cache[_d.id] = _d
            _ds.append(_d)
        return _ds

    async def insert(self, menu_id, dishes_model: DishModel) -> DishModel:
        _id = await self._serial_insert(DISHES_INSERT, (*dishes_model.to_tuple()[1:],))
        dishes_model.id = _id
        self.cache[_id] = dishes_model
        if Menus.cache[menu_id]:
            Menus.cache[menu_id].dishes_count += 1
        if SubMenus.cache[dishes_model.submenu_id]:
            SubMenus.cache[dishes_model.submenu_id].dishes_count += 1
        return dishes_model

    async def update(self, dishes_model: DishModel) -> None:
        await self._change(DISHES_UPDATE_ID, (*dishes_model.to_tuple(),))
        self.cache[dishes_model.id] = dishes_model

    async def delete(self, menu_id, submenu_id, _id: int) -> None:
        await self._change(DISHES_DELETE_ID, (_id,))
        if Menus.cache[menu_id]:
            Menus.cache[menu_id].dishes_count -= 1
        if SubMenus.cache[submenu_id]:
            SubMenus.cache[submenu_id].dishes_count -= 1
        if _id in self.cache:
            self.cache.pop(_id)


class DataBase:
    connection: DBConnect = DBConnect()
    menus: Menus = Menus()
    submenus: SubMenus = SubMenus()
    dishes: Dishes = Dishes()
