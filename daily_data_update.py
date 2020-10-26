import time
import pickle
from nsetools import Nse
import json
import os
import pandas as pd
import numpy as np
import re
import warnings
import time

time_list = time.ctime().split(' ')
date = time_list[1] + '-' + time_list[2] +'-' + time_list[4]


warnings.filterwarnings("ignore")

path = "C:\\Users\\tomdx\\Documents\\GitHub\\stock\\daily_closing_data\\"

os.chdir(path)

with open('nifty_100.pickle', 'rb') as handle:
    stock_dict = pickle.load(handle)


stocks_dict = {}
nse= Nse()
 

stock_parameters = ['dayHigh','dayLow','open','lastPrice','pChange','totalBuyQuantity','totalSellQuantity','totalTradedValue', 'totalTradedVolume']
for i,stock in enumerate(stock_dict.keys(),1):
    print(i,stock)
    
    stock_details = nse.get_quote(stock, as_json=True)
    stocks_dict.setdefault(stock,[])


    for i,parameter in enumerate(stock_parameters):

        #print(parameter,'******',json.loads(stock_details)[parameter])
               
        stocks_dict[stock].append(json.loads(stock_details)[parameter])
df = pd.DataFrame.from_dict(stocks_dict,orient='index',columns=['HIGH','LOW','OPEN','LAST TRADED PRICE','%change','totalBuyQuantity','totalSellQuantity','totalTradedValue', 'totalTradedVolume'])
df.reset_index(inplace=True)
df.rename(columns={'index':'symbol'},inplace=True)
file_name = path + date + 'daily_data.csv'

df.to_csv(file_name)