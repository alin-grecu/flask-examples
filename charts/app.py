from flask import Flask, Markup, render_template
import pandas as pd
import datetime as dt
import re

class GraphCorona:

    def __init__(self, timeframe, country):
        self.timeframe = timeframe
        self.country = country
        self.data = []

    def run(self):
        self.generate_dates()

    def generate_dates(self):
        dates = []
        for i in range(1, self.timeframe):
            date = dt.datetime.today() - dt.timedelta(days=i)
            dates.append(date.strftime("%m-%d-%Y"))
        self.fetch_csv(dates)

    def fetch_csv(self, dates):
        df = pd.DataFrame(columns=['Country', 'Confirmed'])
        repo = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19'
        branch = 'master'
        folder = 'csse_covid_19_data/csse_covid_19_daily_reports/'
        url = repo + '/' + branch + '/' + folder
        for date in dates:
            data_url = url + date + '.csv'
            data = pd.read_csv(data_url, sep=',')
            headers = pd.read_csv(data_url, nrows=0).columns.tolist()
            try:
                data = pd.read_csv(data_url, usecols=['Country_Region', 'Confirmed'], sep=',')
                data = data.rename(columns={"Country_Region": "Country"})
            except ValueError:
                try:
                    data = pd.read_csv(data_url, usecols=['Country/Region', 'Confirmed'], sep=',')
                    data = data.rename(columns={"Country/Region": "Country"})
                except ValueError:
                    print(ValueError)
            data = data[data['Country'].str.contains(self.country, flags = re.IGNORECASE)]
            df = df.append(data, ignore_index=True)
        self.print_csv(df)

    def print_csv(self, data):
        print(data)

@app.route('/bar')
def bar():
    title="Bar chart by me"

corona = GraphCorona(10, 'Romania')
corona.run()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)