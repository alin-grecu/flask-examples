from flask import Flask, Markup, render_template
import pandas as pd
import datetime as dt
import re

app = Flask(__name__)

class GraphCorona:

    def __init__(self, timeframe, country):
        self.timeframe = timeframe
        self.country = country
        self.data = []
        self.dates = []
        self.df = pd.DataFrame(columns=['Country', 'Confirmed'])

    def generate_dates(self):
        for i in range(1, self.timeframe):
            date = dt.datetime.today() - dt.timedelta(days=i)
            self.dates.append(date.strftime("%m-%d-%Y"))
        return self.dates

    def fetch_csv(self, dates):
        self.dates = dates
        repo = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19'
        branch = 'master'
        folder = 'csse_covid_19_data/csse_covid_19_daily_reports/'
        url = repo + '/' + branch + '/' + folder
        for date in self.dates:
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
            self.df = self.df.append(data, ignore_index=True)
        return self.df

@app.route('/')
def bar_chart():
    bar_dates = dates
    bar_df = data
    return render_template('bar_chart.html', title="Confirmed cases in Romania", max=1000, labels=bar_dates, values=bar_df['Confirmed'].tolist())

interval = 10 #days
country = 'Romania'

corona = GraphCorona(interval, country)

dates = corona.generate_dates()
data = corona.fetch_csv(dates)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)