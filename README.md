# Financial Freedom Dashboard V12

Purpose: answer the question:

**How many more years do we need to work?**

This dashboard focuses on retirement planning and forecasting financial independence, not portfolio trading.

## Features

- Financial Freedom Date
- Years Remaining
- Retirement Bridge 55–60
- Investment Portfolio Forecast
- Superannuation Forecast
- Dividend Income Forecast
- Bad Debt Paydown
- Investment Leverage
- Manual Monthly Inputs
- Historical Snapshot Storage
- Scenario Inputs

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Data storage

The dashboard stores historical data in:

```text
data/monthly_snapshots.csv
```

This is intentionally simple for Version 12.
