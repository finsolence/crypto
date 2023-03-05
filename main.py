
'''class Crypto:
    name = None
    currency = None
    currencytobtc = None
    btcusdt = None
    profit = None

    def __int__(self, name, currency, currencytobtc, btcusdt, profit):
        self.set_data(name, currency, currencytobtc, btcusdt, profit)
        self.get_data()

    def set_data(self, name, currency, currencytobtc, btcusdt, profit):
        self.name = name
        self.currency = currency
        self.currencytobtc = currencytobtc
        self.btcusdt = btcusdt
        self.usdt = usdt
        self.profit = profit

    def get_data(self):
        input(self.name)
        print(self.name, self.currency, self.currencytobtc, self.btcusdt, self.profit)


crypto = Crypto()'''
'''from binance import Client

client = Client('')

TOTAL_PROFIT = 0.0

while True:
    crypto = client.get_order_book(symbol='SOLBUSD')
    crypto2 = client.get_order_book(symbol='SOLBTC')
    crypto3 = client.get_order_book(symbol='BTCUSDT')
    #print(float(crypto['bids'][0][0]))
    #print(float(crypto2['bids'][0][0]))
    #print(float(crypto3['bids'][0][0]))


    currency = float(crypto['bids'][0][0])
    currencytobtc = float(crypto2['bids'][0][0])
    btcusdt = float(crypto3['bids'][0][0])
    deposit = 100


    res1 = deposit / currency
    res2 = res1 * currencytobtc
    res3 = res2 * btcusdt
    res4 = res3 - deposit

    if res3 >= deposit:
        TOTAL_PROFIT += res4

        print(TOTAL_PROFIT)'''

from binance import Client
from binance.enums import *
from datetime import datetime, date
import time
from binance.exceptions import BinanceAPIException
from math import *

CLIENT = Client('eDxlJ4jmacsDO4Gj4Az9GqE8qLAKMnZsVFnCvj7xKK1eGSYOVTzjtSiOfpKCCmOg', 'qsQMYO4nn3LM7p3guUjTMxIWnxdAZqHE0v7VmMKu52FkW4UDdRPHFRIeTLUcoeeX')


class Trader:

    def __init__(self, crypta, money, moneyCountToTrade):
        self.__crypta = crypta
        self.__money = money
        self.__isCryptaBought = False

        self.__balanceCrypta = CLIENT.get_asset_balance(asset = self.__crypta.getName())
        self.__balanceMoney = CLIENT.get_asset_balance(asset = self.__money.getName())


        self.__moneyCountToTrade =  moneyCountToTrade

        self.__tempPrice = CLIENT.get_order_book(symbol = self.getFullName())
        self.__prevPrice = self.__tempPrice
        self.__cryptoInfo = CLIENT.get_symbol_info(self.getFullName())
        self.__temporaryPrice = CLIENT.get_all_tickers()[1797]

        self.__buyCryptCost = 0

    def getMinReqToTrade(self):
        return float(self.__cryptoInfo['filters'][0]['minPrice']) * float(self.__cryptoInfo['filters'][1]['minQty'])


    def getCost(self):
        counter = 0
        allTickers = CLIENT.get_all_tickers()
        for ticker in allTickers:
            if self.getFullName() == str(ticker['symbol']):
                return float(allTickers[counter]["price"])
        counter += 1

    def check(self):

            if  not self.__isCryptaBought:
                if self.getCountOfMoney() > self.getMinReqToTrade() and self.getCost() < self.getAvgPrice():
                    self.buyCrypta()
                    self.__isCryptaBought = True
            else:
                if self.__prevPrice < self.__tempPrice and self.getCost() > self.__buyCryptCost + self.__buyCryptCost * 0.01:
                    self.sellCrypta()
                    self.__isCryptaBought = False

    def updatePrice(self):
        self.__previousPrice = self.__tempPrice
        self.__temporaryPrice = CLIENT.get_order_book(symbol=self.getFullName())
        
    def buyCrypta(self):
        self.__buyCryptCost = self.getCost()
        CLIENT.create_order(symbol = self.__crypta.getName() + self.__money.getName(),
                                side = SIDE_BUY,
                                type = ORDER_TYPE_MARKET,
                                quantity = floor(self.getCountOfMoney() / self.__buyCryptCost))

    def sellCrypta(self):
        CLIENT.create_order(symbol= self.__crypta.getName() + self.__money.getName(),
                                     side=SIDE_SELL,
                                     type=ORDER_TYPE_MARKET,
                                     timeInForce=TIME_IN_FORCE_GTC,
                                     quantity = self.getCountOfCrypta())
                                     

    def getCountOfCrypta(self):
        return float(CLIENT.get_asset_balance(asset=self.__crypta.getName()))

    def getCountOfMoney(self):
        return float(CLIENT.get_asset_balance(asset=self.__money.getName())['free'])
    
    def getFullName(self):
        return self.__crypta.getName() + self.__money.getName()

    def getAvgPrice(self):
        return float(CLIENT.get_avg_price(symbol= self.getFullName())['price'])

    def Tick(self):
        self.updatePrice()
        self.check()


