'''
Description: Library built to send confirmation messages
Version: 1.0
Author: Sean Hamill
'''
from twilio.rest import Client
from random import randint

account_sid = "AC690efb272cc8f1046e5348aeff995c2f"
auth_token  = "f8f68bb21bf58fc98eca556c9bbd0173"

client = Client(account_sid, auth_token)

def send_auth_code():
	auth_code = randint(1000, 9999)
	message = client.messages.create(
		to="+447427039469", 
		from_="+447427564225",
		body="Hey your confirmation number is {}".format(auth_code))

def send_buy_confirmation(symbol, amount):
	message = client.messages.create(
		to="+447427039469",
		from_="+447427564225",
		body="Hey just confirming that, you successfully bought {} shares of {}".format(amount, symbol))


def send_sell_confirmation(symbol, amount):
	message = client.messages.create(
			to="+447427039469",
			from_="+447427564225",
			body="Hey just confirming that, you successfully sold {} shares of {}".format(amount, symbol))
