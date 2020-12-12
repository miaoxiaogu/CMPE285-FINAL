# CMPE 285_FINAL PROJECT-Stock Portfolio Suggestion Engine

Input dollar amount to invest in USD (Minimum is $5000 USD)
Pick one or two investment strategies:
Ethical Investing
Growth Investing
Index Investing
Quality Investing
Value Investing
The engine needs to assign stocks or ETFs for a selected investment strategy. 

The suggestion engine will output:

Which stocks are selected based on inputed strategies.
How the money are divided to buy the suggested stock.
The current values (up to the sec via Internet) of the overall portfolio (including all the stocks / ETFs)
A weekly trend of the portfolio value. In order words, keep 5 days history of the overall portfolio value.

Developed in python using Alpha Vantage API for real-time stock data.

## Steps to run the application:

1，Open cmd

2，Navigate to the folder of project

3，Input in cmd：Pip install -r requirements.txt

4，Input in cmd：FLASK_APP=StockPortfolio.py flask run

5，Open web and use Localhost：5000（or other port）to use the engine.
