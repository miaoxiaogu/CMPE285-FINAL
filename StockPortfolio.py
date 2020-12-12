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

@app.route("/")
def home():
    return render_template("Homepage.html", **locals())

def fetch_graph_results(strategy_name, investment_per_strategy, stock_symbol_array):
    stock_details = []
    five_days_history = []
    investment_per_company = investment_per_strategy / 3

    for stock_symbol in stock_symbol_array:

        ts = TimeSeries(key='U5S90TNHCRTW2NQ2')
        data, meta_data = ts.get_daily_adjusted(stock_symbol)

        if meta_data:

            count = 0
            for each_entry in data:
                if count < 5:
                    stock_details.append(
                        [strategy_name, stock_symbol, each_entry, data[each_entry]['5. adjusted close']])
                    five_days_history.append(each_entry)
                    count = count + 1
                else:
                    break

    first_day = []

    first_day_history = []
    second_day_history = []
    third_day_history = []
    fourth_day_history = []
    fifth_day_history = []

    first_day_investment = 0
    second_day_investment = 0
    third_day_investment = 0
    forth_day_investment = 0
    fifth_day_investment = 0

    graph_results = []
    graph_results_detailed = []

    for entry in stock_details:
        if entry[2] == sorted(set(five_days_history))[0]:
            first_day.append([entry[1], entry[3]])
            no_of_stocks_per_company = math.floor(investment_per_company / float(entry[3]))
            first_day_history.append([entry[1], round(float(entry[3]), 2), no_of_stocks_per_company])
            first_day_investment += no_of_stocks_per_company * float(entry[3])

    graph_results.append([sorted(set(five_days_history))[0], round(first_day_investment, 2)])

    for entry in stock_details:

        if entry[2] == sorted(set(five_days_history))[1]:
            for company in first_day_history:
                if company[0] == entry[1]:
                    second_day_history.append([entry[1], round(float(entry[3]), 2), company[2]])
                    second_day_investment += (float(entry[3]) * company[2])

        elif entry[2] == sorted(set(five_days_history))[2]:
            for company in first_day_history:
                if company[0] == entry[1]:
                    third_day_history.append([entry[1], round(float(entry[3]), 2), company[2]])
                    third_day_investment += (float(entry[3]) * company[2])

        elif entry[2] == sorted(set(five_days_history))[3]:
            for company in first_day_history:
                if company[0] == entry[1]:
                    fourth_day_history.append([entry[1], round(float(entry[3]), 2), company[2]])
                    forth_day_investment += (float(entry[3]) * company[2])

        elif entry[2] == sorted(set(five_days_history))[4]:
            for company in first_day_history:
                if company[0] == entry[1]:
                    fifth_day_history.append([entry[1], round(float(entry[3]), 2), company[2]])
                    fifth_day_investment += (float(entry[3]) * company[2])

    graph_results.append([sorted(set(five_days_history))[1], round(second_day_investment, 2)])
    graph_results.append([sorted(set(five_days_history))[2], round(third_day_investment, 2)])
    graph_results.append([sorted(set(five_days_history))[3], round(forth_day_investment, 2)])
    graph_results.append([sorted(set(five_days_history))[4], round(fifth_day_investment, 2)])

    graph_results_detailed.append([sorted(set(five_days_history))[0], first_day_history])
    graph_results_detailed.append([sorted(set(five_days_history))[1], second_day_history])
    graph_results_detailed.append([sorted(set(five_days_history))[2], third_day_history])
    graph_results_detailed.append([sorted(set(five_days_history))[3], fourth_day_history])
    graph_results_detailed.append([sorted(set(five_days_history))[4], fifth_day_history])

    return graph_results, graph_results_detailed


@app.route('/stockportfolio', methods=['POST'])
def generateGraphs():
    amount_money = request.form['investment_value']
    strategies = request.form.getlist('strategy')
    investment_per_strategy = int(amount_money) / len(strategies)

    sleep_time = 37

    print("Money ready for invest", amount_money)
    print("Input Investment Strategies", strategies)

    ethical_stock = ['DIS', 'DBX', 'ADBE']
    growth_stock = ['PFE', 'NIO', 'T']
    index_stock = ['XOM', 'AMZN', 'HMC']
    quality_stock = ['JPM', 'AAPL', 'BBY']
    value_stock = ['BABA', 'TWTR', 'GOOG']

    try:

        final_graph_results = []
        final_graph_results_detailed = []

        num_of_strategy = len(strategies)

        for strategy in strategies:

            if num_of_strategy == 2:
                time.sleep(sleep_time)

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


            print("YSYSYS         " + strategy)

            if num_of_strategy ==2:
                time.sleep(sleep_time)

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