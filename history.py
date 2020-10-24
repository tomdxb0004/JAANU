import pandas as  pd
path = "C:\\Users\\tomdx\\Documents\\GitHub\\stock\\data_from_july_1_2020\\"

df = pd.read_pickle(path + 'BAJAJ-AUTO.pkl')

ohl = df[df['Open']==df['Low']]

print(ohl)