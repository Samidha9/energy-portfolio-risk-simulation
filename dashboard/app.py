import streamlit as st
import pandas as pd
import numpy as np

st.title("Energy Portfolio Pricing & Risk Simulator")

st.write(
    "Estimate portfolio cost, market risk, and the impact of hedging."
)

# User Inputs
total_mwh = st.number_input(
    "Expected demand (MWh)",
    value=100000
)

hedge_ratio = st.slider(
    "Hedge ratio",
    0.0,
    1.0,
    0.70
)

fixed_price = st.number_input(
    "Fixed hedge price ($/MWh)",
    value=45.0
)

base_price = st.number_input(
    "Forecast power price ($/MWh)",
    value=50.67
)

# Load historical forecast errors
results = pd.read_csv(
    "data/processed/forecast_results.csv"
)

errors = results["error"].values

# Monte Carlo Simulation
np.random.seed(42)

simulated_errors = np.random.choice(
    errors,
    size=10000,
    replace=True
)

simulated_prices = base_price + simulated_errors

# Portfolio
fixed_mwh = total_mwh * hedge_ratio
spot_mwh = total_mwh - fixed_mwh

portfolio_cost = (
    fixed_mwh * fixed_price
    + spot_mwh * simulated_prices
)

# Risk Metrics
expected_cost = portfolio_cost.mean()
var95 = np.percentile(portfolio_cost, 95)
cvar95 = portfolio_cost[portfolio_cost >= var95].mean()

# Results
st.subheader("Portfolio Risk Results")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Expected Cost",
    f"${expected_cost:,.0f}"
)

col2.metric(
    "95% VaR",
    f"${var95:,.0f}"
)

col3.metric(
    "95% CVaR",
    f"${cvar95:,.0f}"
)

st.subheader("Portfolio Exposure")

col1, col2 = st.columns(2)

col1.metric(
    "Hedged Energy",
    f"{fixed_mwh:,.0f} MWh"
)

col2.metric(
    "Spot Exposure",
    f"{spot_mwh:,.0f} MWh"
)

st.subheader("Stress Test")

stress_choice = st.selectbox(
    "Choose a market scenario",
    [
        "Base",
        "Power Price +20%",
        "Power Price +50%"
    ]
)

if stress_choice == "Base":
    stressed_price = base_price

elif stress_choice == "Power Price +20%":
    stressed_price = base_price * 1.20

else:
    stressed_price = base_price * 1.50


stressed_prices = stressed_price + simulated_errors

stressed_portfolio_cost = (
    fixed_mwh * fixed_price
    + spot_mwh * stressed_prices
)

stress_expected = stressed_portfolio_cost.mean()
stress_var95 = np.percentile(stressed_portfolio_cost, 95)
stress_cvar95 = stressed_portfolio_cost[
    stressed_portfolio_cost >= stress_var95
].mean()


col1, col2, col3 = st.columns(3)

col1.metric(
    "Stress Expected Cost",
    f"${stress_expected:,.0f}"
)

col2.metric(
    "Stress 95% VaR",
    f"${stress_var95:,.0f}"
)

col3.metric(
    "Stress 95% CVaR",
    f"${stress_cvar95:,.0f}"
)

st.subheader("How to Interpret the Results")

st.write("""
- **Expected Cost:** Average portfolio cost across all simulated scenarios.
- **95% VaR:** Cost threshold that about 95% of simulated outcomes stay below.
- **95% CVaR:** Average portfolio cost in the worst 5% of simulated outcomes.
- **Hedge Ratio:** Percentage of electricity purchased at the fixed contract price.
- **Spot Exposure:** Electricity that still needs to be purchased at the uncertain market price.
""")