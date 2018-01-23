## ExRates deals with the public part of the API, data that can be obtained without a valid API key.
#  it retrieves the information:
#  - Server time and date - This is the time and date on the coinbase servers
#  - Exchange Rates       - The current exhange rate between any two currencies
#  - Spot Price           - The actual value of the currency at the time of the request (this value is what is displayed on the coinbase dashboard)
#  - Buy price            - The exhange rate being used for coin purchases (this is a generic rate, actual rates during purchase will depend on individual cirumstanes)
#  - Sell Price           - The exhange rate being used for coin sales (this is a generic rate, actual rates during sale will depend on individual cirumstanes)
#
#  All value will be refreshed when the class is instantiated and can be retrieved using the getter methods. To refresh the values just create a new instance.
class MyExRates():

    def __init__(self, client, currency1, currency2):
        self.__client = client
        self.__currency1 = currency1
        self.__currency2 = currency2
        self.__currency_pair = currency1.get_currency_id() + currency2.get_currency_id()

        self.__refresh_time()
        self.__refresh_exchange_rate()
        self.__refresh_buy_price()
        self.__refresh_sell_price()
        self.__refresh_spot_price()

    def __refresh_time(self):
        strAPITime = self.__client.get_time()
        self.__date = strAPITime['iso'][:10]
        self.__time = strAPITime['iso'][11:19]
        self.__epoch = int(strAPITime['epoch'])

    def __refresh_exchange_rate(self):
        rates = self.__client.get_exchange_rates(currency = self.__currency1.get_currency_id())
        assert rates['currency'] == self.__currency1.get_currency_id(), 'Returned exchange rate does not match the requested currencies'
        self.__exchange_rate  = float(rates['rates'][self.__currency2.get_currency_id()])

    def __refresh_buy_price(self):
        price_data = self.__client.get_buy_price(currency_pair = self.__currency_pair)
        assert price_data['base'] == self.__currency1.get_currency_id() and price_data['currency'] == self.__currency2.get_currency_id(), 'Returned buy price does not match the requested currencies'
        self.__buy_price = float(price_data['amount'])

    def __refresh_sell_price(self):
        price_data = self.__client.get_sell_price(currency_pair = self.__currency_pair)
        assert price_data['base'] == self.__currency1.get_currency_id() and price_data['currency'] == self.__currency2.get_currency_id(), 'Returned sell price does not match the requested currencies'
        self.__sell_price = float(price_data['amount'])

    def __refresh_spot_price(self):
        price_data = self.__client.get_spot_price(currency_pair = self.__currency_pair)
        assert price_data['base'] == self.__currency1.get_currency_id() and price_data['currency'] == self.__currency2.get_currency_id(), 'Returned spot price does not match the requested currencies'
        self.__spot_price = float(price_data['amount'])

    @property
    def date(self):
        return self.__date

    @property
    def time(self):
        return self.__time

    @property
    def epoch(self):
        return self.__epoch

    @property
    def exchange_rate(self):
        return self.__exchange_rate

    @property
    def buy_price(self):
        return self.__buy_price

    @property
    def sell_price(self):
        return self.__sell_price

    @property
    def spot_price(self):
        return self.__spot_price
