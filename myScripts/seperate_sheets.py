import pandas as pd
from myScripts.utils import *

if __name__=="__main__":
    datapath = f'../report/(4._.2020)/report.xlsx'
    df = pd.read_excel(datapath)
    artIds = list(df['articleID'].unique())
    writer = pd.ExcelWriter(f'../report/(4._.2020)/seperated_results.xlsx',
                            engine='xlsxwriter')
    c = 0
    for id in  artIds:
        c = c + 1
        df_sheet = df[df['articleID']==id]
        assert len(df_sheet['articleID'].unique()) == 1, f'{id} not unique'
        df_sheet.to_excel(writer,index=None, sheet_name=f"{c}")

    writer.save()
