import json
import os

import pandas as pd
import requests

from app import app
from app.core.config import settings
from app.core.excel import excel_to_dataframe, save_df_to_excel
from app.core.google import GoogleAuth

current_dir = os.getcwd()
file_path = os.path.join(current_dir, 'admin', 'Menu.xlsx')


class APIClient:
    def __init__(self):
        self.base = 'http://restaurant_ylab:8000'

    def fetch(self, path: str, **params) -> dict:
        return requests.get(
            self.base + app.url_path_for(path, **params)
        ).json()

    def post(self, path: str, _json: dict, **params) -> dict:
        return requests.post(
            self.base + app.url_path_for(path, **params),
            json=_json
        ).json()

    def patch(self, path: str, _json: dict, **params) -> dict:
        return requests.patch(
            self.base + app.url_path_for(path, **params),
            json=_json
        ).json()

    def delete(self, path: str, **params) -> None:
        requests.delete(
            self.base + app.url_path_for(path, **params),
        )


def dataframe_to_db(df: pd.DataFrame):
    cascades: dict[int, dict[int, list[int]]] = {}
    apiCli = APIClient()

    dishes_discounts: dict[int, int] = {}

    for row, col in enumerate(df.iloc[:, 1]):
        if isinstance(col, str) and isinstance(df.iloc[row, 2], str):
            menu = {
                'title': col,
                'description': df.iloc[row, 2],
            }
            if (menu_id := df.iloc[row, 0]) and pd.notna(menu_id):
                last_menu_id = int(menu_id)
                apiCli.patch(path='patch_menu_id', _json=menu, menu_id=last_menu_id)
            else:
                response = apiCli.post(path='post_menu', _json=menu)
                last_menu_id = int(response['id'])
                df.iloc[row, 0] = last_menu_id
                save_df_to_excel(df)
                GoogleAuth().dataframe_to_sheet(df)

            cascades[last_menu_id] = {}

        if isinstance(df.iloc[row, 2], str) and isinstance(df.iloc[row, 3], str):
            submenu = {
                'title': df.iloc[row, 2],
                'description': df.iloc[row, 3],
            }
            if (submenu_id := df.iloc[row, 1]) and pd.notna(submenu_id):
                last_submenu_id = int(submenu_id)
                apiCli.patch(path='patch_submenu_id', _json=submenu, menu_id=last_menu_id, submenu_id=last_submenu_id)
            else:
                response = apiCli.post(path='post_submenu', _json=submenu, menu_id=last_menu_id)
                last_submenu_id = int(response['id'])
                df.iloc[row, 1] = last_submenu_id
                save_df_to_excel(df)
                GoogleAuth().dataframe_to_sheet(df)

            cascades[last_menu_id][last_submenu_id] = []

        if isinstance(df.iloc[row, 3], str) and isinstance(df.iloc[row, 4], str):
            dish = {
                'title': df.iloc[row, 3],
                'description': df.iloc[row, 4],
                'price': df.iloc[row, 5],
            }
            if (dish_id := df.iloc[row, 2]) and pd.notna(dish_id):
                last_dish_id = int(dish_id)
                apiCli.patch(path='patch_dish_id', _json=dish, menu_id=last_menu_id,
                             submenu_id=last_submenu_id, dish_id=last_dish_id)
            else:
                response = apiCli.post(path='post_dish', _json=dish, menu_id=last_menu_id, submenu_id=last_submenu_id)
                last_dish_id = int(response['id'])
                df.iloc[row, 2] = last_dish_id
                save_df_to_excel(df)
                GoogleAuth().dataframe_to_sheet(df)

            cascades[last_menu_id][last_submenu_id].append(last_dish_id)

            if pd.notna(df.iloc[row, 6]):
                dishes_discounts[last_dish_id] = int(df.iloc[row, 6])

    settings.redis.set('dishes_discounts', json.dumps(dishes_discounts))

    all_from_api = apiCli.fetch('get_all')
    for menu in all_from_api['menus']:
        menu_id = int(menu['id'])
        if menu_id not in cascades:
            apiCli.delete(path='delete_menu_id', menu_id=menu_id)
        else:
            for submenu in menu['submenus']:
                submenu_id = int(submenu['id'])
                if submenu_id not in cascades[menu_id]:
                    apiCli.delete(path='delete_submenu_id', menu_id=menu_id, submenu_id=submenu_id)
                else:
                    for dish in submenu['dishes']:
                        dish_id = int(dish['id'])
                        if dish_id not in cascades[menu_id][submenu_id]:
                            apiCli.delete('delete_dish_id', menu_id=menu_id,
                                          submenu_id=submenu_id, dish_id=dish_id)


def refresh_db_from_excel():
    dataframe_to_db(excel_to_dataframe())


def refresh_db_from_google():
    google = GoogleAuth()
    dataframe_to_db(google.sheet_to_dataframe())
