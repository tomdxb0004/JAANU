import pandas as pd
import yfinance as yf
from yahoofinancials import YahooFinancials
from datetime import datetime as dt
import os
import pickle
print(os.getcwd())
path = "C:\\Users\\tomdx\\Documents\\GitHub\\stock\\data_from_july_1_2020\\"
todays_date = str(dt.today()).split(' ')[0]

with open('all_stocks.pickle', 'rb') as handle:
    stock_dict = pickle.load(handle)
del stock_dict['NIFTY 50']    

for i,stock in enumerate(stock_dict.keys(),1):
    print(i,stock)
    stock_name = str(stock) + '.ns'

    stock_df = yf.download(stock_name, 
                      start='2020-07-01', 
                      end=todays_date, 
                      progress=True)
    stock_df.to_pickle(path+str(stock)+'.pkl')
