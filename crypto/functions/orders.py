from binance import AsyncClient
from os import environ
import asyncio


async def main():
    client = await AsyncClient.create(api_key=environ.get('apikey'), api_secret=environ.get('secretkey'))
    await create_order(client, 'ADAUSDT', 'SELL', 3500, type='LIMIT')
            

async def create_order(client, sym, side, price=None, type='MARKET', qty=0.002):
    task = asyncio.create_task(order(client, sym, side, price, type, qty))


async def order(client, sym, side, price, type, qty):
    trade_params = {
        'symbol': sym,
        'side': side,
        'type': type,
        'quantity': qty,
        'price': price,
        'reduce_only': 'False'
    }
    if trade_params['type'] == 'LIMIT': trade_params['timeInForce'] = 'GTC'
    if trade_params['type'] == 'MARKET': del trade_params['price']

    res = await client.futures_create_order(**trade_params)
    return


if __name__ == '__main__':
    asyncio.run(main())
