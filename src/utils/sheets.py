from datetime import datetime
import pandas as pd
import string

import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheet(object):
    def __init__(self, keyfile):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            keyfile, scope)
        self.client = gspread.authorize(creds)

    def get_sheet(self):
        return self.client.open('kontstats').sheet1

    def get_vals(self):
        sheet = self.get_sheet()
        return sheet.get_all_values()

    def add_row(self, row):
        """
        Function that appends row to the bottom of the sheet

        Parameters
        row :: list of values to append
        """

        assert len(row) <= 26, 'Only support up to 26 value at this moment'
        sheet = self.get_sheet()

        last_row_nr = str(len(self.get_vals())+1)
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        row = [timestamp]+row
        for i, value in enumerate(row):
            col_letter = string.ascii_uppercase[i]
            cell_name = col_letter+last_row_nr
            sheet.update_acell(cell_name, value)

        return True
