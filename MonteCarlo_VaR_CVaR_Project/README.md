# Monte Carlo Simulation for Risk Metrics (VaR & CVaR)

## Project Overview
This project simulates future asset returns using historical stock data and Monte Carlo methods.
It also estimates Value at Risk (VaR) and Conditional Value at Risk (CVaR), which are widely used in quantitative finance for risk management.

## Features
- Fetches historical stock data from Yahoo Finance (yfinance).
- Simulates future return paths using Monte Carlo.
- Visualizes simulation paths and return distributions.
- Estimates VaR and CVaR at configurable confidence levels.

## Tech Stack
- Python
- NumPy
- Pandas
- Matplotlib / Seaborn
- yfinance

## How to Run
### Option 1: Google Colab (Recommended)
1. Open the notebook in Google Colab.
2. Install dependencies:
   ```python
   !pip install yfinance numpy pandas matplotlib seaborn
   ```
3. Run all cells.

### Option 2: Local Jupyter Notebook
1. Clone the repo and navigate to the folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch Jupyter Notebook and run the file `MonteCarloSimulation+VaR&CVaR.ipynb`.

## Results
- Monte Carlo paths show possible future scenarios.
- Histogram of returns shows distribution of outcomes.
- VaR gives worst expected loss under normal conditions.
- CVaR gives average loss in extreme downside cases.

## Author
Developed by [Your Name].
