import json
from typing import Sequence

import pandas as pd

from app.api.depends import get_services
from app.core.config import settings
from app.core.excel import excel_to_dataframe, save_df_to_excel
from app.core.google import GoogleAuth
from app.database.models import Menu
from app.schemas import DishSchemeAdd, MenuSchemeAdd, SubmenuSchemeAdd
from app.schemas.extra import MenuPlus


class DataFrameToDB:
    def __init__(self):
        self.df_before = pd.DataFrame()

    async def process(self, df: pd.DataFrame):

        if not self.df_before.empty and df.equals(self.df_before):
            return
        _df_before = self.df_before
        self.df_before = df.copy()

        cascades: dict[int, dict[int, list[int]]] = {}

        async for service in get_services():

            for i, row in df.iterrows():

                if isinstance(_title := row[1], str) and isinstance(_description := row[2], str):
                    menu = MenuSchemeAdd(
                        title=_title,
                        description=_description
                    )
                    menu_id = int(menu_id) if (menu_id := row[0]) and pd.notna(menu_id) else None
                    if menu_id is None:
                        response = await service.menu.new(
                            title=menu.title,
                            description=menu.description
                        )
                        menu_id = response.id
                        cascades[menu_id], df.iloc[i, 0] = {}, menu_id
                        self.df_before = df.copy()
                        save_df_to_excel(df)
                        GoogleAuth().dataframe_to_sheet(df)
                        continue
                    else:
                        cascades[menu_id] = {}
                        try:
                            if _df_before.iloc[i, 0] == menu_id \
                                    and _df_before.iloc[i, 1] == _title \
                                    and _df_before.iloc[i, 2] == _description:
                                continue
                            else:
                                pass
                        except IndexError:
                            pass

                        await service.menu.update(
                            ident=menu_id,
                            scheme=menu,
                        )

                if isinstance(_title := row[2], str) and isinstance(_description := row[3], str):
                    submenu = SubmenuSchemeAdd(
                        title=_title,
                        description=_description
                    )
                    submenu_id = int(submenu_id) if (submenu_id := row[1]) and pd.notna(submenu_id) else None
                    if submenu_id is None:
                        response = await service.submenu.new(
                            menu_id=menu_id,  # type: ignore
                            title=submenu.title,
                            description=submenu.description
                        )
                        submenu_id = response.id
                        cascades[menu_id][submenu_id], df.iloc[i, 1] = [], submenu_id  # type: ignore
                        self.df_before = df.copy()
                        save_df_to_excel(df)
                        GoogleAuth().dataframe_to_sheet(df)
                        continue
                    else:
                        cascades[menu_id][submenu_id] = []  # type: ignore
                        try:
                            if _df_before.iloc[i, 1] == submenu_id \
                                    and _df_before.iloc[i, 2] == _title \
                                    and _df_before.iloc[i, 3] == _description:
                                continue
                            else:
                                pass
                        except IndexError:
                            pass

                        await service.submenu.update(
                            ident=submenu_id,
                            scheme=submenu,
                        )

                if isinstance(_title := row[3], str) and isinstance(_description := row[4], str):
                    dish = DishSchemeAdd(
                        title=_title,
                        description=_description,
                        price=row[5]
                    )
                    dish_id = int(dish_id) if (dish_id := row[2]) and pd.notna(dish_id) else None

                    if not dish_id:
                        response = await service.dish.new(
                            submenu_id=submenu_id,  # type: ignore
                            title=dish.title,
                            description=dish.description,
                            price=dish.price
                        )
                        dish_id = response.id
                        cascades[menu_id][submenu_id].append(dish_id)  # type: ignore
                        df.iloc[i, 2] = dish_id
                        self.df_before = df.copy()
                        save_df_to_excel(df)
                        GoogleAuth().dataframe_to_sheet(df)
                    else:
                        cascades[menu_id][submenu_id].append(dish_id)  # type: ignore
                        try:
                            if _df_before.iloc[row, 2] == dish_id \
                                    and _df_before.iloc[row, 3] == _title \
                                    and _df_before.iloc[row, 4] == _description \
                                    and _df_before.iloc[row, 5] == row[5]:
                                pass
                            else:
                                pass
                        except IndexError:
                            pass

                        await service.dish.update(
                            ident=dish_id,
                            scheme=dish,
                        )

                    dish_discount = int(row[6]) if pd.notna(row[6]) else 0

                    if (dishes_discounts := settings.redis.get('dishes_discounts')) \
                            and isinstance(dishes_discounts, bytes):
                        dishes_discounts = json.loads(dishes_discounts)
                        dishes_discounts[dish_id] = dish_discount
                    else:
                        dishes_discounts = {dish_id: dish_discount}

                    settings.redis.set('dishes_discounts', json.dumps(dishes_discounts))

            all_from_api: Sequence[MenuPlus | Menu] = await service.menu.get_all_extra()
            for menu in all_from_api:
                menu_id = int(menu.id)
                if menu_id not in cascades:
                    await service.menu.delete(
                        ident=menu_id,
                    )
                else:
                    for submenu in menu.submenus:
                        submenu_id = int(submenu.id)
                        if submenu_id not in cascades[menu_id]:
                            await service.submenu.delete(
                                ident=submenu_id,
                            )
                        else:
                            for dish in submenu.dishes:
                                dish_id = int(dish.id)
                                if dish_id not in cascades[menu_id][submenu_id]:
                                    await service.dish.delete(
                                        ident=dish_id,
                                    )


google = GoogleAuth()
dttdb = DataFrameToDB()


async def refresh_db_from_excel():
    await dttdb.process(excel_to_dataframe())


async def refresh_db_from_google():
    await dttdb.process(google.sheet_to_dataframe())
