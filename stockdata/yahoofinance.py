import requests
import json

YAHOO_PUB_API_URL = "https://query.yahooapis.com/v1/public/yql?"
YAHOO_ALL_ENV = "http://datatables.org/alltables.env"
class Base():
    def __init__(self, symbol):
        self.symbol = symbol

    def _build_query(self, table, key):
        base = "SELECT * FROM yahoo.finance.{table} WHERE {key} = {symbol}"
        self.query = base.format(table=table, key=key, symbol=self.symbol)
        return self.query

    def execute_query(self, query, format, ):



class Quote(Base):

    def __init__(self, symbol):
        super(Quote, self).__init__(symbol)
        self.table = "quotes"
        self.key = "symbol"



    def update(self):
        pass

class Currency(Base):
    def __init__(self, symbol):
        super(Currency, self).__init__(symbol)