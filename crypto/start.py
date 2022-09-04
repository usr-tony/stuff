import sys
sys.path.append('./functions')
from threading import Thread
from binance import AsyncClient, BinanceSocketManager
from os import environ
import time
import asyncio
from statistics import mean
from bisect import bisect_left
from get_info import get_exchange_info
from orders import create_order
from math import floor


symbols = [
    'ETHUSDT',
    'BTCUSDT',
    'LTCUSDT',
    'ADAUSDT',
    'XRPUSDT',
    'DOGEUSDT',
    'BNBUSDT',
]

async def main():
    apikey = environ.get('apikey')
    apisecret = environ.get('secretkey')
    # insert api keys above
    create_global_vars()
    client = await AsyncClient.create(api_key=apikey, api_secret=apisecret)
    ex_info = await get_exchange_info(client)   # dictionary of symbol : {minQty: <minimum trade quantity>, tickSize: <contract tick size>}
    await start_soc(client, ex_info)


def create_global_vars():
    globals()['position'] = {'status': 0, 'symbol': '', 'qty': 0} # keeps track of current position; status 1 = long, -1 = short, 0 = no position;
    globals()['tables'] = dict()  # table containing parsed websocket trade data
    globals()['sym_index'] = dict() # moving averages of individual tickers
    for s in symbols:
        tables[s] = {
            'T': [],
            'b': [],
            'a': []
        }
        sym_index[s] = []


async def start_soc(client, ex_info):
    global tables
    bsm = BinanceSocketManager(client)
    ts = bsm.futures_multiplex_socket([s.lower() + '@bookTicker' for s in symbols]) # starts a socket with all symbols in symbols file
    async with ts: # starts receiving messages and appends them to table
        while True:
            d = await ts.recv()
            sym = d['stream'].split('@')[0].upper()     # retrieves symbol from websocket message
            print(d)
            table = tables[sym]    
            table['T'].append(int(d['data']['T']))     # appends the following to tables[symbol]: timestamp
            table['b'].append(float(d['data']['b']))     # closest bid
            table['a'].append(float(d['data']['a']))     # closest ask
            await signal(sym, client, ex_info)


async def signal(sym, client, ex_info):
    global position
    if sym_index[sym] == []:
        return
    
    rel_prices = []
    agg_index = 0
    for s in symbols:
        index_mean = mean(sym_index[s])
        rel_bid = tables[s]['b'][-1] / index_mean
        rel_ask = tables[s]['a'][-1] / index_mean
        rel_mid = (rel_bid + rel_ask) / 2
        rel_prices.append([s, rel_mid, rel_bid, rel_ask])
        # for relative prices:
        # 0 : symbol
        # 1 : mid price
        # 2 : bid
        # 3 : ask
        agg_index += rel_mid

    agg_index /= len(symbols)   # aggregate index is the average calculated index of all symbols considered
    if abs(agg_index - 1) > 0.0004 and position['status'] == 0:
        if_reverse = True if agg_index > 0 else False
        rel_prices.sort(key=lambda x:x[1], reverse=if_reverse)

        if abs(rel_prices[0][1] - 1) > 0.0008 and abs(rel_prices[1][1] - 1) > 0.0005:
            position['symbol'] = rel_prices[-1][0]    # asset of interest is the one that is slowest to move
            
            if position['symbol'] != 'BTCUSDT':
                side = 'BUY' if agg_index > 1 else 'SELL'
                price = tables[position['symbol']]['a'][-1] if side == 'BUY' else tables[position['symbol']]['b'][-1]
                min_qty = float(ex_info[position['symbol']]['minQty'])   
                # dictionary of symbol : {minQty: <minimum trade quantity>, tickSize: <contract tick size>}
                qty = floor(5.0 // (min_qty * price) + 1) * min_qty
                await create_order(client, position['symbol'], side, price, 'MARKET', qty)
                position['qty'] = qty
                if agg_index > 1: 
                    position['status'] = 1
                elif agg_index < 1: 
                    position['status'] = -1
                
                print(price, position, 'minqty:', min_qty, 'precision:', ex_info[position['symbol']]['tickSize'])


    elif position['status'] != 0 and abs(agg_index - 1) < 0.0002:
        side = 'BUY' if position['status'] == -1 else 'SELL'
        qty = position['qty']
        await create_order(client, position['symbol'], side, qty=qty)
        price = tables[position['symbol']]['a'][-1] if side == 'BUY' else tables[position['symbol']]['b'][-1]
        position['status'] = 0
        position['symbol'] = ''
        position['qty'] = 0
            

def indices():
    global tables
    time.sleep(22) # waits for websockets to initialize and collect data
    while True:
        for s in symbols:
            update_index(s)
    
        time.sleep(0.67)


def update_index(sym): # generates index and relative index values from table containing raw trade data
    global tables
    global sym_index
    time_stamp, bid, ask = [tables[sym][c] for c in tables[sym]] # extracts columns from table as variables
    index_values = []
    for dt in [20000, 10000, 5000]: #  generate index values for to determine asset price (x)ms ago
        t1 = time_stamp[-1] - dt
        ii = bisect_left(time_stamp, t1)
        index_values.append(ii)

    mid_prices = []
    rel_mid_prices = []
    relative_price = ((bid[index_values[0]] + ask[index_values[0]]) / 2)
    for ii in index_values:
        mid = (bid[ii] + ask[ii]) / 2
        mid_prices.append(mid)
        rel_mid_prices.append(mid / relative_price)
        
    sym_index[sym] = mid_prices
    

if __name__ == '__main__':
    t = Thread(target=indices)
    t.start()
    asyncio.run(main())
    
    
