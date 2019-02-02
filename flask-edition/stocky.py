''' 
Description: Library built to make it simpler to work with the IEX-Trading HTTTP GET API.
Version: 1.0
Author: Sean Hamill
'''

# import the requests library used to handle HTTP GET requests
import requests
import json

base_api_link = 'https://api.iextrading.com/1.0/'

if __name__ == "__main__":
    """
    @author proposal by EM
    """
	# Run this file using the python command
	# Test functions can be invoked from here

def process_api_call(api_url):
	try:
		result = requests.get(api_url)
		if result.status_code != 200:
			result.raise_for_status()		
	except requests.exceptions.HTTPError as e:
		return "This stock is not listed on our system"	
		#to-do log
	
	return result.json()


def get_current_share_price(symbol):
	'''
	Returns current price value in dollars
	'''  
	api_url = '{}stock/{}/quote'.format(base_api_link,symbol)
	
	return process_api_call(api_url)['iexRealtimePrice']

def get_company_info(symbol):
	'''
	Returns general information on company (inc. CEO, Sector, Description)
	'''
	api_url = '{}stock/{}/company'.format(base_api_link, symbol)
	
	return process_api_call(api_url)
	
def get_month_chart(symbol, num_of_months):
	'''
	Parameters:
		
		symbol - Stock symbol used on exchange (e.g AAPL,GOOG, TSLA)
		num_of_months - Number of months of data to return limited to only (1,3,6)
		
	Returns the daily price-close over the last 30 day period for a company
	'''
	accepted_numbers = [1,3,6]
	if num_of_months not in accepted_numbers:
		return '{} is not a valid time period'.format(num_of_months)
	else:
		num_of_months = '{}m'.format(num_of_months)
	api_url = '{}stock/{}/chart/{}'.format(base_api_link, symbol, num_of_months)
	
	return process_api_call(api_url)
	
def get_current_share_quote(symbol):
	'''
	Returns general current price data (inc. high, low, volume)
	'''  
	api_url = '{}stock/{}/quote'.format(base_api_link,symbol)
	
	return process_api_call(api_url)

def test():
	stuff = get_month_chart('aapl', 3)

	for things in stuff:
		print(things['date'])
		print(things['close'])

	
