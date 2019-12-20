#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Requires python-requests. Install with pip:
#
#   pip install requests
#
# or, with easy-install:
#
#   easy_install requests

import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase


# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key,pass_word):
        self.api_key = api_key
        self.secret_key = secret_key
        self.pass_word=pass_word
    def __call__(self, request):
        print(self.api_key)
        print(self.secret_key)

        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = self.secret_key
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'Content-Type': 'application/json',
            'OK-ACCESS-PASSPHRASE':self.pass_word
        })
        return request


API_KEY_3 = "4244c1fb-f4e2-4a25-97b4-91ef45d2fd00"
API_SECRET_3 = "BF72805249AD14CC87B852F4A99447E7"
AUTH_3 = CoinbaseExchangeAuth(API_KEY_3, API_SECRET_3)

API_KEY_4 = "f01629ef-73db-11e4-a9e3-c86000d26d7c"
API_SECRET_4 = "19535CF3D949D4EF56F8D3D4ED78C505"
AUTH_4 = CoinbaseExchangeAuth(API_KEY_4, API_SECRET_4)

API_URL = 'http://192.168.80.60:8814/api/spot/v3'

PRODUCT_ID = ("BCH_BTC", "BCS_BTC", "LTC_BTC", "ETH_BTC", "ETC_BTC", "ETH_USDT", "BTC_USDT")
def getHelper(method, auth=AUTH_3):
    r = requests.get(API_URL + method, auth=auth)
    print(("response status: ", r.status_code, "response json: ", r.json()))
def postHelper(method, body={}, auth=AUTH_3):
    r = requests.post(API_URL + method, json=body, auth=auth)
    print(("response status: ", r.status_code, "response json: ", r.json()))
def deleteHelper(method, body={}, auth=AUTH_3):
    r = requests.delete(API_URL + method, json=body, auth=auth)
    print(("response status: ", r.status_code, r.content))
# 行情
def testTicker():
    for p in PRODUCT_ID:
        method = "/products/" + p + "/ticker"
        getHelper(method)


# 深度信息
def testBook():
    for p in PRODUCT_ID:
        method = "/products/" + p + "/book"
        getHelper(method)


# 获取 server time
def testGetServerTime():
    method = "/time"
    getHelper(method)


# 获取币对信息
def testProducts():
    method = "/products"
    getHelper(method)

# 行情信息
def testTrades():
    for p in PRODUCT_ID:
        method = "/products/" + p + "/trades?before=10&limit=10"
        getHelper(method)

# kline 信息
def testCandles():
    for p in PRODUCT_ID:
        method = "/products/" + p + "/candles?type=1min&start=2018-01-30T13:08:00Z&end=2018-01-31T13:08:00Z"
        getHelper(method)

# 获取账户信息
def testAccount():
    method = "/accounts"
    getHelper(method, auth=AUTH_4)

# 下单
def testOrder():
    method = "/order"
    # limit sell
    body_limit_sell = {
        'product_id': PRODUCT_ID[0],
        'side': 'sell',
        'type': 'limit',
        'size': '1',
        'price': '10'
    }
    # postHelper(method, body=body_limit_sell)
    # limit buy
    body_limit_buy = {
        'product_id': PRODUCT_ID[0],
        'side': 'buy',
        'type': 'limit',
        'size': '1',
        'price': '10'
    }
    #  postHelper(method, body=body_limit_buy, auth=AUTH_4)

    body_market_sell = {
        'product_id': PRODUCT_ID[0],
        'side': 'sell',
        'type': 'market',
        'size': '100',
        'funds': '10'
    }
    postHelper(method, body=body_market_sell)

    body_market_buy = {
        'product_id': PRODUCT_ID[0],
        'side': 'buy',
        'type': 'market',
        'size': '100',
        'funds': '10'
    }
    postHelper(method, body=body_market_buy, auth=AUTH_4)

# 通过订单id取消订单
def testCancelByOrderId():
    orderId = '6682';
    method = "/orders/" + orderId
    body = {
        'product_id': PRODUCT_ID[0]
    }
    deleteHelper(method, body=body, auth=AUTH_4)

# 取消所有订单，目前逻辑最多取消 50 条
def testCancelAll():
    method = "/orders"
    body = {
        'product_id': PRODUCT_ID[0]
    }
    deleteHelper(method, body=body)

# 通过订单 id 获取订单
def testGetOrderById():
    method = "/orders/6682?product_id=" + PRODUCT_ID[0]
    getHelper(method)

# 获取历史订单 status 只能为 pending、done
def testGetOrderAll():
    method = "/orders?product_id=" + PRODUCT_ID[1] + "&status=pending&current_page=1&page_length=10"
    getHelper(method)

#testTicker()
testBook()
# testGetServerTime()
# testProducts()
# testTrades()
# testCandles()
# testAccount()
# testOrder()
# testCancelByOrderId()
# testCancelAll()

# testGetOrderById()
# testGetOrderAll()
