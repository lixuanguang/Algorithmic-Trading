# Specify project path
import sys
import os

path = os.path.abspath(os.getcwd())
sys.path.append(path)


# Retrieve stock ticker
import yfinance as yf

acwi = yf.Ticker("ACWI")

hist = acwi.history(period="max")

hist.to_csv("ACWI.csv")