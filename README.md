# Dividend Freedom Dashboard

Educational Streamlit app for tracking progress toward a dividend-funded retirement income goal.

## What it does

- Tracks shares and ETFs
- Calculates portfolio value
- Calculates annual and monthly dividend/distribution income
- Compares income against a target, default $120,000/year
- Estimates portfolio yield
- Estimates portfolio required to meet the income target
- Includes simple rules-based guidance: Accumulate / Hold / Watch
- Includes dummy data for safe testing

## Run locally

1. Install Python.
2. Open a terminal in this folder.
3. Run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Create a GitHub account.
2. Create a new repository.
3. Upload `app.py`, `requirements.txt`, and `sample_holdings.csv`.
4. Create a free Streamlit Community Cloud account.
5. Deploy from the GitHub repository.
6. Main file path: `app.py`.

## Privacy note

Use dummy data on public Streamlit. For real portfolio values, run locally on your own PC unless you have set up private hosting and access controls.

## Disclaimer

This app is educational only and is not financial advice.
