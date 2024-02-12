import os

import pandas as pd

current_dir = os.getcwd()
file_path = os.path.join(current_dir, 'admin', 'Menu.xlsx')


def save_df_to_excel(dataframe):
    dataframe.to_excel(file_path, index=False, header=False)
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        dataframe.to_excel(writer, index=False, header=False)


def excel_to_dataframe():
    df = pd.read_excel(file_path, header=None, engine='openpyxl')
    return df
