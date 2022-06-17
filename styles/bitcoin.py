import schedule
import time

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import http.client, urllib

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'coinmarketcapkey',
}
session = Session()
session.headers.update(headers)

def func():
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        tether = [d for d in data["data"] if d['slug'] == 'tether'][0]
        price = tether["quote"]["USD"]["price"]
        message = f"Tether: ${price} - Price is under 99.5 cents!"

        print(f"Tether: ${price}")
        if price < 0.995:
            conn = http.client.HTTPSConnection("api.pushover.net:443")
            conn.request("POST", "/1/messages.json",
            urllib.parse.urlencode({
                "token": "pushover-app-token",
                "user": "pushover-user-token",
                "message": message,
            }), { "Content-type": "application/x-www-form-urlencoded" })
            conn.getresponse()

        btc = [d for d in data["data"] if d['slug'] == 'bitcoin'][0]
        price = btc["quote"]["USD"]["price"]
        message = f"BTC: ${price} - Price is under 21000!"

        print(f"BTC: ${price}")
        if price < 20000:
            conn = http.client.HTTPSConnection("api.pushover.net:443")
            conn.request("POST", "/1/messages.json",
            urllib.parse.urlencode({
                "token": "pushover-app-token",
                "user": "pushover-user-token",
                "message": message,
            }), { "Content-type": "application/x-www-form-urlencoded" })
            conn.getresponse()

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

schedule.every(5).minutes.do(func)
  
while True:
    schedule.run_pending()
    time.sleep(5)