from nse import Nse

db = Nse()

data = db.live("HDFCBANK")   
print(data)