# Crypto-Sector-Comparison
This project analyzes and compares the performance of different crypto categories over a chosen time period. It retrieves necessary category and token data via the CoinGecko API, calculates each category’s weighted price (normalized to 100 on the start date), and visualizes their trends through interactive comparative chart.

## Demo Result Chart
Please see [here](https://jessie2019w.github.io/Crypto-Sector-Comparison/).

## ⚙️ Configuration
Before running the **Main.ipynb**, adjust the configuration parameters as needed or use the current config file for demo:

**1. IS_PRO_USER and API_KEY**
- Specify your CoinGecko API plan and API key.
- The free plan does not require an API key.

**2. START_DATE and END_DATE**
- Set the start and end dates for the observation period.
- Note: Free API plan can only set the end date as "1 days ago" (yesterday).

**3. START_RANK and END_RANK**
- Select categories based on market cap ranking from CoinGecko’s category list.
- For example, START_RANK = 1 and END_RANK = 5 will pick the top 5 categories by market cap.

**4. INCLUDE_SECTORS and EXCLUDE_SECTORS**
- INCLUDE_SECTORS: A list of categories you want to include. You can find category names on [CoinGecko Categories](https://www.coingecko.com/en/categories ).
- EXCLUDE_SECTORS: A list of categories you want to exclude (e.g., stablecoins, as their prices rarely change).
- If you set both rank ranges (START_RANK, END_RANK) and INCLUDE_SECTORS, the script will combine the top-ranked categories and the explicitly included categories for comparison.

**5. MIN_MARKET_CAP**
- Set a minimum market cap for categories or tokens. Categories or tokens below this value will be ignored.

**6. WEIGHTED_PRICE_BASE**
- The initial value for calculating weighted prices.
- For example, if WEIGHTED_PRICE_BASE = 100, then on the START_DATE, all categories are normalized to 100.

**7. FREE_USER_PER_PAGE**
- For free API plan users, this limits the number of tokens retrieved per category.
- For example, if FREE_USER_PER_PAGE = 20, only the top 20 tokens (by market cap) in each category will be used.

## 🚀 How to Run
- Edit the `config.py` with desired settings.
- Run the Main.ipynb in the **Jupyter Notebook**

## 📊 Output
- The script will generate an interactive comparative chart in the Jupyter Notebook and export an .html file containing the same chart.
- Please find the demo result chart [here](https://jessie2019w.github.io/Crypto-Sector-Comparison/).

## CoinGecko API (Free / Demo Plan) Limitations
- Historical data is limited to the past 365 days only.
- Free API plan can only set the time range by "days ago", not a custom start–end range.
- Each category returns only the first page of tokens (max 100); here we limit to 20 for speed.
- Sector-level full token lists are not available.
- The free plan works but may be slower.
- 👉 For broader or more precise data, consider a [CoinGecko paid API plan](https://www.coingecko.com/en/api/pricing).
