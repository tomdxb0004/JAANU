import pandas as  pd
import pickle
import time
path = "C:\\Users\\tomdx\\Documents\\GitHub\\stock\\data_from_july_1_2020\\"

df = pd.read_pickle(path + 'BAJAJ-AUTO.pkl')

ohl = df[df['Open']==df['Low']]

date = time.ctime().split(' ')[2] + time.ctime().split(' ')[1]

print(date)