class Currency:

    def __init__(self, name):
        self.__name = name

    def getName(self):
        return self.__name
    
def main():
    COCOSCurrency = Currency("COCOS")
    BUSDCurrency = Currency("BUSD")
    COCOSBUSDTrader = Trader(COCOSCurrency, BUSDCurrency, 20)
    timing = time.time()

    while True:
        if time.time() - timing > 3.0:
            timing = time.time()
            COCOSBUSDTrader.Tick()

main()

'''
def main(*args, **argv):
    

    timing = time.time()
    
    timer = 10
    while True:
        try:
            if time.time() - timing > 3.0:
                timing = time.time()
    
    
                file = open('data.txt', 'a', encoding='utf-8')
    
                current_datetime = date.today()
                current_time = datetime.now().time()

            dict = ('Валютна пара:', info['symbol'],
                    'Статус: ', info['status'],
                    'Дата: ', current_datetime,
                    'Час: ', current_time,
                    'Криптобаланс:', balanceCOCOS['free'],
                    'Валютний баланс:', balanceBUSD['free'])

            file.write(str(dict) + '\n')

            file.close()



            if balBUSD > quaCOCOS_ToBuy * int(priceCOCOS_ToBuy):
                order = client.create_order(symbol='COCOSBUSD',
                    side = SIDE_BUY,                                #КУПІВЛЯ
                    type = ORDER_TYPE_LIMIT,
                    timeInForce = TIME_IN_FORCE_GTC,
                    quantity = quaCOCOS_ToBuy,
                    price = priceCOCOS_ToBuy)
            else:
                print('Недостатно BUSD')

            if balCOCOS > quaCOCOS_ToSell * int(priceCOCOS_ToSell):
                order2 = client.create_order(symbol='COCOSBUSD',
                    side=SIDE_SELL,                                 #ПРОДАЖ
                    type=ORDER_TYPE_LIMIT,
                    timeInForce=TIME_IN_FORCE_GTC,
                    quantity=quaCOCOS_ToSell,
                    price=priceCOCOS_ToSell)

            else:
                print('Недостатньо COCOS')
    except BinanceAPIException:
        pass



#print(order)
#print(order2)

    #print(float(crypto['bids'][0][0]))
    #print(float(crypto2['bids'][0][0]))
    #print(float(crypto3['bids'][0][0]))


    #currency = float(crypto['bids'][0][0])
    #currencytobtc = float(crypto2['bids'][0][0])
    #btcusdt = float(crypto3['bids'][0][0])
    #deposit = 100


    #res1 = deposit / currency
    #res2 = res1 * currencytobtc
    #res3 = res2 * btcusdt
   #res4 = res3 - deposit

    #if res3 >= deposit:
       # TOTAL_PROFIT += res4
        #client.sell
       # print(TOTAL_PROFIT)'''

