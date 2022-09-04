import pandas as pd
import requests
import datetime
from bs4 import BeautifulSoup as bs


binance_futures_url = 'https://fapi.binance.com'


def main():
    res = requests.get('https://s3-ap-northeast-1.amazonaws.com/data.binance.vision?delimiter=/&prefix=data/futures/um/daily/trades/BTCUSDT/&marker=data/futures/um/daily/trades/BTCUSDT/BTCUSDT-trades-2021-01-19.zip.CHECKSUM')
    with open('res.html', 'w') as f:
        f.write(res.text)

    soup = bs(res.text, 'html.parser')
    keys = soup.find_all('key')
    for k in keys:
        print(k.text)



if __name__ == '__main__':
    main()