import pandas as pd
import numpy as np
import requests, datetime, time, os, argparse
from coingecko_pro_api import CoinGeckoAPI
import matplotlib.pyplot as plt

if __name__ == '__main__':
    cg = CoinGeckoAPI()

    dexes = [
        'uniswap',
        'spookyswap',
        'serum_dex',
        'pancakeswap_new',
        'traderjoe',
        'quickswap',
        'sushiswap',
        'sushiswap_arbitrum',
        'spiritswap',
        'defi_kingdoms',
        'netswap',
        'ubeswap',
        'osmosis',
        'trisolaris',
        'tethys',
        'viperswap',
        'terraswap'
    ]


    btc_price = cg.get_btc_price_hist(90)

    dex_vol = {}

    for d in dexes:
        v = cg.get_exchange_vol(d, 90)
        v = [float(w[1]) for w in v]
        if len(v) < 90:
            v = [np.nan]*(90-len(v)) + v
        v = np.array(v) * btc_price
        dex_vol[d] = v

    p = pd.DataFrame(dex_vol).ewm(span=7).mean()

    plt.plot(p)
    plt.legend(p.columns)
    plt.show()
    plt.clf()
