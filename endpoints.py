import os
import json
import coinbase
from coinbase.wallet.client import Client
from coinbase.wallet.error import APIError

class Endpoint:
    FILE_NAME = ''

    def write_json(self, obj):
        JSON = json.dumps(obj, indent=4)
        f = open('data/' + self.FILE_NAME, 'w')
        f.write(JSON)
        f.close()

    def read_json(self):
        f = open('data/' + self.FILE_NAME, 'r')
        JSON = json.load(f)
        f.close()
        return JSON

class MyClient(Endpoint):
    client = None
    connected = False

    API_VERSION = '2018-01-16'

    def __init__(self):
        self.FILE_NAME = 'cb_client.json'
        try:
            clientDict = Endpoint.read_json(self)
        except IOError as err:
            APIKey = ''
            while len(APIKey) == 0:
                APIKey= input('Please enter your API Key:')
                
            APISecret = ''
            while len(APISecret) == 0:
                APISecret = input('Please enter your API Secret:')
            
            clientDict = {'APIKey': APIKey, 'APISecret': APISecret}
            Endpoint.write_json(self, clientDict)
            clientDict = Endpoint.read_json(self)
        
        self.client = Client(clientDict['APIKey'], clientDict['APISecret'], api_version=self.API_VERSION)

        try:
            user = self.client.get_current_user()
        except APIError as err:
            print('Unable to communicate with coinbase User API.')
            print('Error: ' + err.message)
            os.remove(Endpoint.FILE_NAME)
        else:
            self.connected = True
            print('API Connection Successful.')


            
class MyUser(Endpoint):
    user = None
    name = ''
    uid = ''
    local_curr = ''

    def __init__(self, client):
        self.FILE_NAME = 'cb_user.json'
        self.user = client.get_current_user()
        self.name = self.user['name']
        self.local_curr = self.user['native_currency']
        self.uid = self.user['id']
        Endpoint.write_json(self, {'name': self.name, 'id': self.uid, 'native_currency': self.local_curr})

class MyPaymentMethods(Endpoint):
    pms = None

    def __init__(self, client):
        self.FILE_NAME = 'cb_payment_methods.json'
        pms = client.get_payment_methods()
        self.pms = {'payment_methods': []}
        for pm in pms.data:
            pmDict = {'id': pm['id'], 'name': pm['name'], 'currency': pm['currency']}
            self.pms['payment_methods'].append(pmDict)

        Endpoint.write_json(self, self.pms)

    def get_payment_methods(self):
        return self.pms

    def get_payment_method(self, payment_method_id):
        for pm in self.pms['payment_methods']:
                    if pm['id'] == payment_method_id:
                        return pm

class MyAccounts(Endpoint):
    accounts = None

    def __init__(self, client):
        self.FILE_NAME = 'cb_accounts.json'
        accounts = client.get_accounts()

        self.accounts = {'accounts': []}
        for account in accounts.data:
            accountDict = {'id': account['id'],
                           'name': account['name'],
                           'currency': account['currency']['code'],
                           'type':account['type']}
            
            self.accounts['accounts'].append(accountDict)

        Endpoint.write_json(self, self.accounts)

    def get_accounts(self):
        return self.accounts

    def get_account(self, account_id):
        for account in self.accounts['accounts']:
            if account['id'] == account_id:
                return account

class Transfers(Endpoint):
    wallet = ''
    payment_method = ''

    def __init__(self, wallet='', payment_method=''):
        self.FILE_NAME = 'cb_transfers.json'

        self.wallet = wallet
        self.payment_method = payment_method
        
        Endpoint.write_json(self, {'wallet': wallet, 'payment_method': payment_method})

    def get_transfers(self):
        return Endpoint.read_json(self)


