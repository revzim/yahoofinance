#!/usr/local/bin/python3
import argparse
import time

import yahoo

"""
  ex:
    # HELP
      # python3 main.py -h
        # OR
      # chmod u+rwx main.py
      # ./main.py -h instead of python3 main.py -h
 
    # GET TSLA CURRENT PRICE
      python3 main.py -s tsla

    # SUPPLY A RANGE TO GET QUOTE DATA OVER TIME
      # GET 3 MONTHS WORTH OF AMD TICKER DATA AND WRITE TO FILE
      # DATA SAVED TO: data/<SYMBOL>_<TIME>_r<RANGE>.json
      python3 main.py -r 3mo -s amd -w y
    
"""

start_time = time.time()

parser = argparse.ArgumentParser(description='yahoo finance stock quotes.')

# SYMBOL
parser.add_argument('-s', '--symbol', dest='symbol', default="AMD",
  help='symbol of stock quote desired (default: AMD)')

# RANGE
parser.add_argument('-r', '--range', dest='qrange', default="NONE",
  help='range %s (default: 3mo)' % (yahoo.Settings().ranges()))

# WRITE
parser.add_argument('-w', '--write', dest='write_file', default="n",
  help='if should write query to file or not (default: n <y|n>)')

# TICKRATE
parser.add_argument('-tr', '--tickrate', dest='tick_rate', default=3,
  help='how often we want to query for the current price (default: 3 only fires off if range is NONE )')

# INFINITE
parser.add_argument('-i', '--inf', dest='inf_loop', default="n",
  help='whether current price ticker should continuously run (default: n )')

args = parser.parse_args()

yf = yahoo.YahooFinance()

if args.qrange != "NONE":
  write_to_file = False
  if args.write_file.lower() == 'y':
    write_to_file = True
  print('Querying Yahoo Finance for: %s data with a range of %s...' % (args.symbol, args.qrange))
  print('\nLast value of query:\n\n%s\n' % (yf.get_stock_data(args.symbol, args.qrange, write_to_file)[0].get_json()))
  # for quote in data:
  #     print(quote.get_json())
else:
  print('Querying Yahoo Finance for %s current price every %d seconds.\n' % (args.symbol, int(args.tick_rate)))
  i = 0
  loop_count = 1
  if args.inf_loop == "y":
    loop_count = float('inf')
  for i in range(loop_count):
    loop_start_time = time.time()
    print('Repsonse: %s: $%.02f | Query took %.02fs to complete.\n' % (args.symbol, yf.get_market_price(args.symbol), time.time() - loop_start_time))
    if i != loop_count - 1:
      time.sleep(int(args.tick_rate))
      

print('Query/Response/Save took %.02fs to complete.\n' % (time.time() - start_time))