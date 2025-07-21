# # =========================CoinGecko API============================

# data_fetcher.py

import requests
from config.config import *
from requests import Session




def get_sector_list():
    '''
    Get all categroies' id, name, market cap sorted by market cap 
    '''
    url = f"{API_BASE}/coins/categories"
    response = requests.get(url)
    
    if response.status_code == 200:
        print(f"Successful to get category list.")

        return response.json()
    
    else:
        print(f"Error getting category list: {response.status_code}")
        return None


def get_token_list(sector_id):
    """
    Get the list of all tokens under a specific sector.
    - Free users only retrieve the first a few tokens (up to 100);
    - Paid users use PRO_API_BASE and retrieve all data through pagination.
    """
    base_url = PRO_API_BASE if IS_PRO_USER else API_BASE
    
    headers = {
    "accept": "application/json",
    "x-cg-pro-api-key": API_KEY
    } if IS_PRO_USER else {}
    
    per_page = 100 if IS_PRO_USER else FREE_USER_PER_PAGE

    page = 1
    all_tokens = []

    while True:
        url = f"{base_url}/coins/markets"
        params = {
            "vs_currency": "usd",
            "category": sector_id,
            "order": "market_cap_desc",
            "per_page": per_page,
            "page": page
        }

        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code != 200:
            print(f"[ERROR] Failed to fetch token list for sector {sector_id}: {response.status_code}")
            return all_tokens if IS_PRO_USER else []  

        tokens = response.json()
        all_tokens.extend(tokens)
        print(f"Completed retrieval of tokens in page {page} under {sector_id} sector")

        # For free user 
        if not IS_PRO_USER:
            print(f"Free users only take first {per_page} tokens under a sector")
            break

        # For paid user, If the result is less than  per_page, all data has been obtained
        if len(tokens) < per_page:
            print(f"Completed retrieval of {len(all_tokens)} tokens under {sector_id} sector")
            break
        
        page += 1
    print()
    
    return all_tokens



def get_token_history_data(token_id):
    """
    Get token history daily open price and market cap 
    """
    if IS_PRO_USER:

        # Convert date object to unix timestamp
        from_dt = datetime.datetime(START_DATE.year, START_DATE.month, START_DATE.day, tzinfo=datetime.timezone.utc)
        from_ts = int(from_dt.timestamp())
    
        to_dt = datetime.datetime(END_DATE.year, END_DATE.month, END_DATE.day, tzinfo=datetime.timezone.utc)
        to_ts = int(to_dt.timestamp())
        
        base_url = PRO_API_BASE
        headers = {
        "accept": "application/json",
        "x-cg-pro-api-key": API_KEY
        }

        url = f"{base_url}/coins/{token_id}/market_chart/range"
        params = {
            "vs_currency": "usd",
            "from": from_ts,
            "to":to_ts,
            "interval": "daily"
        }
    else:
        # Wait for rate limit
        time.sleep(20)
        
        base_url = API_BASE
        headers = {}

        url = f"{base_url}/coins/{token_id}/market_chart"
        params = {
            "vs_currency": "usd",
            "days": days,
            "interval": "daily"
        }

    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch token history data for token {token_id} via API: {response.status_code}")
        
        if response.status_code == 429:
            print(f"[ERROR] API rate limit  reached. Consider scaling service plan")
        return None

    return response.json()




    