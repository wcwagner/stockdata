import demjson
import requests
import sys
from .vars import (_NEWS_KEYMAP, _OPTONS_KEYMAP, _QUOTES_KEYMAP,
                   _GOOGLE_NEWS_BASE_URL, _GOOGLE_OPTIONS_BASE_URL, _GOOGLE_QUOTES_BASE_URL)

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
    url = _build_url(_GOOGLE_NEWS_BASE_URL, symbol, num_articles, start)
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
    url = _build_url(_GOOGLE_QUOTES_BASE_URL, symbols, exchange)
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
    url = _build_url(_GOOGLE_OPTIONS_BASE_URL, symbol)
    json_str = _get(url).text
    options_json = demjson.decode(json_str)
    _conv_options_keys(options_json)
    return options_json

class Share():
    def __init__(self, stock_symbol):
        self.stock_symbol = stock_symbol
        self.data = get_quotes(self.stock_symbol)[self.stock_symbol]

    def __repr__(self):
        return "Share({0})".format(self.stock_symbol)

    def __str__(self):
        ret = "Stock: {symbol}\nTrading At: {price}\nChange(%): " \
              "{change}".format(symbol = self.symbol, price=self.price,
                                change=self.change_percent)

        return ret

    def refresh(self):
        self.data = get_quotes(self.stock_symbol)[self.stock_symbol]

        
    @property
    def after_hours_trade_time(self):
        return self.data['afterHoursLastTradeTime']

    @property
    def after_hours_last_price(self):
        return self.data['afterHoursLastPrice']

    @property
    def after_hours_change(self):
        return self.data['afterHoursChange']

    @property
    def change(self):
        return self.data['change']

    @property
    def change_percent(self):
        return self.data['changePercentage']

    @property
    def dividend(self):
        return self.data['dividend']

    @property
    def dividend_yield(self):
        return self.data['dividendYield']

    @property
    def exchange(self):
        return self.data['exchange']

    @property
    def last_trade_datetime(self):
        return self.data['lastTradeDateTime']

    @property
    def last_trade_with_currency(self):
        return self.data['lastTradeWithCurrency']

    @property
    def last_trade_size(self):
        return self.data['lastTradeSize']

    @property
    def symbol(self):
        return self.data['symbol']


    @property
    def price(self):
        return self.data['price']

    @property
    def volume(self):
        return self.data['volume']








