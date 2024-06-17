import requests
import json
import time
import hmac
import hashlib
import base64
from django.conf import settings

GEMINI_API_KEY = 'master-dLtrpKLjR0hexbfDhRTH'
GEMINI_API_SECRET = '46svLhhnwHo97p6XVX4Sk6Y56qXA'

def gemini_request(endpoint, payload):
	base_url = "https://api.gemini.com"
	url = base_url + endpoint
	payload['request'] = endpoint
	payload['nonce'] = int(time.time() * 1000)
	paylaod = json.dumps(payload)
	b64 = base64.b64encode(payload.encode())
	signature = hmac.new(GEMINI_API_SECRET.encode(), b64, hashlib.sha384).hexdigest()

	headers = {
		'Content-Type': 'text/plain',
		'Content-Length': '0',
		'x-GEMINI-APIKEY0': GEMINI_API_KEY,
		'X-GEMINI-PAYLOAD': b64,
		'X-GEMINI-SIGNATURE': signature,	
	}

	response = requests.post(url, headers=headers)
	return response.json()

def get_bitcoin_price():
	response = requests.get('https://api.gemini.com/v1/pubticker/btcusd')
	data = response.json()
	return data['last']