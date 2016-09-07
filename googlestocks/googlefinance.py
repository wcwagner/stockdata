import demjson
import requests
import sys
from .vars import (_NEWS_KEYMAP, _OPTONS_KEYMAP, _QUOTES_KEYMAP,
                   _NEWS_BASE_URL, _OPTIONS_BASE_URL, _QUOTES_BASE_URL)


def _build_url(base_url, *args):
    """ formats a string based on the parameters passed in"""
    return base_url.format(*args)

def _conv_keys_with_keymap(json_obj, key_map):
    """
    If a key in a dictionary appears in the `key_map`, it will be converted
    IN PLACE to it's corresponding value in key_map
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
        _conv_keys_with_keymap(outer_json, _NEWS_KEYMAP)
        if 'clusteredArticles' in outer_json:
            for article_json in outer_json['clusteredArticles']:
                _conv_keys_with_keymap(article_json, _NEWS_KEYMAP)

def _conv_quote_keys(quotes_json):
    """
    Converts the short abbreviated keys of the stock quote object to the more
    verbose form e.g. "t" --> "ticker"
    """
    for quote in quotes_json:
        _conv_keys_with_keymap(quote, _QUOTES_KEYMAP)

def _conv_options_keys(options_json):

    for type in ['puts', 'calls']:
        if type in options_json:
            for option in options_json[type]:
                _conv_keys_with_keymap(option, _OPTONS_KEYMAP)


def _get(url):
    """
    Performs a request of the passed in url, if the url is bad then the error
    is printed and the program exits
    """
    try:
        resp = requests.get(url)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    return resp

def get_news(symbol, num_articles=100, start=0):
    """
    Queries the google finance API and returns a JSON object of news articles
    related to the stock symbol passed in.

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
    url = _build_url(_NEWS_BASE_URL, symbol, num_articles, start)
    json_str = _get(url).text
    # need demjson's decode, json data is invalid for pythons native decoder
    news_json = demjson.decode(json_str)['clusters']
    # make keys verbose
    _conv_news_keys(news_json)
    return news_json


def get_quotes(symbols, exchange="NASDAQ"):
    """
    Queries the google finance API and returns the stock quotes, formatted in
    JSON, for the symbol(s) passed in

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
        the quote(s) in the form of a JSON object

    """

    #multiple symbols, convert to comma seperated list
    if not isinstance(symbols, str):
        symbols = ",".join(symbols)
    url = _build_url(_QUOTES_BASE_URL, symbols, exchange)
    json_str = _get(url).text
    quotes_json = demjson.decode(json_str[3:])
    _conv_quote_keys(quotes_json)
    return {quote["symbol"]: quote for quote in quotes_json}

def get_options(symbol):
    """
       Queries the google finance API and returns the options data, formatted
       in JSON, for the  symbol passed in

       Parameters
       ----------
       symbols: str or list like
           The stock ticker symbol you want options for e.g. GOOG

       Returns
       -------
       options_json : JSON object
           JSON object that has a 'puts' and 'calls' property corresponding to all
           options of that type.
           Each individual option has properties
           ["ask", "bid", "change", "changePercentage", "volume", "exchange",
            "openInterest"]
    """
    url = _build_url(_OPTIONS_BASE_URL, symbol)
    json_str = _get(url).text
    options_json = demjson.decode(json_str)
    _conv_options_keys(options_json)
    return options_json
