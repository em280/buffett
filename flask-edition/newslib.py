'''
Description: Library built to make it simpler to gather news
Version: 1.0
Author: Sean Hamill
'''

import requests
import json
import stocky
import datetime as dt

def get_general_headlines():
	result = requests.get("https://newsapi.org/v2/top-headlines?sources=bloomberg&apiKey=ca4b323cc91f4bf0a4da4f28f70f26f5")
	
	return result.json()
	
def search_headlines(company):
	date = (dt.datetime.now() - dt.timedelta(days=7)).date()
	api_url = requests.get("https://newsapi.org/v2/everything?q={}&sortBy=popularity&from={}&apiKey=ca4b323cc91f4bf0a4da4f28f70f26f5".format(company, date))
	
	return api_url.json()
	
print(search_headlines('apple'))