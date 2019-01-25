# import the requests library used to handle HTTP GET requests
import requests
import json

base_api_link = 'https://api.iextrading.com/1.0/'

def getStockPrice(ticker):
	# generate custom API call using the base API url and the Stock ticker 
	api_url = '{0}stock/{1}/quote'.format(base_api_link,ticker)
	try:
		output = requests.get(api_url)
		if output.status_code != 200:
			output.raise_for_status()
	except requests.exceptions.HTTPError as e:
		return "This stock is not listed on our system"	
		#to-do log
	
	# get the output in json format and then pick out the current stock price
	return output.json()['iexRealtimePrice']

	
print(getStockPrice('aapl'))