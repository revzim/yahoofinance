#!/usr/local/bin/python3
import json

import yahoo

yf = yahoo.YahooFinance()

data_file_name = "data/AMD_1596056711_r3mo"

testdata = yf.read_json(data_file_name)

def get_lists(data):
  datadict = {}
  keys = list(data[0].keys())
  for i in range(len(keys)):
    datadict[keys[i]] = []
    for j in range(len(data)):
      datadict[keys[i]].append(data[j][keys[i]])
  return datadict

def parse_to_list(key, data=testdata):
  return list(map(lambda x: x[key], data))

def avg(data_list):
  return sum(data_list) / len(data_list)

def increased(a, b):
  if a < b:
    return "+"
  return "-"

def simple_chart(key, l):
  last = datalists[key][0]
  flow = str()
  for val in datalists[key]:
    flow += increased(last, val)
  return flow

# PARSE_TO_LIST EXAMPLE
  # print("PARSE_TO_LIST EXAMPLE START...\n")
  # close_list = parse_to_list("close")
  # open_list = parse_to_list("open")
  # high_list = parse_to_list("high") 
  # low_list = parse_to_list("low")
  # print("PARSE_TO_LIST EXAMPLE END...\n")

# GET_LISTS EXAMPLE
  # print("GET_LISTS EXAMPLE START...\n")
  # print(get_lists(testdata))
  # print("GET_LISTS EXAMPLE START...\n")

# GET_CHART EXAMPLE
print("GET_CHART EXAMPLE START...\n")
datalists = get_lists(testdata)
print(f"OPEN:       {simple_chart('open', datalists)}\n")
print(f"CLOSE:      {simple_chart('close', datalists)}\n")
print(f"ADJCLOSE:   {simple_chart('adjclose', datalists)}\n")
print(f"HIGH:       {simple_chart('high', datalists)}\n")
print(f"LOW:        {simple_chart('low', datalists)}\n")
print(f"VOLUME:     {simple_chart('volume', datalists)}\n")
print(f"TIMESTAMPS: {simple_chart('timestamp', datalists)}\n")
print("\nGET_CHART EXAMPLE END...")