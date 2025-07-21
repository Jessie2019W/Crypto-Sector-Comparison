# config.py

import time
import datetime

import pandas as pd

import os

IS_PRO_USER = False  # True if with a paid API plan
API_BASE = "https://api.coingecko.com/api/v3"
PRO_API_BASE = "https://pro-api.coingecko.com/api/v3"
API_KEY = "CG-xxxxxxxxxxxxxx"  # API KEY with paid plan

START_DATE = datetime.date(2025,7,1) 
END_DATE = datetime.datetime.now(datetime.UTC).date() - datetime.timedelta(days=1)

days = (END_DATE - START_DATE).days

# Select categories based on their market cap's rank
START_RANK = 1
END_RANK = 5

# Specific categories to compare in the plot
INCLUDE_SECTORS = ['DePIN','Meme','Layer 1 (L1)','Liquid Staking','Real World Assets (RWA)','Restaking']  
# INCLUDE_SECTORS = ['Proof of Stake (PoS)']  
EXCLUDE_SECTORS = ['Stablecoins', 'USD Stablecoin']

# Drop categories with small market cap
MIN_MARKET_CAP = 1_000_000

WEIGHTED_PRICE_BASE = 100

FREE_USER_PER_PAGE = 20





