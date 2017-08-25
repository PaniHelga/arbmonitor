
import time
import json

from bittrex_driver import BittrexDriver
from poloniex_driver import PoloniexDriver


def check_pair_on_exchanges(pair, pair_ex1, pair_ex2, ex1, ex2, btc_size):

    if pair_ex1['ask_rate'] != 0 and pair_ex2['ask_rate'] != 0:
        ask1 = float(pair_ex1['ask_rate'])
        bid1 = float(pair_ex1['bid_rate'])
        ask2 = float(pair_ex2['ask_rate'])
        bid2 = float(pair_ex2['bid_rate'])
        if ask1 < bid2 and ask1 > 0:
            lot = btc_size / ask1
            max_lot = min(pair_ex2['bid_quanity'], pair_ex1['ask_quanity'], lot)
            benefit = bid2 * (1.0 - ex2.fee) - ask1*(1.0 - ex1.fee)
            benefit_total = benefit * max_lot
            percentage = benefit/ask1*100
            if benefit > 0 and percentage > 0:
                print("---------------------------------------------------------------------------------------------")
                print("buy " + pair[0] + "/" + pair[1] + " on " + ex1.name + " @" + '{0:.9f}'.format(ask1) +
                      " sell on " + ex2.name + " @" + '{0:.9f}'.format(bid2))

                print("price difference in " + pair[1] +": " + '{0:.9f}'.format(benefit) +
                      " or " + "~" + '{0:.1f}'.format(benefit/ask1*100) + "%")

                print("Max available lot: " + '{0:.9f}'.format(max_lot) + " in " + pair[1] + "; profit: " +
                      '{0:.9f}'.format(benefit_total) + "BTC" + " or " +
                      '{0:.9f}'.format(benefit_total/ask1) + "in " + pair[1])

        elif ask2 < bid1 and ask2 > 0:
            lot = btc_size / ask2
            max_lot = min(pair_ex2['bid_quanity'], pair_ex1['ask_quanity'], lot)
            benefit = bid1 * (1.0 - ex2.fee) - ask2*(1.0 - ex1.fee)
            benefit_total = benefit * max_lot
            percentage = benefit/ask2*100
            if benefit > 0 and percentage > 0:
                print("---------------------------------------------------------------------------------------------")
                print("buy " + pair[0] + "/" + pair[1] + " on " + ex2.name + " @" + '{0:.9f}'.format(ask2) +
                      " sell on " + ex1.name + " @" + '{0:.9f}'.format(bid1))

                print("price difference in " + pair[1] +": " + '{0:.9f}'.format(benefit) +
                      " or " + "~" + '{0:.1f}'.format(benefit/ask2*100) + "%")

                print("Max available lot: " + '{0:.9f}'.format(max_lot) + " in " + pair[1] + "; profit: " +
                      '{0:.9f}'.format(benefit_total) + "BTC" + " or " +
                      '{0:.9f}'.format(benefit_total/ask2) + "in " + pair[1])


def check_arbitrage(pairs, drivers):
    for pair in pairs:
        pair_result = []
        for d in drivers:
            pair_result.append(d.get_order(pair))

        for k in range(len(drivers)):
            for j in range(k+1, len(drivers)):
                check_pair_on_exchanges(pair, pair_result[k], pair_result[j], drivers[k], drivers[j], 0.1)


drivers = []


def load_config():

    with open('arbmonitor.conf') as data_file:    
        cfg = json.load(data_file)

    return cfg


def init():
    cfg = load_config()
    b=BittrexDriver(cfg["Bittrex"]["apikey"], cfg["Bittrex"]["secret"])
    p=PoloniexDriver(cfg["Poloniex"]["apikey"], cfg["Poloniex"]["secret"])
    drivers.append(b);
    drivers.append(p);


def collect_pairs():
    # a bit of hardcode
    return drivers[0].create_pairs()


def run():
    init()

    coin_pairs = collect_pairs()

    while True:
        check_arbitrage(coin_pairs, drivers)
        time.sleep(5)
        print("next iteration")
        break


run()

