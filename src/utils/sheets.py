from datetime import datetime
import pandas as pd
from string import ascii_uppercase

import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
from .constants import SUPPORTED_RAW_LOG_PLATFORMS, SUPPORTED_RAW_LOG_MESSAGES, SUPPORTED_RAW_LOG_SONGS


class GoogleSheet(object):
    def __init__(self, keyfile):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = SAC.from_json_keyfile_name(keyfile, scope)
        self.client = gspread.authorize(creds)

    def get_raw_logs_as_sheet(self):
        return self.client.open('kontstats').worksheet('RAW_LOGS')

    def get_raw_logs_as_values(self):
        sheet = self.get_raw_logs_as_sheet()
        return sheet.get_all_values()

    def get_raw_logs_as_df(self):
        all_vals = self.get_raw_logs_as_values()

        colnames = all_vals[0]
        data = all_vals[1:]
        df = pd.DataFrame(data,
                          columns=colnames)
        return df

    def write_raw_log(self, platform, song, message, value):
        """
        Method that writes a raw log entry in the RAW_LOGS sheet
        """
        assert platform in SUPPORTED_RAW_LOG_PLATFORMS, f'{platform} not in SUPPORTED_RAW_LOG_PLATFORMS:{", ".join(SUPPORTED_RAW_LOG_PLATFORMS)}'
        assert message in SUPPORTED_RAW_LOG_MESSAGES, f'{message} not in SUPPORTED_RAW_LOG_PLATFORMS:{", ".join(SUPPORTED_RAW_LOG_MESSAGES)}'
        assert song in SUPPORTED_RAW_LOG_SONGS, f'{song} not in SUPPORTED_RAW_LOG_PLATFORMS:{", ".join(SUPPORTED_RAW_LOG_MESSAGES)}'

        log = []

        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log.append(timestamp)
        log.append(platform)
        log.append(song)
        log.append(message)
        log.append(value)

        sheet = self.get_raw_logs_as_sheet()

        nrow = str(len(self.get_raw_logs_as_values())+1)
        for i, value in enumerate(log):
            col_letter = ascii_uppercase[i]
            cell_name = col_letter+nrow
            sheet.update_acell(cell_name, value)

    def sheet_to_df(self, worksheet_name, sheet_name):
        """
        Method that returns a dataframe of a sheet

        Parameters
        worksheetname(str) : worksheet name
        sheet_name(str): sheet name in worksheet
        """
        sheet = self.client.open(worksheet_name).worksheet(sheet_name)
        all_vals = sheet.get_all_values()

        colnames = all_vals[0]
        data = all_vals[1:]
        df = pd.DataFrame(data,
                          columns=colnames)
        return df

    def df_to_sheet(self, worksheet_name, sheet_name, df):
        """
        Method that overwrites sheet_name with df

        Parameters
        worksheetname(str) : worksheet name
        sheet_name(str): sheet name in worksheet
        df(pd.DataFrame): DataFrame to write
        """
        df = df.T.reset_index().T  # to add the columns to the content of the DataFrame
        nr_rows = df.shape[0]
        nr_cols = df.shape[1]
        assert nr_cols <= 26, 'Only less than 26 columns supported'

        sheet = self.client.open(worksheet_name).worksheet(sheet_name)

        col_names = df.columns
        col_letters = ascii_uppercase[0:nr_cols]

        for col_name, col_letter in zip(col_names, col_letters):
            cell_range = f'{col_letter}1:{col_letter}{nr_rows}'
            cell_list = sheet.range(cell_range)
            series = df[col_name]
            for cell, value in zip(cell_list, series.values):
                cell.value = str(value)
            # Update in batch
            sheet.update_cells(cell_list)
