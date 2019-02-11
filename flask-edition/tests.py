import unittest as ut
import requests
from stocky import get_current_share_price, get_month_chart, get_day_chart, process_api_call

class StockyTests(ut.TestCase):
	def test_get_stock_price(self):
		'''
		Test that it can return the current price of a stock
		'''
		output = requests.get('https://api.iextrading.com/1.0/stock/aapl/quote').json()['iexRealtimePrice']
		self.assertEqual(get_current_share_price('aapl'), output)
	
	def test_invalid_param_get_month_chart(self):
		'''
		Test if an invalid parameter is correctly rejected
		'''
		self.assertEqual(get_month_chart('AAPL', 5), '5 is not a valid time period')
	
	def test_invalid_param_get_day_chart(self):
		'''
		Test if an invalid parameter is correctly rejected
		'''
		self.assertEqual(get_day_chart('MSFT', 4), '4 is not a valid time period')
	
	def test_invalid_symbol(self):
		'''
		Test that a non-existent symbol is rejected with an appropriate message
		'''
		self.assertEqual(process_api_call("https://api.iextrading.com/1.0/stock/IHDIHISB/quote"), "This stock is not listed on our system")
		
		
if __name__ == '__main__':
	ut.main()