
from poloniex import Poloniex


class PoloniexDriver:

    fee = 0.0025
    name = "Poloniex"

    def __init__(self, api_key, secret):
        api_p='UR0WOR8H-A8A45PZX-XWQ6BCS1-8T1D2XZN'
        key_p='bccb9947c68c835c1085f0dd8434824225069c6538fda2747e22b382466e3e60d752d5c56852e231f5c24b5ee736588811f51fc691fc266f6b14f50f6d6e0c39'
        self.api=Poloniex(api_key, secret)
        pass

    def get_market_info(self, pairs):
        pair = '{0}_{1}'.format(pairs[0], pairs[1])
        try:
            ticker=self.api.returnTicker()[pair]
            market=(pairs[0], pairs[1], float(ticker['lowestAsk']), float(ticker['highestBid']))
        except:
            market=('0','0','0','0')
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


