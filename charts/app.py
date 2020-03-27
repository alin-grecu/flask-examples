from flask import Flask, Markup, render_template
import pandas as pd
import datetime as dt
import re

source = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

app = Flask(__name__)

class GraphCorona:

    def __init__(self, timeframe, country, dates=[]):
        self.timeframe = timeframe
        self.country = country
        self.dates = dates
        self.df = pd.DataFrame(columns=['Country', 'Confirmed'])

    def get_dates(self):
        dates = []
        for i in range(1, self.timeframe):
            date = dt.datetime.today() - dt.timedelta(days=i)
            self.dates.append(date.strftime("%m-%d-%Y"))
        return self.dates

    def get_paths(self):
        sources = []
        for date in self.dates:
            path = source + date + '.csv'
            sources.append(path)
        return sources

    def read_csv(self, path):
        try:
            df = pd.read_csv(path, usecols=['Country_Region', 'Confirmed'], sep=',')
            df = df.rename(columns={"Country_Region": "Country"})
        except ValueError:
            try:
                df = pd.read_csv(path, usecols=['Country/Region', 'Confirmed'], sep=',')
                df = df.rename(columns={"Country/Region": "Country"})
            except ValueError:
                print(ValueError)
        df = df[df['Country'].str.contains(self.country, flags = re.IGNORECASE)]
        return df

    def get_data(self):
        df_list = []
        sources = self.get_paths()
        for source in sources:
            df_list.append(self.read_csv(source))
        self.df = pd.concat(df_list, ignore_index=True)
        return self.df

@app.route('/')
def bar_chart():
    maximum = 0
    bar_dates = dates
    bar_df = data['Confirmed'].tolist()
    maximum += max(bar_df) + max(bar_df) / 10
    return render_template('bar_chart.html', title="Confirmed cases in Romania", max=maximum, labels=bar_dates, values=bar_df)

interval = 10 #days
country = 'Romania'

corona = GraphCorona(interval, country)

dates = corona.get_dates()
data = corona.get_data()
print(data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)