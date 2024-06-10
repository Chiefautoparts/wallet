import requests
import json
import time
import hmac
import hashlib
from django.conf import settings

GEMINI_API_KEY = 'master-uu3YZeMptV08Xa7XSq13'
GEMINI_API_SECRET = 'ur8YRswZpzkXkofMCftdUDGEYya'

def gemini_request(endpoint, payload):
	base_url = 'https://api.gemini.com'
	url = base_url + endpoint
	payload['request'] = endpoint
	payload['nonce'] = int(timei.time() * 1000)
	payload = json.dumps(payload)
	b64 = base64.b64encode(paylaod.encode())
	signature = hmac.new(GEMINI_API_SECRET.encode(), b64, hashlib.sha384).hexdigest()

	headers = {
		'Content-Type': 'text/plain',
		'Content-Length': 0,
		'X-GEMINI-APIKEY': GEMINI_API_KEY,
		'X-GEMINI-PAYLOAD': b64,
		'X-GEMINI-SIGNATURE': signature,
	}

	response = request.post(url, headers=headers)
	return response.json()

def get_bitcoin_price():
	response = requests.get('https://api.gemini.com/v1/pubticker/btcusd')
	return response.json()['last']