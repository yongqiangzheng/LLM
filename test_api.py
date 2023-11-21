import requests
import json
from datetime import date, datetime, timedelta
import os

from typing import Optional, Dict, Union, List


def love_quote(quotes: str='random quotes', toolbench_rapidapi_key: str='eae88b5158mshf6e518fc7dd644bp11cb23jsnb7e9ff89ef5d'):
    """
    "It shows random quotes"

    """
    url = f"https://olato-quotes.p.rapidapi.com/love"
    querystring = {}
    if quotes:
        querystring['quotes'] = quotes

    headers = {
            "X-RapidAPI-Key": toolbench_rapidapi_key,
            "X-RapidAPI-Host": "olato-quotes.p.rapidapi.com"
        }


    response = requests.get(url, headers=headers, params=querystring)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation

obs = love_quote()
print(obs)
