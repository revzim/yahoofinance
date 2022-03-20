import time
import os
import datetime
import urllib.request
import json

class YahooFinance:

  def __init__(self):
    self.__rtd_url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%s"
    self.__chart_url = "https://query2.finance.yahoo.com/v8/finance/chart/%s?range=%s&interval=1d"
    self.__settings = Settings()
    self.data = {}

  def get_rtd_url(self):
    return self.__rtd_url

  def get_chart_url(self):
    return self.__chart_url

  def get_quote(self, name):
    url = self.__rtd_url % (name)
    resp = urllib.request.urlopen(url).read()
    return json.loads(resp.decode('utf-8'))['quoteResponse']

  def get_quote_range(self, name, qrange):
    url = self.__chart_url % (name, qrange)
    resp = urllib.request.urlopen(url).read()
    return json.loads(resp.decode('utf-8'))

  def read_json(self, name):
    f = open("%s.json" % (name), "r")
    return json.loads(f.read())

  def write_file(self, name, data):
    try:
      os.mkdir("data")
    except FileExistsError:
      print("\ndata directory already exists...\n\nskipping...\n")
    with open('data/%s.json' % (name), 'x', encoding='utf-8') as f:
      json.dump(data, f)

  def parse_cquery(self, data, qrange, write):
    datadict = {}
    chart = data['chart']
    result = chart['result'][0]
    datadict['meta'] = result['meta']
    datadict['symbol'] = result['meta']['symbol']
    datadict['timestamps'] = result['timestamp']
    indicators = result['indicators']
    quotes = indicators['quote']
    adjcloses = indicators['adjclose']
    datadict['market_price'] = datadict['meta']['regularMarketPrice']
    for quote in quotes:
      datadict['close'] = quote['close']
      datadict['open'] = quote['open']
      datadict['low'] = quote['low']
      datadict['high'] = quote['high']
      datadict['volume'] = quote['volume']
    
    for adjclose in adjcloses:
      datadict['adjclose'] = adjclose['adjclose']

    stockdata = []
    
    for i in range(len(datadict['close'])):  
      stockdata.append(
        Stockquote(
          datadict['symbol'],
          datetime.datetime.fromtimestamp(datadict['timestamps'][i]).strftime('%Y_%m_%d'),
          datadict['open'][i],
          datadict['close'][i],
          datadict['high'][i],
          datadict['low'][i],
          datadict['volume'][i],
          datadict['adjclose'][i],
          datadict['timestamps'][i])
        )
    if write is True:
      self.write_file('%s_%s_r%s'
        % (datadict['symbol'], int(time.time()), qrange),
        list(map(lambda x: x.get_data(), stockdata)))
    return stockdata

  def get_stock_data(self, name, qrange, write):
    return self.parse_cquery(self.get_quote_range(name, qrange), qrange, write)

  def get_market_price(self, name, verbose=False):
    datadict = {}
    result = self.get_quote(name)['result'][0]
    datadict['meta'] = {}
    for key in result.keys():
      if "regularMarketPrice" in key:
        if not verbose:
          return result[key]
        datadict["currentprice"] = result[key]
      if "regular" in key:
        datadict[key] = result[key]
      else:
        datadict['meta'][key] = result[key]
    self.data[name] = datadict
    return datadict


class Settings:
  def __init__(self):
    self.__ranges = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

  def ranges(self):
    return self.__ranges

class Stockquote:
  def __init__(self, symbol, date, sopen, close, high, low, volume, adjclose, timestamp):
    self.symbol = symbol
    self.date = date
    self.open = sopen
    self.close = close
    self.high = high
    self.low = low
    self.volume = volume
    self.adjclose = adjclose
    self.timestamp = timestamp

  def get_json(self):
    return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2)

  def get_data(self):
    return self.__dict__

