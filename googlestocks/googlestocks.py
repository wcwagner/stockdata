import demjson
import requests
import sys
from .vars import (_NEWS_KEYMAP, _OPTONS_KEYMAP, _QUOTES_KEYMAP,
                   _NEWS_BASE_URL, _OPTIONS_BASE_URL, _QUOTES_BASE_URL)





class GoogleFinanceAPI():

    def __init__(self):
        pass
    def _build_url(self, base_url, *args):
        return base_url.format(*args)

    def _conv_keys_with_keymap(self, json_obj, key_map):
        """
        If a key in a dictionary appears in the `key_map`, it will be converted
        IN PLACE to it's corresponding value in key_map
        """
        for old_key, new_key in key_map.items():
            if old_key in json_obj:
                json_obj[new_key] = json_obj[old_key]
                del json_obj[old_key]

    def _conv_news_keys(self, json_objs):
        """
        In place conversion of the JSON objects' keys to make them more verbose
        e.g. "s" --> "source"
        """
        for outer_json in json_objs:
            self._conv_keys_with_keymap(outer_json, _NEWS_KEYMAP)
            if 'clusteredArticles' in outer_json:
                for article_json in outer_json['clusteredArticles']:
                    self._conv_keys_with_keymap(article_json, _NEWS_KEYMAP)

    def _conv_quote_keys(self, quotes_json):
        """
        Converts the short abbreviated keys of the stock quote object to the more
        verbose form e.g. "t" --> "ticker"
        """
        print("BEFORE", quotes_json)
        for quote in quotes_json:
            self._conv_keys_with_keymap(quote, _QUOTES_KEYMAP)
        print("\n---------------------\nAFTER", quotes_json)

    def _get(self, url):
        """
        Performs a request of the passed in url and returns the text
        """
        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
        return resp.text

    def get_news(self, symbol, num_articles=100, start=0):
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
        url = self._build_url(_NEWS_BASE_URL, symbol, num_articles, start)
        json_str = self._get(url)
        # need demjson's decode, json data is invalid for pythons native decoder
        news_json = demjson.decode(json_str)['clusters']
        # make keys verbose
        self._conv_news_keys(news_json)
        return news_json


    def get_quotes(self, symbols, exchange="NASDAQ"):
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
        if not isinstance(symbols, str):
            symbols = ",".join(symbols)
        url = self._build_url(_QUOTES_BASE_URL, symbols, exchange)
        json_str = self._get(url)
        quotes_json = demjson.decode(json_str[3:])
        self._conv_quote_keys(quotes_json)
        return {quote["ticker"]: quote for quote in quotes_json}

    def get_options(self, symbol):
        url = self._build_url(_OPTIONS_BASE_URL, symbol)
        return url

