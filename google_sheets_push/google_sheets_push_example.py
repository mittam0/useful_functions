from datetime import datetime
from Google_class import Google_table
import pandas as pd 



google = Google_table()

# df = pd.read_excel('all_deals.xlsx')
# df = df.astype(str)
df = pd.DataFrame({'id': list(range(0, 10))})
google.write_to_my_sheet_batch(df = df, worksheet_name = 'sheet_name')