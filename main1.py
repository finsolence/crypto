import asyncio

#import nest_asyncio
#nest_asyncio.apply()
import pandas as pd
from binance import BinanceSocketManager
from binance.client import Client
import numpy as np
from tradingview_ta import TA_Handler, Interval, Exchange

client = Client('','')
'''ST = 7
LT = 25

def gethistoricals (symbol, LT):
  df = pd.DataFrame(client.get_historical_klines(symbol, '1d',
                                                 str(LT) + 'days ago UTC',
                                                 '1 day ago UTC'))
  closes = pd.DataFrame(df[4])
  closes.columns = ['Close']
  closes['ST'] = closes.Close.rolling(ST-1).sum()
  closes['LT'] = closes.Close.rolling(LT-1).sum()
  closes.dropna(inplace=True) #удаления строк и столбцов с значениями NULL/NAN
  return closes

historicals = gethistoricals('COCOSUSDT', LT)
#print(historicals)
def liveSMA(hist, live):
  liveST = (hist['ST'].values + live.Price.values) / ST
  liveLT = (hist['LT'].values + live.Price.values) / LT
  return liveST, liveLT

def createframe(msg):
  df = pd.DataFrame([msg])
  df = df.loc[:,['s', 'E', 'p']]
  df.columns = ['Symbol', 'Time', 'Price']
  df.Price = df.Price.astype(float)
  df.Time = pd.to_datetime(df.Time, unit='ms')
  return df
''' #робоча схема торгівлі, но поки не розібрався

'''async def main(coin, qty, SL_limit, open_position = False):
  bm = BinanceSocketManager(client)
  ts = bm.trade_socket(coin)
  async with ts as tscm:
    while True:
      res = await tscm.recv()
      if res:
        frame = createframe(res)
        print(frame)
        livest, livelt = liveSMA(historicals, frame)
        if livest > livelt and not open_position:
          order = client.create_order(symbol=coin, syde='BUY', type='MARKET', quantity=qty)
          print(order)
          print('Open Order')
          buyprice = float(order['fills'][0]['price'])
          open_position = True
        if open_position:
          if frame.Price[0] < buyprice * SL_limit or frame.Price[0] > 1.03 * buyprice:
            order = client.create_order(symbol=coin, syde='SELL', type='MARKET', quantity=qty)
            print(order)
            print('Close Order')
            loop.stop()'''
'''if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main('COCOSUSDT', 5, 0.999))'''



import time
from tradingview_ta import TA_Handler, Interval, Exchange

SYMBOL = 'BTCUSDT'
INTERVAL = Interval.INTERVAL_1_MINUTE
QNTY = 1



def get_data():
        output = TA_Handler(symbol=SYMBOL,
                                screener='Crypto',
                                exchange='Binance',
                                interval = INTERVAL)

        activity = output.get_analysis().summary
        return activity


def place_order(order_type):
    if(order_type == 'BUY'):
        order = client.create_order(symbol=SYMBOL, side=order_type, type= 'MARKET', quantity= QNTY)
        print(order)
        with open('data.txt', 'w') as file:
            file.write(order)
    if(order_type == 'SELL'):
        order = client.create_order(symbol=SYMBOL, side=order_type, type= 'MARKET', quantity= QNTY)
        print(order)
        with open('data.txt', 'w') as file:
            file.write(order)


def main():
    buy = False
    sell = True
    print('SCRIPT IS RUNNING...')
    while True:
        data = get_data()
        print(data)
        #if (data['RECOMMENDATION'] == 'STRONG_BUY' and not buy):
            #print("_____BUY_____")
            #place_order('BUY')
           #buy = not buy
            #sell = not sell

        #if (data['RECOMMENDATION'] == 'STRONG_SELL' and not sell):
           # print("_____SELL_____")
            #place_order('SELL')
           # buy = not buy
            #sell = not sell


        time.sleep(1)


if __name__ == '__main__':
    main() #Trading View indicators
