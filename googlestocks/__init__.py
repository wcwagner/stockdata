import json
import requests


def build_url_from_symbols(symbols):
    """
    Builds a url for querying googles REST based API. The format of the url is
    http://finance.google.com/finance/info?client=ig&q=NASDAQ%3A{SYMBOLS}
    where {SYMBOLS} is a comma seperated list of symbols
    """
    if not isinstance(symbols, str):
        symbols = ",".join(symbols)
    return  "http://finance.google.com/finance/info?client=ig&q=NASDAQ%3A{0}".format(symbols)

def conv_to_json(jstr):
    """
    Google's API returns a string with invalid characters leading and trailing the json str.
    So clean the str, then decode it
    """
    jstr = jstr.replace("\n", "")
    try:
        result = json.loads(jstr[3:])
    except Exception as e:
        print("There was a problem: {0}".format(str(e)))
    return result

def conv_keys(json_obj):
    key_map = {
        "t": "Ticker",
        "e": "Exchange",
        "l": "Last Price",
        "l_cur": "Last Trade With Currency",
        "ltt": "Last Trade Time",
        "l": "Price",
        "lt": "Last Trade Time",
        "lt_dts": "Last Trade Date/Time",
        "c": "Change",
        "cp": "Change Percentage",
        "ec": "After Hours Change",
        "el": "After Hours Last Price",
        "elt": "After Hours Last Trade Time",
        "div": "Dividend",
        "s": "Last Trade Size",
        "pcls_fix": "Last Close Price",
        "yld": "Dividend Yield"
    }
    for key in key_map:
        if key in json_obj:
            json_obj[key_map[key]] = json_obj[key]
            del json_obj[key]
    return json_obj


def get_quotes(symbols):
    """
    Queries the google finance API and returns the stock quotes for the symbol
    passed in

    Parameters
    ----------
    symbols: str or list like
    """
    url = build_url_from_symbols(symbols)
    json_objs = conv_to_json(requests.get(url).text)
    json_objs = {json_obj["Ticker"]:conv_keys(json_obj) for json_obj in json_objs}
    return json_objs

