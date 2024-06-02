import requests

def get_bitcoin_price():
	url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
	response = requests.get(url)
	if response.status_code == 200:
		data = response.json()
		return data['bitcoin']['usd']
	return None