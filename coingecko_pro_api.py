import pycoingecko, json, requests
import numpy as np

CG_API_URL_BASE = 'https://pro-api.coingecko.com/api/v3/'

def get_api_key():
    with open('cg_pro_api_key.json') as f:
        return json.load(f)['key']

class CoinGeckoAPI(pycoingecko.CoinGeckoAPI):
    def __init__(self):
        super().__init__(api_base_url=CG_API_URL_BASE)
        self.key = get_api_key()

    def __request(self, url):
        headers = {'X-Cg-Pro-Api-Key': self.key}
        try:
            response = self.session.get(url, headers=headers, timeout=self.request_timeout)
        except requests.exceptions.RequestException:
            raise

        try:
            response.raise_for_status()
            content = json.loads(response.content.decode('utf-8'))
            return content
        except Exception as e:
            # check if json (with error message) is returned
            try:
                content = json.loads(response.content.decode('utf-8'))
                raise ValueError(content)
            # if no json
            except json.decoder.JSONDecodeError:
                pass

            raise

    def request_wrapper(self, func, kwargs={}):
        try:
            return func(**kwargs)
        except requests.exceptions.HTTPError:
            print('Request error. Retrying in 30 seconds...')
            time.sleep(30)
            return request_wrapper(func, kwargs)


    # get exchange volume (in BTC) for last number of days
    def get_exchange_vol(self, exchange_id, days):
        func = self.get_exchanges_volume_chart_by_id
        kwargs = {
            'id': exchange_id,
            'days': days
        }
        return self.request_wrapper(func, kwargs)


    def get_btc_price_hist(self, days):
        func = self.get_coin_market_chart_by_id
        kwargs = {
            'id': 'bitcoin',
            'vs_currency': 'usd',
            'days': days-1,
            'interval': 'daily'
        }
        response = self.request_wrapper(func, kwargs)
        prices = [p[1] for p in response['prices']]

        return np.array(prices)
