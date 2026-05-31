import requests


try:
    prices=requests.get('http://api.navasan.tech/latest/?api_key=freelerlC92tDxdOmgE2sO9Bj7v4yGu7')
    dict_prices=eval(prices.text)
except Exception:
    dict_prices={
        'usd':{
            'value':'50000'
            }
        }

usd_dollar_price=float(dict_prices['usd']['value'])

