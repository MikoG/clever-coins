class MyCurrency:

    __client = None
    __currencyData = None
    
    def  __init__(self, client, currency1 = 'BTC'):
        self.__client = client
        dataCryptoCurrency = self.__client.get_currencies()
        for curr in dataCryptoCurrency.data:
            if curr['id'] == currency1:
                self.__currencyData = curr

    def get_currency_name(self):
        return self.__currencyData['name']

    def get_currency_id(self):
        return self.__currencyData['id']

    def get_currency_min_size(self):
        return self.__currencyData['min_size']

    def debug_dict(self):
        print(self.__currencyData)
