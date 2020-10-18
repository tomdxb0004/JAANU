#Your API key is: b6e9d55332d74399afb695de97258a57
from newsapi import NewsApiClient
print('pass')
api = NewsApiClient(api_key='b6e9d55332d74399afb695de97258a57')
api.get_top_headlines(sources='MONEYCONTROL')
print(api.get_everything(q='yes bank'))
api.get_sources()

