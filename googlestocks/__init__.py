import json

import demjson
import requests
import sys

NEWS_KEYMAP = {
    "a": "clusteredArticles",
    "d": "dateTime",
    "s": "source",
    "t": "title",
    "tt": "titleId",
    "u": "url",
    "sp": "openingSentence"
}
QUOTES_KEYMAP = {
    "t": "ticker",
    "e": "exchange",
    "l": "lastPrice",
    "l_cur": "lastTradeWithCurrency",
    "ltt": "lastTradeTime",
    "l": "price",
    "lt": "lastTradeTime",
    "lt_dts": "lastTradeDateTime",
    "c": "change",
    "cp": "changePercentage",
    "ec": "afterHoursChange",
    "el": "afterHoursLastPrice",
    "elt": "afterHoursLastTradeTime",
    "div": "dividend",
    "s": "lastTradeSize",
    "pcls_fix": "lastClosePrice",
    "yld": "dividendYield"
}


def _build_quote_url(symbols, exchange):
    """
    Builds a url for querying googles REST based API. The format of the url is
    http://finance.google.com/finance/info?client=ig&q=NASDAQ%3A{SYMBOLS}
    where {SYMBOLS} is a comma seperated list of symbols
    """
    if not isinstance(symbols, str):
        symbols = ",".join(symbols)
    url = "http://finance.google.com/finance/" \
          "info?client=ig&q={0}%3A{1}".format(exchange, symbols)
    return  url

def _conv_quote_keys(json_obj):
    """
    Converts the short abbreviated keys of the stock quote object to the more
    verbose form e.g. "t" --> "ticker"
    """
    return _conv_keys_with_keymap(json_obj, QUOTES_KEYMAP)


def get_quotes(symbols, exchange="NASDAQ"):
    """
    Queries the google finance API and returns the stock quotes for the symbol(s)
    passed in

    Parameters
    ----------
    symbols: str or list like
        The stock ticker symbol you want quotes for e.g. GOOG
    exchange: str, optional
        The exchange you want the quote data from, the default is NASDAQ
    Returns
    -------
    stock_quotes : dictionary
        Dictionary where keys are the stock symbols passed in, and the values are
        the quote in the form of a JSON object
    
    """
    url = _build_quote_url(symbols, exchange)
    try:
        req = requests.get(url)
        req.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    stock_data = req.text
    json_objs = demjson.decode(stock_data[3:])
    for json_obj in json_objs:
        _conv_quote_keys(json_obj)
    return {json_obj["ticker"]:json_obj for json_obj in json_objs}

def _build_news_url(symbol, num_articles, start):
    return "http://www.google.com/finance/company_news?output=json"\
            "&q={0}&num={1}&start={2}".format(symbol, num_articles, start)

def get_news(symbol, num_articles=100, start=0):
    """
    Queries the google finance API and returns news articles related to a certain
    stock.

    Parameters
    ----------
    symbol : str
        The stock ticker symbol you want news articles for
    num_articles : int, optional
        The number of articles you want, the default is 100
    start : int, optional
        The start point in the news stream where you want your article(s)
        returned from
    Returns
    -------
    A array of JSON objects, where each JSON object contains a cluster of
    articles all relating to a similar subject.
    """
    url = _build_news_url(symbol, num_articles, start)
    try:
        req = requests.get(url)
        req.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    # need demjson's decode, json data is invalid for pythons native decoder
    news_data = demjson.decode(req.text)['clusters']
    _conv_news_keys(news_data)
    return news_data

def _conv_keys_with_keymap(json_obj, key_map):
    """
    If a key in a dictionary appears in the `key_map`, it will be converted
    IN PLACE to it's corresponding value in key_map (key_map[key])
    """
    for old_key, new_key in key_map.items():
        if old_key in json_obj:
            json_obj[new_key] = json_obj[old_key]
            del json_obj[old_key]

def _conv_news_keys(json_objs):
    """
    In place conversion of the JSON objects' keys to make them more verbose
    e.g. "s" --> "source"
    """
    for outer_json in json_objs:
        _conv_keys_with_keymap(outer_json, NEWS_KEYMAP)
        if 'clusteredArticles' in outer_json:
            for article_json in outer_json['clusteredArticles']:
                _conv_keys_with_keymap(article_json, NEWS_KEYMAP)

