import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


class Google_table:

    def __init__(self, spreadsheet_id=None):
        self.SPREADSHEET_ID = spreadsheet_id or # "" ID Google таблицы по умолчанию


    def get_google_sheets_client(self):
        SCOPE = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        CREDS_FILE = "credentials.json"
        creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE)
        client = gspread.authorize(creds)
        return client

    def write_to_my_sheet_batch(self, df, worksheet_name="Sheet1"):
        """Записывает данные в гугл таблицу по 1000 строк"""
        try:
            client = self.get_google_sheets_client()
            spreadsheet = client.open_by_key(self.SPREADSHEET_ID)
            
            try:
                worksheet = spreadsheet.worksheet(worksheet_name)
            except gspread.WorksheetNotFound:
                worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=26)
            
            all_data = [df.columns.tolist()] + df.values.tolist()
            
            # Очищаем и записываем за один раз
            worksheet.clear()
            worksheet.update('A1', all_data)
            
            print("Данные записаны пакетным методом!")
            return True
            
        except Exception as e:
            print(f"Ошибка: {e}")
            return False


    def list_worksheets(self):
        """Показывает все листы в таблице"""
        try:
            client = self.get_google_sheets_client()
            spreadsheet = client.open_by_key(self.SPREADSHEET_ID)
            
            worksheets = spreadsheet.worksheets()
            print("Доступные листы:")
            for ws in worksheets:
                print(f"- {ws.title} (строк: {ws.row_count}, колонок: {ws.col_count})")
                
            return worksheets
        except Exception as e:
            print(f"Ошибка: {e}")
            

    def read_from_my_sheet(self, worksheet_name="Sheet1"):
        """Читает данные из таблицы"""
        try:
            client = self.get_google_sheets_client()
            spreadsheet = client.open_by_key(self.SPREADSHEET_ID)
            worksheet = spreadsheet.worksheet(worksheet_name)
            
            # Получаем все данные
            data = worksheet.get_all_records()
            df = pd.DataFrame(data)
            
            print(f"Прочитано {len(df)} строк из листа '{worksheet_name}'")
            return df
            
        except Exception as e:
            print(f"Ошибка при чтении: {e}")
            return pd.DataFrame()
