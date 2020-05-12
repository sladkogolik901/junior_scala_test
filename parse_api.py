import requests
import pandas as pd
from bs4 import BeautifulSoup
import sys

# Constants for translate date
RU_MONTH_VALUES = {
    'янв': 1,
    'фев': 2,
    'мар': 3,
    'апр': 4,
    'май': 5,
    'июн': 6,
    'июл': 7,
    'авг': 8,
    'сен': 9,
    'окт': 10,
    'ноя': 11,
    'дек': 12,
}

url = "https://data.gov.ru/opendata/7710349494-urals"

# Global variable for data storage
df = pd.DataFrame()

# Return html from url
def get_code(url):
    res = requests.get(url)
    return res.text

# Parse html, get data's link, download file
def get_link(html):
    soup = BeautifulSoup(html, 'lxml')
    # Изначальный вариант, до того, как сайт data.gov.ru стал выдавать ошибку 502
    #    tds = soup.find('td', class_="views-field views-field-field-upload-revision-id-1").find('div')
    tds = soup.find('td', class_="views-field views-field-field-upload-revision-id-1")
    if tds:
        tds = tds.find('div')
        for td in tds:
            link = td.find('a').get('href')
            condition = link[0:8]
            if condition == 'https://':
                file = requests.get(link)
                with open('data_file.csv', 'bw') as data_f:
                    for chunk in file.iter_content(8192):
                        data_f.write(chunk)
                print('Done')
        date_path = 'data_file.csv'
        return date_path
    else:
        print("Sorry, url is incorrect or site does't work")
        sys.exit()
# Function for translate str to date
def int_value_from_ru_month(date_str):
    for k,v in RU_MONTH_VALUES.items():
        date_str = date_str.replace(k, str(v))
    return date_str

# Prepare data for analyze
def data_to_pandas(df):
    new_names = ['start_date', 'end_date', 'mean_price']
    df.set_axis(new_names, axis='columns', inplace=True)
    df['start_date'] = df['start_date'].apply(int_value_from_ru_month)
    df['end_date'] = df['end_date'].apply(int_value_from_ru_month)
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    df['mean_price'] = df['mean_price'].apply(lambda x: x.replace(',', '.'))
    df['mean_price'] = df['mean_price'].astype('float64')

# Main function
def get_info():
    file = get_link(get_code(url))  # Если сайт работает
    global df
#    file = 'data_file.csv'  # Скачанный вариант данных. Если сайт не работает,
    #    закомментировать строчку с переменной file выше, эту раскомментировать для проверки API
    df = pd.read_csv(file, encoding='cp1251')
    data_to_pandas(df)
