import requests
import json
import time
import warnings
YAHOO_PUB_API_URL = "https://query.yahooapis.com/v1/public/yql?"
YAHOO_ALL_ENV = "store://datatables.org/alltableswithkeys"


def _request(url, payload):
    """
     Performs a request of the passed in url, if the url is bad then the error
     is printed
     """
    try:
        resp = requests.get(url, params=payload)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)

    return resp

def _build_query(symbols, table, key):
    YQL_BASE = "SELECT * FROM yahoo.finance.{table} WHERE {key} IN {symbols}"
    query = YQL_BASE.format(table=table, key=key, symbols=symbols)
    return query

def get_quote(*symbols):
    """
    Parameters
    ----------
    symbols:

    Returns
    -------
    """
    if len(symbols) == 0:
        raise ValueError("Must pass in at least one symbol")
    elif len(symbols) == 1:
        # tuples w/ one element have trailing comma, must truncate
        symbols="('{0}')".format(symbols[0])
    yql_query = _build_query(symbols=symbols, table="quote", key="symbol")
    payload = {"q": yql_query,
              "format": "json",
              "env": YAHOO_ALL_ENV}
    quote = json.loads(_request(YAHOO_PUB_API_URL, payload).text)
    return quote['query']['results']['quote']

class Quote():

    def __init__(self, symbol):
        self.data = get_quote(symbol)

    @property
    def average_daily_volume(self):
        return self.data['AveragedDailyVolume']

    @property
    def change(self):
        return self.data['Change']

    @property
    def days_high(self):
        return self.data['DaysHigh']

    @property
    def days_low(self):
        return self.data['DaysLow']

    @property
    def days_range(self):
        return self.data['DaysRange']

    @property
    def price(self):
        return self.data['LastTradePriceOnly']

    @property
    def market_cap(self):
        return self.data['MarketCapitalization']

    @property
    def name(self):
        return self.data['Name']

    @property
    def exchange(self):
        return self.data['StockExchange']

    @property
    def symbol(self):
        return self.data['Symbol']

    @property
    def volume(self):
        return self.data['Volume']

    @property
    def year_high(self):
        return self.data['YearHigh']

    @property
    def year_low(self):
        return self.data['YearLow']

    def refresh(self):
        self.data = get_quote(self.symbol)

    def set_alert(self, threshold):
        last_price = float(self.price)
        pct_change = 0
        while True:
            time.sleep(1)
            self.refresh()
            pct_change = (last_price / float(self.price)) * 100.0
            if pct_change > threshold:
                print("{0}'s price has changed "
                      "more than {1}%".format(self.symbol, threshold))



class Currency():
    def __init__(self, symbol):
        super(Currency, self).__init__(symbol)