# data_processor.py

import pandas as pd
from config.config import *
from function.data_fetcher import *


def process_sectors(raw_data):
    
    """
    Filter out unwanted categories
    Keep categories in the INCLUDE_SECTORS and not in the EXCLUDE_SECTORS
    """
    
    sectors = []
    for item in raw_data:
        sector_name = item.get("name")
        market_cap = item.get("market_cap", 0)

        if (
            sector_name in EXCLUDE_SECTORS and sector_name not in INCLUDE_SECTORS 
            or market_cap is None
            or market_cap < MIN_MARKET_CAP
        ):
            continue

        sectors.append({"id": item["id"], "name": sector_name, "market_cap": market_cap})

    sectors_df = pd.DataFrame(sectors)
    sectors_df = sectors_df.sort_values(by="market_cap", ascending=False).reset_index(drop=True)
    
    return sectors_df


def check_include_sectors(sectors_df,INCLUDE_SECTORS):
    
    # Get all sectors name in sectors_df 
    available_sectors = set(sectors_df['name'])
    
    # Check if all INCLUDE_SECTORS is included 
    if set(INCLUDE_SECTORS).issubset(available_sectors):
        print("All specified sectors are available and included ✅")
    else:
        missing = set(INCLUDE_SECTORS) - set(sectors_df['name'])
        print(f"The specified sector: {missing} not available ❌")


def filter_sectors(sectors_df,START_RANK = None, END_RANK = None ):
    '''
    Combine sectors in INCLUDE_SECTORS list, and specified ranks
    '''
    
    include_condition = sectors_df['name'].isin(INCLUDE_SECTORS)
    
    if START_RANK is None and END_RANK is None:
        rank_condition = False
        print(f"We will only perform a comparison for those explicitly specified in the INCLUDE_SECTORS list.")
    else:
        # If START_RANK is not specified, set to 0.
        if START_RANK is None:
            START_RANK = 0
    
        # If END_RANK is not specified, set to the last element.
        if END_RANK is None:
            END_RANK = len(sectors_df)
    
        # Check for invalid values.
        try:
            START_RANK = int(START_RANK)
            END_RANK = int(END_RANK)
        except ValueError:
            raise ValueError("START_RANK and END_RANK must be integer or None")
    
        if START_RANK > len(sectors_df) or END_RANK > len(sectors_df):
            raise ValueError(f"START_RANK ({START_RANK}) or END_RANK ({END_RANK}) cannot be greater than the max index of fetched sectors ({len(sectors_df)})")
        if START_RANK >= END_RANK:
            raise ValueError(f"START_RANK ({START_RANK}) cannot be greater or equal than END_RANK ({END_RANK})")
    
        rank_condition = sectors_df.index.isin(range(START_RANK, END_RANK))
        print(f"We will perform a comparison between sectors ranked {START_RANK} to {END_RANK} by market capitalization and those explicitly specified in the INCLUDE_SECTORS list.")
    
    check_include_sectors(sectors_df,INCLUDE_SECTORS)
    
    filtered_sectors = sectors_df[rank_condition | include_condition]

    return filtered_sectors



def filter_tokens(all_tokens):
    """
    Filter tokens with small market cap
    """
    tokens = []
    for item in all_tokens:
        market_cap = item.get("market_cap")

        # Check if market_cap is a valid number (not None, not missing)
        if isinstance(market_cap, (int, float)) and market_cap >= MIN_MARKET_CAP:
            tokens.append({
                "id": item["id"],
                "symbol": item["symbol"],
                "name": item["name"],
                "market_cap": market_cap
            })

    # Check if all tokens' market cap meet the requirement
    if not tokens:
        print("❗Warning: No tokens meet the market cap requirement under the current sector.")
        return None 

    tokens_df = pd.DataFrame(tokens)
    tokens_df = tokens_df.sort_values(by="market_cap", ascending=False).reset_index(drop=True)
    
    return tokens_df



def process_token_data(raw_token_history_data, token_id , sector_id):
    '''
    Organize token data into a dataframe
    '''   
    # Extract and align data
    dates = [datetime.datetime.fromtimestamp((x[0] / 1000), datetime.UTC).date() for x in raw_token_history_data['prices']]
    prices = [x[1] for x in raw_token_history_data['prices']]
    market_caps = [x[1] for x in raw_token_history_data['market_caps']]
    total_volumes = [x[1] for x in raw_token_history_data['total_volumes']]
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'token_id': token_id,
        'prices': prices,
        'market_caps': market_caps,
        'total_volumes': total_volumes,
        'sector_id': sector_id
    })

    # Remove the last row as it's the real-time data for current day
    df = df.iloc[:-1]
    
    return df


def full_range_token_data(filtered_tokens_df, sector_id):
    '''
    Get all date range price data of all tokens under a sector
    '''
    
    sector_data_df = pd.DataFrame()
    
    for token_id in filtered_tokens_df['id']:
        print(token_id)
        
        raw_token_history_data = get_token_history_data(token_id)
        token_history_data_df = process_token_data(raw_token_history_data, token_id,sector_id)
    
        if token_history_data_df.empty:
            print(token_id , "token processed data history empty")
            continue
    
        # sector_data_df includes all tokens' price, market cap data under one sector for the full date range
        if sector_data_df.empty:
            sector_data_df = token_history_data_df
        else:
            sector_data_df = pd.concat([sector_data_df,token_history_data_df])
    
        # sector_data_df.to_excel(general_path + f"/complete output/one_category_2_df/{category_name}.xlsx", index=False)
    print()
    return sector_data_df



def calculate_sector_weighted_value(df):

    df_daily_summary = df.groupby(['date']).agg({'market_caps': 'sum'}).reset_index()
    df_daily_summary['Weighted Price'] = df.groupby(['date']).apply(lambda x: (x['market_caps'] * x['prices']).sum() / x['market_caps'].sum(), include_groups=False).values
    df_daily_summary['Daily Return'] = df_daily_summary['Weighted Price'].pct_change()
    df_daily_summary.loc[0, 'Weighted Value'] = WEIGHTED_PRICE_BASE
    
    for i in range(1, len(df_daily_summary)):
        df_daily_summary.loc[i, 'Weighted Value'] = df_daily_summary.loc[i - 1, 'Weighted Value'] * (1 + df_daily_summary.loc[i, 'Daily Return'])

    return df_daily_summary



    