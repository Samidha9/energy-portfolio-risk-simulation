# Energy Portfolio Pricing & Risk Simulation

A quantitative analytics project that forecasts wholesale electricity prices and evaluates the cost and risk of a hypothetical utility energy portfolio using Monte Carlo simulation, VaR, CVaR, and hedging analysis.

## Business Problem

Utilities must purchase electricity while market prices are uncertain. Part of the demand can be purchased through fixed-price contracts, while the remaining demand is exposed to spot-market prices.

This project evaluates:

- Future electricity price uncertainty
- Portfolio cost under different price scenarios
- VaR and CVaR risk
- Impact of different hedge ratios
- Portfolio performance under stressed market conditions

## Data

Historical market data from the U.S. Energy Information Administration (EIA):

- **PJM Real-Time Peak electricity prices** — 2017–2025
- **Henry Hub natural gas prices** — 2017–2025

The cleaned dataset contains 2,149 matched daily observations.

## Methodology

### 1. Data Analysis & Feature Engineering

Analyzed electricity and natural gas price trends, volatility, seasonality, and price relationships.

Created forecasting features including:

- Electricity price lags
- Natural gas price lags
- 7-day moving average
- 7-day price volatility
- Month and day of week

### 2. Electricity Price Forecasting

Compared multiple approaches:

| Model | 2025 MAE | 2025 RMSE |
|---|---:|---:|
| Naive Baseline | 13.46 | 26.66 |
| Linear Regression | **13.34** | **23.96** |
| XGBoost | 14.23 | 26.78 |

Linear Regression was selected because it showed the most consistent performance across different time periods.

### 3. Monte Carlo Risk Simulation

Historical forecast errors were sampled to generate **10,000 possible electricity price scenarios**.

Each simulated price was then used to calculate the cost of a hypothetical utility portfolio.

Base portfolio:

- Demand: **100,000 MWh**
- Hedged: **70%**
- Spot exposure: **30%**
- Fixed price: **$45/MWh**

### 4. Portfolio Risk

Base simulation results:

| Metric | Result |
|---|---:|
| Expected Cost | ~$4.78M |
| 95% VaR | ~$5.81M |
| 95% CVaR | ~$6.95M |

Higher hedge ratios reduced exposure to extreme spot-market price movements.

Stress tests were also performed by increasing electricity prices and demand to evaluate portfolio behavior under adverse market conditions.

## Dashboard

A Streamlit application allows users to change:

- Expected electricity demand
- Hedge ratio
- Fixed contract price
- Forecast electricity price
- Stress scenario

The dashboard dynamically calculates Expected Cost, VaR, CVaR, hedged energy, and spot exposure.

Run with:

```bash
streamlit run dashboard/app.py
