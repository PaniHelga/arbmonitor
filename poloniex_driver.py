
from poloniex import Poloniex


class PoloniexDriver:

    fee = 0.0025
    name = "Poloniex"

    def __init__(self, api_key, secret):
        api_p=''
        key_p=''
        self.api=Poloniex(api_key, secret)
        pass

        
    def get_market_info(self):
        market={}
        try:
            tickers=self.api.returnTicker()
            for pairs, ticker in tickers.iteritems():
                pair=pairs.split('_')
                pair=tuple(pair)
                market[pair]=(float(ticker['lowestAsk']), float(ticker['highestBid']))                   
        except:
            market={}
        return market

        
    def get_txFee(self):
        txfee=list()
        currencies=self.api.returnCurrencies()
        for k, v in currencies.iteritems():
            txfee.append(( k, v['name'], v['txFee'])) # create list of tuples(len = 2) 1 - trade, 2- trade name 3 - txFee
        return txfee

        
    def get_order(self, pairs): # return from lists sells and buy
        pair = '{0}_{1}'.format(pairs[0], pairs[1])
        try:
            orders=self.api.returnOrderBook(pair,1) # return lists sells and buy
            ask_rate=float(orders['asks'][0][0]) # ask-sell rate
            bid_rate=float(orders['bids'] [0][0])#bid-buy rate
            ask_quanity=float(orders['asks'][0][1])
            bid_quanity=float(orders['bids'] [0][1])
            order={'ask_rate': ask_rate, 'ask_quanity': ask_quanity, 'bid_rate': bid_rate, 'bid_quanity': bid_quanity}
        except:
            order={'ask_rate': '0', 'ask_quanity': '0', 'bid_rate': '0', 'bid_quanity': '0'}
        return order


