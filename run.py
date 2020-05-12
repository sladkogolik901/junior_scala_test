from flask import Flask
import pandas as pd
import parse_api
import json

app = Flask(__name__)

module_name = 'parse_read'

#Download and prepare data
parse_api.get_info()

#Testing
@app.route("/")
def hello():
    return "Everything is working. Please, enter your query"

#retun price for selected date
@app.route('/price/<string:date>')
def return_price(date):
    try:
        dt_date = pd.to_datetime(date)
        df_price = parse_api.df[(parse_api.df['start_date'] <= dt_date) & (parse_api.df['end_date'] >= dt_date)]
        selected_price = str(list(df_price['mean_price'])[0])
        return selected_price
    except:
        print('Wrong date.You need to enter correct date - YYYY-mm-dd')

#return mean price in date's interval
@app.route('/mean_price/<string:start_date>/<string:end_date>')
def return_mean_price(start_date, end_date):
    try:
        dt_start = pd.to_datetime(start_date)
        dt_end = pd.to_datetime(end_date)
        df_mean = parse_api.df[(parse_api.df['start_date'] >= dt_start) & (parse_api.df['end_date'] <= dt_end)]
        mean_price = str(df_mean['mean_price'].mean())
        return mean_price
    except:
        print('Wrong date. You need to enter correct dates in format YYYY-mm-dd, start_date/end_date ')

#return min and max prices in date's interval
@app.route('/min_max_price/<string:start_date>/<string:end_date>')
def return_min_max_price(start_date, end_date):
    try:
        dt_start = pd.to_datetime(start_date)
        dt_end = pd.to_datetime(end_date)
        df_mean = parse_api.df[(parse_api.df['start_date'] >= dt_start) & (parse_api.df['end_date'] <= dt_end)]
        min_price = str(df_mean['mean_price'].min())
        max_price = str(df_mean['mean_price'].max())
        dict_price = {'min_price': min_price, 'max_price': max_price}
        data_json = json.dumps(dict_price)
        return data_json
    except:
        print('Wrong date. You need to enter correct dates in format YYYY-mm-dd, start_date/end_date ')

#return statistics
@app.route('/statistics/')
def statistics():
    try:
        shape = parse_api.df.shape
        size = int(parse_api.df.size)
        dict_stat = {'rows': shape[0],
                     'columns': shape[1],
                     'size': size}
        return dict_stat
    except:
        print('Something goes wrong. Please, repeat your query later')

if __name__ == "__main__":
    app.run()