import json
import os
import requests
import time

class CoinmarketcapHandler:
    """ Coinmarketcap APIs handler. Connect and fetch data from Coinmarketcap APIs """

    def __init__(self):
        self.url = ''
        self.parameters = {}
        self.headers = {}

    def fetch_currencies_data(self):
        # Отримайте та поверніть дані через API Coinmarketcap
        response = requests.get(url=self.url, headers=self.headers, params=self.parameters).json()
        return response['data']


class CryptoReport(CoinmarketcapHandler):

    def __init__(self):
        super(CryptoReport, self).__init__()
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': "78e38c2d-9c05-477e-91b2-ee86c43cf8fa",
        }
        self.reports = self.get_reports()

    def get_reports(self):
        # Поверніть 6 типів звітів про криптовалюти
        reports = {
            'most traded': self.most_traded_currency(),
            'best 10': self.best_ten_currencies(),
            'worst 10': self.worst_ten_currencies(),
            'amount top 20': self.amount_top_twenty_currencies(),
            'amount by volumes': self.amount_by_volumes_currencies(),
            'gain top 20': self.gain_top_twenty_currencies()
        }

        return reports

    def most_traded_currency(self):
        # Поверніть криптовалюту з найбільшим об'ємом (у $) за останній час
        self.parameters = {
            'start': 1,
            'limit': 1,
            'sort': 'volume_24h',
            'sort_dir': 'desc',
            'convert': 'USD'
        }

        currencies = self.fetch_currencies_data()
        return currencies[0]

    def best_ten_currencies(self):
        # Поверніть найкращі 10 криптовалют на відсоткове збільшення за останній час
        self.parameters = {
            'start': 1,
            'limit': 10,
            'sort': 'percent_change_24h',
            'sort_dir': 'desc',
            'convert': 'USD'
        }

        currencies = self.fetch_currencies_data()
        return currencies

    def worst_ten_currencies(self):
        # Поверніть найгірші 10 криптовалют за відсоткове збільшення за останній час
        self.parameters = {
            'start': 1,
            'limit': 10,
            'sort': 'percent_change_24h',
            'sort_dir': 'asc',
            'convert': 'USD'
        }

        currencies = self.fetch_currencies_data()
        return currencies

    def amount_top_twenty_currencies(self):
         # Поверніть суму грошей, необхідну для придбання однієї одиниці кожної з 20 найкращих криптовалют у порядку капіталізації
        amount = 0
        self.parameters = {
            'start': 1,
            'limit': 20,
            'sort': 'market_cap',
            'sort_dir': 'desc',
            'convert': 'USD'
        }

        currencies = self.fetch_currencies_data()
        for currency in currencies:
            amount += currency['quote']['USD']['price']
        return round(amount, 2)

    def amount_by_volumes_currencies(self):
         # Поверніть суму грошей, необхідну для придбання однієї одиниці всіх криптовалют, останній 24-годинний обсяг яких перевищує $ 76 000 000
        amount = 0
        self.parameters = {
            'start': 1,
            'limit': 100,
            'volume_24h_min': 76000000,
            'convert': 'USD'
        }

        currencies = self.fetch_currencies_data()
        for currency in currencies:
            amount += currency['quote']['USD']['price']
        return round(amount, 2)

    def gain_top_twenty_currencies(self):
         # Поверніть відсоток прибутку чи збитку, який ви зробили б, якби ви придбали одну одиницю кожної з 20 найкращих криптовалют за день до цього
        initial_amount = 0
        final_amount = 0
        self.parameters = {
            'start': 1,
            'limit': 20,
            'sort': 'market_cap',
            'sort_dir': 'desc',
            'convert': 'USD'
        }

        currencies = self.fetch_currencies_data()
        for currency in currencies:
            old_price = currency['quote']['USD']['price'] / (1 + (currency['quote']['USD']['percent_change_24h'] / 100))
            initial_amount += old_price
            final_amount += currency['quote']['USD']['price']
        gain = round((((final_amount - initial_amount) / initial_amount) * 100), 1)
        return gain
