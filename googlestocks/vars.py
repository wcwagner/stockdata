"""
Queries to Googles Finance REST API return JSON objects with abbreviated keys.
In this file are the corresponding verbose keys, which are used to convert the
keys to their more verbose form.
"""
_NEWS_KEYMAP = {
    "a": "clusteredArticles",
    "d": "dateTime",
    "s": "source",
    "t": "title",
    "tt": "titleId",
    "u": "url",
    "sp": "openingSentence"
}

_QUOTES_KEYMAP = {
    "t": "symbol",
    "e": "exchange",
    "l": "lastPrice",
    "l_cur": "lastTradeWithCurrency",
    "ltt": "lastTradeTime",
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

_OPTONS_KEYMAP = {
    "c": "change",
    "cp": "changePercentage",
    "vol": "volume",
    "e": "exchange",
    "a": "ask",
    "b": "bid",
    "oi": "openInterest"
}

_NEWS_BASE_URL = "http://www.google.com/finance/company_news?output=json" \
               "&q={0}&num={1}&start={2}"

_QUOTES_BASE_URL = "http://finance.google.com/finance/" \
              "info?client=ig&q={0}%3A{1}"

_OPTIONS_BASE_URL = "http://www.google.com/finance/option_chain?q={0}&" \
                    "output=json"