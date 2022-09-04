from binance import AsyncClient
from os import environ
from time import *
from asyncio import *


async def main():
    client = await AsyncClient.create(api_key=environ.get('apikey'), api_secret=environ.get('secretkey'))
    res = await client.get_account_snapshot(type="SPOT")
    await client.close_connection()
    return res


async def get_exchange_info(client):
    ex_info = {}
    r = await client.futures_exchange_info()
    for row in r['symbols']:
        k = row['filters']
        d = ex_info[row['symbol']] = {}
        d['minQty'] = k[1]['minQty']
        d['tickSize'] = k[0]['tickSize']
        d['qtyprecision'] = row['quantityPrecision']
    
    return ex_info
         
if __name__ == '__main__':
    data = run(main())