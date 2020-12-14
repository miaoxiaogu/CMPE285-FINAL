from flask import Flask, render_template, request,flash, redirect, session, abort
from flask_bootstrap import Bootstrap
from alpha_vantage.timeseries import TimeSeries
import requests
import datetime
import time
import calendar,math
import os

flag = False
message=""

app = Flask(__name__);
Bootstrap(app)

api_keys = ["KCTRYLR11PVQT6JJ", "U5S90TNHCRTW2NQ2", "MFTE7USIP2Q5WO5R", "JR6QIK8EY3VBLE9H", "UT78M5WYW4QJS1RR", "PRU63Z5EY37N9OPZ"]
key_index = 0

@app.route("/")
def home():
    return render_template("Homepage.html", **locals())

def fetch_graph_results(strategy_name, investment_per_strategy, stock_symbol_array):
    stocks_data = {}
    days = set()
    investment = investment_per_strategy / len(stock_symbol_array)

    for stock_symbol in stock_symbol_array:
        # take turns using API key
        global key_index
        print ("key_index:" + str(key_index))
        ts = TimeSeries(key=api_keys[key_index])
        key_index = (key_index + 1) % len(api_keys)
        data, meta_data = ts.get_daily_adjusted(stock_symbol)

        # successfully retrieve data
        if meta_data:
            count = 0
            for day in data:
                days.add(day)
                price = data[day]['5. adjusted close']
                if day in stocks_data.keys():
                    stocks_data[day].append([strategy_name, stock_symbol, price])
                else:
                    stocks_data[day] = []
                    stocks_data[day].append([strategy_name, stock_symbol, price])
                count = count + 1
                if count >= 5:
                    break

    print (sorted(days))

    graph_results = []
    graph_results_detailed = []

    for day in sorted(days):
        # loop each of the historical days
        investment_num = 0
        stocks = stocks_data[day]
        plan = []
        for stock in stocks:
            symbol = stock[1]
            price = float(stock[2])
            share = math.floor(investment / price)
            investment_num += share * price
            plan.append([symbol, round(price, 2), share])
        graph_results.append([day, round(investment_num, 2)])
        graph_results_detailed.append([day, plan])

    return graph_results, graph_results_detailed


@app.route('/stockportfolio', methods=['POST'])
def generateGraphs():
    amount_money = request.form['investment_value']
    strategies = request.form.getlist('strategy')
    investment_per_strategy = int(amount_money) / len(strategies)

    print("Money ready for invest", amount_money)
    print("Input Investment Strategies", strategies)

    ethical_stock = ['DIS', 'DBX', 'ADBE']
    growth_stock = ['TSLA', 'ZM', 'SNOW']
    index_stock = ['XOM', 'AMZN', 'HMC']
    quality_stock = ['JPM', 'AAPL', 'BBY']
    value_stock = ['MSFT', 'FB', 'GOOG']

    try:

        final_graph_results = []
        final_graph_results_detailed = []

        num_of_strategy = len(strategies)

        for strategy in strategies:

            if num_of_strategy == 2:
                time.sleep(38)

            if strategy == "Ethical Investing":
                current_stock = ethical_stock
            elif strategy == 'Growth Investing':
                current_stock = growth_stock
            elif strategy == 'Index Investing':
                current_stock = index_stock
            elif strategy == 'Quality Investing':
                current_stock = quality_stock
            elif strategy == 'Value Investing':
                current_stock = value_stock
            elif strategy == 'Low Risk':
                current_stock = value_stock
            elif strategy == 'High Risk':
                current_stock = growth_stock


            print("YSYSYS         " + strategy)

#             if num_of_strategy ==2:
#                 time.sleep(60)

            print("RESULT for" + strategy+":")
            graph_results, graph_results_detailed = fetch_graph_results(strategy, investment_per_strategy, current_stock)

            final_graph_results.append([strategy, graph_results])

            final_graph_results_detailed.append([strategy, graph_results_detailed])

            print("Graph Result : ", final_graph_results)

            for something in final_graph_results_detailed:
                print(len(final_graph_results_detailed))
                for another_thing in something:
                    print(len(another_thing))
                    for thing in another_thing:
                        if type(thing) is list:
                            
                            #print(thing[1])
                            #print(thing[1][1])
                            price0 = round(thing[1][0][1]*thing[1][0][2],2)
                            thing[1][0].append(price0)
                            price1 = round(thing[1][1][1]*thing[1][1][2],2)
                            thing[1][1].append(price1)
                            price2 = round(thing[1][2][1]*thing[1][2][2],2)
                            thing[1][2].append(price2)
                            print(thing)


            # print("Detailed Graph Result : ", final_graph_results_detailed)

        if len(final_graph_results) == 1 and len(final_graph_results_detailed) == 1:
            return render_template("Portfolio_One Strategy.html", fgr=final_graph_results, pgrd=final_graph_results_detailed)

        elif len(final_graph_results) == 2 and len(final_graph_results_detailed) == 2:
            return render_template("Portfolio_Two Strategies.html", fgr=final_graph_results, pgrd=final_graph_results_detailed)
        else:
            print("Strategy Selection Error")

    except ValueError:
        print('Stock Symbol NOT found')

    except requests.ConnectionError:
        print('Connection Error')

if __name__=='__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=3000)
