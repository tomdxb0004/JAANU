import pandas as pd
import numpy as np
import os
import pickle
from nsetools import Nse
import json
import time
import glob
import warnings
from table_to_html import send_dataframe
warnings.filterwarnings("ignore")


os.chdir("C:\\Users\\tomdx\\Documents\\GitHub\\stock")

with open('nifty_100.pickle', 'rb') as handle:
    stock_dict = pickle.load(handle)


def get_nse100_data(stock_dict=stock_dict):
    stocks_dict = {}
    nse = Nse()
    stock_parameters = ['dayHigh','dayLow','open','lastPrice','pChange','totalTradedVolume']
    for i,stock in enumerate(stock_dict.keys(),1):
        print(i,stock)

        stock_details = nse.get_quote(stock, as_json=True)
        stocks_dict.setdefault(stock,[])


        for i,parameter in enumerate(stock_parameters):
            stocks_dict[stock].append(json.loads(stock_details)[parameter])
    df = pd.DataFrame.from_dict(stocks_dict,orient='index',columns=['HIGH','LOW','OPEN','LAST TRADED PRICE','%change','TOTAL TRADED VOLUME'])
    df.reset_index(inplace=True)
    df.rename(columns={'index':'symbol'},inplace=True)
    minute = time.ctime().split(':')[1]
    file_name = 'data.csv'
    file_name = minute + '_' +file_name
    path =  './vwap_data/' + file_name
    df.to_csv(path,index=False)
    return df

for i in range(9):
    get_nse100_data()
    time.sleep(300)

appended_df = pd.DataFrame()
path = r'./vwap_data/' 
all_files = glob.glob(path + "/*.csv")

for filename in all_files:
    pf = pd.read_csv(filename, index_col=None, header=0)
    appended_df = appended_df.append(pf)

def vwap(infy):
    infy['avg'] = (infy['HIGH'].values + infy['LOW'].values + infy['LAST TRADED PRICE'].values)/3
    infy['price_volume'] = infy['avg'] * infy['TOTAL TRADED VOLUME']
    infy['pv_cum_sum'] = infy['price_volume'].cumsum()
    infy['cum_v'] = infy['TOTAL TRADED VOLUME'].cumsum()
    infy['vwap'] = infy['pv_cum_sum']/infy['cum_v']
    infy.loc[infy['vwap']>infy['LAST TRADED PRICE'],'Action'] = 'Short'
    infy.loc[infy['vwap']<infy['LAST TRADED PRICE'],'Action'] = 'Long'
    infy.loc[infy['vwap']==infy['LAST TRADED PRICE'],'Action'] = 'No VWAP'
    return infy

final_df = pd.DataFrame()
for stock in stock_dict.keys():
    infy = appended_df.groupby('symbol').get_group(stock)
    final_df = final_df.append(vwap(infy).drop_duplicates(keep='last',subset=['symbol']))

nse= Nse()

nifty50 = nse.get_index_quote("nifty 50")
trend = float(nifty50['pChange'])

if trend>0:
    buy_candidates = final_df[final_df['Action']=='Long']
    send_dataframe(buy_candidates,'green_light')
else:
    sell_candidates = final_df[final_df['Action']=='Short']
    send_dataframe(sell_candidates,'red_light')
    