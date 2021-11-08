# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 08:29:16 2021

@author: Matt
"""

## Package Usage ##

import requests
import pandas as pd
import json
from pycoingecko import CoinGeckoAPI
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

## Coin Gecko API ##
cg = CoinGeckoAPI()

## Connect to Slack ##
slack_client = WebClient(token='')

## Define Slack Token ##
def slack_trigger(slack_chat):
    try:
        response = slack_client.chat_postMessage(channel='#demo', text=slack_chat,username = "python_bot")
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")  
    
## ThorSwap Exchange ##
thorswap_base = "https://midgard.thorchain.info/v2/"
thorswap_pool = "pool/"
bch_token = "BCH.BCH"

def thorswap_api(token,datatype):
    thorswap_api = thorswap_base + thorswap_pool + token
    thorswap_get = requests.get(thorswap_api)
    thorswap_json = json.loads(thorswap_get.text)
    thorswap_price = thorswap_json['assetPriceUSD']
    if datatype == "json":
        return(thorswap_json)
    else:
        return(float(thorswap_price))


## PancakeSwap ##
bch_token_id = '0x8ff795a6f4d97e7887c79bea79aba5cc76444adf'

def pancake_api(token_id):
    pancake_api = "https://api.pancakeswap.info/api/v2/tokens/"
    pancake_get = requests.get(url = pancake_api + token_id)
    pancake_dict = json.loads(pancake_get.text)
    pancake_price = pancake_dict['data']['price']
    return(float(pancake_price))


bot_timer = 11

for time_int in range(bot_timer):
    thorswap_exchange_price = float(thorswap_api(bch_token,'price'))
    pancake_exchange_price = float(pancake_api(bch_token_id))
    exchange_delta = abs(thorswap_exchange_price - pancake_exchange_price)
    slack_verbage = "Difference is $" + str(exchange_delta)
    print(slack_verbage)
    time.sleep(2)



