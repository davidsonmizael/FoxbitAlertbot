import requests

class BlinkTradeApi:
    def __init__(self, currency, crypto_currency):
        self.currency = currency
        self.crypto_currency = crypto_currency
        self.api_url = "https://api.blinktrade.com/api/v1/%s/ticker?crypto_currency=%s" % (currency, crypto_currency)
    def get_last_status(self):
        resp = requests.get(self.api_url)
        return resp.json()
    def get_buylow_variance(self):
        result = self.get_last_status()
        high = float(result["high"])
        low = float(result["low"])
        buy = float(result["buy"])

        variance = (buy / low - 1) * 100

        return variance
