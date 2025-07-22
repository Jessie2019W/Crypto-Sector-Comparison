# Crypto-Sector-Comparison
This project analyzes and compares the performance of different crypto categories over a chosen time period. It retrieves necessary category and token data via the CoinGecko API, calculates each category’s weighted price (normalized to 100 on the start date), and visualizes their trends through interactive comparative charts.
## Demo Result Chart
Please see [here](https://jessie2019w.github.io/Crypto-Sector-Comparison/).
## CoinGecko API (Free / Demo Plan) Limitations:
- Historical data is limited to the past 365 days only.
- You can only set the time range by "days ago", not a custom start–end range.
- Each category returns only the first page of tokens (max 100); here we limit to 20 for speed.
- Sector-level full token lists are not available.
- The free plan works but may be slower.
- 👉 For broader or more precise data, consider a [CoinGecko paid API plan](https://www.coingecko.com/en/api/pricing).
