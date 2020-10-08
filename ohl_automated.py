import time
start_time = time.time()
import pickle
from collections import defaultdict
from nsetools import Nse
import json
import os
import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import LabelEncoder
from emailer_stock import SendEmail
import warnings
from pytz import timezone 
from datetime import datetime
warnings.filterwarnings("ignore")

os.chdir("C:\\Users\\tomdx\\Documents\\GitHub\\stock")
ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')


with open('all_stocks.pickle', 'rb') as handle:
    stock_dict = pickle.load(handle)
del stock_dict['NIFTY 50']    
#with open('nifty50.pickle', 'rb') as handle:
    #stock_dict = pickle.dump(handle)

stocks_dict = {}
nse= Nse()


stock_parameters = ['dayHigh','dayLow','open','lastPrice','pChange']
for stock in stock_dict.keys():
    print(stock)
    
    stock_details = nse.get_quote(stock, as_json=True)
    stocks_dict.setdefault(stock,[])


    for i,parameter in enumerate(stock_parameters):

        print(parameter,'******',json.loads(stock_details)[parameter])
               
        stocks_dict[stock].append(json.loads(stock_details)[parameter])
df = pd.DataFrame.from_dict(stocks_dict,orient='index',columns=['HIGH','LOW','OPEN','LAST TRADED PRICE','%change'])
df.reset_index(inplace=True)
df.rename(columns={'index':'symbol'},inplace=True)
print(df.head())

nifty50 = nse.get_index_quote("nifty 50")
trend = float(nifty50['pChange'])

# qty
def cap_split_allocate(capital,ltp,no_of_best_candidates):
    cap_split = capital/no_of_best_candidates
    cap_split = 0.9 * cap_split
    return round(cap_split/ltp,0)

# from best candidates pick stock to enter
def pick_stock(no_of_best_candidates,dataframe):
    today = []
    
    if no_of_best_candidates>1:
        symbol = le.inverse_transform(dataframe['SYM']) 
        quantity = dataframe['quantity']
        action = dataframe['action']
        price = dataframe['LTP']
        today.append([symbol,action,price])
        
                
        print('Symbol: ',symbol,'\n Quantity :',quantity,'\n Price :',price)
        
        return today
df.columns = [re.sub(r'\n','',x.lower()) for x in df.columns]
df.columns = [re.sub(r'\s$','',c) for c in df.columns]

if 'chng' in df.columns:
    print('Renaming chng to change')
    df.rename(columns = {'chng':'change'},inplace=True)
 
if '%chng' in df.columns:
    print('Renaming %chng to %change')
    df.rename(columns = {'%chng':'%change'},inplace=True)
    
if 'ltp' in df.columns:
    print('Renaming ltp to last traded price')
    df.rename(columns = {'ltp':'last traded price'},inplace=True)

#remove encoding on deployment
# check time and timezones 
le = LabelEncoder()
dfx = df.copy()

dfx['SYM'] = le.fit_transform(dfx['symbol'])
dfx.drop(columns=['symbol'],inplace=True)

#for column in  dfx.select_dtypes(include='object').columns:
    #print(column)
    
    #dfx[column] = dfx[column].apply(lambda x: x.replace(',',''))
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
        today = ['No good pick today']
message = str(today) + str(ind_time)
m = SendEmail(message,'cool')
m.send_email()
print("--- %.2f seconds ---" % (time.time() - start_time))