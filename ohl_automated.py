import time
s = time.time()
import pickle
from nsetools import Nse
import json
import os
import pandas as pd
import numpy as np
import re
import warnings
from pytz import timezone 
from datetime import datetime
from table_to_html import send_dataframe

warnings.filterwarnings("ignore")

os.chdir("C:\\Users\\tomdx\\Documents\\GitHub\\stock")
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')


with open('all_stocks.pickle', 'rb') as handle:
    stock_dict = pickle.load(handle)
del stock_dict['NIFTY 50']    
# with open('nifty50.pickle', 'rb') as handle:
    #stock_dict = pickle.dump(handle)

stocks_dict = {}
nse= Nse()


stock_parameters = ['dayHigh','dayLow','open','lastPrice','pChange']
for i,stock in enumerate(stock_dict.keys(),1):
    print(i,stock)
    
    stock_details = nse.get_quote(stock, as_json=True)
    stocks_dict.setdefault(stock,[])


    for i,parameter in enumerate(stock_parameters):

        #print(parameter,'******',json.loads(stock_details)[parameter])
               
        stocks_dict[stock].append(json.loads(stock_details)[parameter])
df = pd.DataFrame.from_dict(stocks_dict,orient='index',columns=['HIGH','LOW','OPEN','LAST TRADED PRICE','%change'])
df.reset_index(inplace=True)
df.rename(columns={'index':'symbol'},inplace=True)


nifty50 = nse.get_index_quote("nifty 50")
trend = float(nifty50['pChange'])

# qty
def cap_split_allocate(capital,ltp,no_of_best_candidates):
    cap_split = capital/no_of_best_candidates
    cap_split = 0.9 * cap_split
    return round(cap_split/ltp,0)

# from best candidates pick stock to enter
def pick_stock(no_of_best_candidates,dataframe):
      
    if no_of_best_candidates>0:
        print(dataframe)
        todays_pick = dataframe
        
        return todays_pick
df.columns = [re.sub(r'\n','',x.lower()) for x in df.columns]
#df.columns = [re.sub(r'\s$','',c) for c in df.columns]

dfx = df.copy()


dfx['%change'] = dfx['%change'].astype(float)


#ohl candidates
dfx.loc[(dfx['open']==dfx['low']),'action'] = 'B'
dfx.loc[(dfx['open']==dfx['high']),'action'] = 'S'
ohl_cand = dfx.dropna(how='any')
ohl_cand.rename(columns={'last traded price':'LTP'},inplace=True)

capital = 400000
ideal_profit = 2
stop_loss = 0.5

if trend <0:
    print('Pre-market downtrend')
    
# for S
    best_s_candidates = ohl_cand[ohl_cand['action']=='S']
    best_s_candidates = ohl_cand[ohl_cand['%change'] == ohl_cand['%change'].max()]
    ns = len(best_s_candidates)
    print('# of short candidates: ',ns,best_s_candidates)  
     
    
    best_s_candidates['Ideal_Buy_price'] = best_s_candidates['open'] * (1-(ideal_profit)/100)
    best_s_candidates['Stop_Loss'] = best_s_candidates['open'] * (1 + (stop_loss)/100)
    
        
    if ns != 0:
       
        today = pick_stock(ns,best_s_candidates)

    else:
        print('NO good pick as per OHL strategy')
        today = ['No good pick today']
    
    
else:
    print('Pre-market Uptrend')

# for B
    best_b_candidates = ohl_cand[ohl_cand['%change'] == ohl_cand['%change'].min()]
    best_b_candidates = ohl_cand[ohl_cand['action']=='B']
    nb = len(best_b_candidates)
    
    best_b_candidates['quantity'] = best_b_candidates['open'].apply(lambda x: cap_split_allocate(capital,x,nb))
    
    best_b_candidates['Ideal_Sell_price'] = best_b_candidates['open'] * (1+(ideal_profit/100))
    best_b_candidates['Stop_Loss'] = best_b_candidates['open'] *  (1 - (stop_loss)/100)
   
    print('# of buy candidates: ',nb )
    
    
    if nb != 0:
              
        today = pick_stock(nb,best_b_candidates)

    else:
        print('NO good pick as per OHL strategy')
        today = 'No good pick today'

message = today
send_dataframe(message)
e = time.time()
time_taken = str(round((e-s)/60,2)).split('.')
print('Executed in : {0} minute(s) {1} seconds'.format(time_taken[0],round(int(time_taken[1])*60/100),1))
