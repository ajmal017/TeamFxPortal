import datetime
from flask import Flask,redirect, url_for, request
import matplotlib.pyplot as plt
import pandas as pd


def plot_results():
    print("duck")
    year = request.form["year"]
    from_month = request.form["from_month"]
    to_month = request.form["to_month"]

    print('anomalies are detecting...')
    print('year: ' + str(year))
    print('from_month: ' + str(from_month))
    print('to_month: ' + str(to_month))
    currency = request.form["currency"]

    start_date = request.form["year"] + "-" + request.form["from_month"] + "-01"
    #end_date = request.form["year"] + "-" + str(int(request.form["to_month"]) + 1) + "-01"
    if (int(request.form["to_month"]) == 12):
        end_date = str(int(request.form["year"]) + 1) + "-" + str(1) + "-01"
    else:
        end_date = request.form["year"] + "-" + str(int(request.form["to_month"]) + 1) + "-01"

    quotes = pd.read_csv("static/data/"+currency+"/DAT_MT_"+currency+"_M1_" + str(year) + ".csv")


    quotes['Time'] = quotes[['Date', 'Time']].apply(lambda x: ' '.join(x), axis=1)
    quotes['Time'] = quotes['Time'].apply(lambda x: pd.to_datetime(x) - datetime.timedelta(hours=2))
    quotes.index = quotes.Time

    print(quotes)
    # select desired range of dates
    mask = (quotes.index > start_date) & (quotes.index <= end_date)
    quotes = quotes.loc[mask]

    print(quotes)

    fig, ax = plt.subplots()
    ax.plot(quotes['Close'])
    ax.set_title('Black Regions')
    anormalies = pd.read_csv("static/anomalies/all_anomalies.csv")

    anormalies['Time'] = anormalies['DateHour'].apply(lambda x: pd.to_datetime(x))
    anormalies.index = anormalies.Time
    mask = (anormalies.index > start_date) & (anormalies.index <= end_date)
    anormalies = anormalies.loc[mask]
    #xdate = [datetime.datetime.fromtimestamp(i) for i in quotes['Time']]

    for index, row in anormalies.iterrows():
        a_index = row["Time"]
        b_index = row["Time"]+datetime.timedelta(hours=1)
        ax.axvspan(a_index, b_index, color='red', alpha=0.5)

    plt.show()


#https://stackoverflow.com/questions/42373104/candlestick-ochl-graph