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
	date = (dt.datetime.now() - dt.timedelta(days=14)).date()
	base = "https://newsapi.org/v2/everything"
	
	payload = {'apiKey' : 'ca4b323cc91f4bf0a4da4f28f70f26f5', 'q' : company, 'sortBy' : 'popularity', 'from' : date} 
	
	response = requests.get(base, params=payload)
	
	return response.json()

print(get_general_headlines())