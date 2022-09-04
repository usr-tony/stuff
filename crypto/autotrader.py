import binance
from asyncio import run, create_task
from os import environ


symbols = ['btcusdt', 'adausdt', 'ethusdt']
positions = {}
db = {}


async def main():
    client = await binance.AsyncClient.create(api_key=environ.get('apikey'), api_secret=environ.get('secretkey'))
    await start(client)
    print('connection closed')
    client.close_connection()


async def start(client):
    socket_names = [symbol + '@bookTicker' for symbol in symbols]
    manager = binance.BinanceSocketManager(client)
    async with manager.futures_multiplex_socket(socket_names) as socket:
        while True:
            analyze(await socket.recv())


def analyze(data):
    print(data)


if __name__ == '__main__':
    run(main())
