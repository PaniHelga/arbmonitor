
from bittrex import Bittrex


class BittrexDriver:

    fee = 0.0025
    name = "Bittrex"

    def __init__(self, api_key, secret):
        api_b='20cfb884f5c141dead2a58c56757887d'
        key_b='4d0e5ad81e574816bf047fb0d18158db'
        self.api = Bittrex(api_key, secret)
        pass

    def get_market_info(self, pairs): # to get data ask and bid for pair
        # pairs: tuple of pair (len 2)
        pair = '{0}-{1}'.format(pairs[0], pairs[1])
        try:
            ticker=self.api.get_ticker(pair)
            market=(pairs[0], pairs[1], float(ticker['result']['Ask']), float(ticker['result']['Bid']))
        except:
            market=('0','0','0','0')
        return market # list (len=4) of data main coin, currency, aks, bid

    def get_order(self, pairs):
        pair = '{0}-{1}'.format(pairs[0], pairs[1])
        try:
            orders=self.api.get_orderbook(pair, 'both')
            ask_rate=float(orders['result']['sell'][0]['Rate']) # ask-sell rate
            bid_rate=float(orders['result']['buy'][0]['Rate']) #bid-buy rate
            ask_quanity=float(orders['result']['sell'][0]['Quantity'])
            bid_quanity=float(orders['result']['buy'][0]['Quantity'])
            order={'ask_rate': ask_rate, 'ask_quanity': ask_quanity, 'bid_rate': bid_rate, 'bid_quanity': bid_quanity}
        except:
            order={'ask_rate': '0', 'ask_quanity': '0', 'bid_rate': '0', 'bid_quanity': '0'}
        return order

    def get_txFee(self):
        txfee=list()
        currencies=self.api.get_currencies()
        for i in currencies['result']:
            txfee.append((i['Currency'], i['CurrencyLong'], float(i['TxFee'])))
        return txfee # create list of tuples(len = 3) 1 - trade, 2- trade name 3 - txFee

    def create_pairs(self):
        fee = self.get_txFee()
        # txfee list of tuples(len = 3) 1 - trade, 2- trade name 3 - txFee
        firstmarket=('BTC', 'ETH', 'USDT')
        listpair=list()
        for fi in firstmarket:
            for tx in fee:
                listpair.append((fi, tx[0]))
        return listpair # create list of tuples-pair 1 - trade, 2- currency



