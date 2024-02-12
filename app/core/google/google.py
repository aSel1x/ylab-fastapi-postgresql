import os

import numpy as np
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleAuth:
    def __init__(self):
        self.CURRENT_DIR = os.path.dirname(__file__)
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.SAMPLE_SPREADSHEET_ID = '1H9LGzP5cCgBqqdUGyBz6fqJeZ6IXZEdacCmC60mQ9nQ'
        self.SAMPLE_RANGE_NAME = 'ylab!A:G'
        self.CREDENTIAL = self._get_credentials()

    def _get_credentials(self):
        creds = None
        if os.path.exists(self.CURRENT_DIR + '/token.json'):
            creds = Credentials.from_authorized_user_file(self.CURRENT_DIR + '/token.json', self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CURRENT_DIR + '/credentials.json', self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(self.CURRENT_DIR + '/token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def sheet_to_dataframe(self):
        service = build('sheets', 'v4', credentials=self.CREDENTIAL)
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range=self.SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get('values', [])
        df = pd.DataFrame(values)
        df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
        df = df.map(lambda x: pd.to_numeric(x, errors='ignore') if isinstance(x, str) else x)
        return df

    def dataframe_to_sheet(self, df: pd.DataFrame):
        df_new = df.copy()
        service = build('sheets', 'v4', credentials=self.CREDENTIAL)
        df_new.fillna('', inplace=True)
        body = {'values': df_new.values.tolist()}
        (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                range=self.SAMPLE_RANGE_NAME,
                valueInputOption='RAW',
                body=body
            )
            .execute()
        )
