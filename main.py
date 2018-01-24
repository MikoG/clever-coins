import time
from ExRates import MyExRates
from currency import MyCurrency
from datalogger import DataLogger
from endpoints import *

def set_transfers(accounts, payment_methods):
    accountList = accounts.get_accounts()['accounts']
    pmList = payment_methods.get_payment_methods()['payment_methods']
    
    accountID = ''
    pmID =''
    
    iii = 1
    for account in accountList:
        if account['type'] == 'wallet':
            account.update(enum=str(iii))
            print(account['enum'] + ' - ' + account['name'])
            iii += 1

    optAccount = input('Select which wallet to monitor: ')
    for account in accountList:
        if account['type'] == 'wallet':
            if account['enum'] == optAccount:
                accountID = account['id']

    print()

    iii = 1
    for pm in pmList:
        pm.update(enum=str(iii))
        print(pm['enum'] + ' - ' + pm['name'])
        iii += 1

    optAccount = input('Select which account to pay from / sell to: ')
    for pm in pmList:
        if pm['enum'] == optAccount:
            pmID = pm['id']

    return Transfers(accountID, pmID)

def loop(client, account_currency, payment_method_currency, transfers):
    sell_target = 141.00    
    quote_sell_at = 0.95          # Ratio of sell price when quotes will be obtained (0.00 to 1.00)

    exRates = MyExRates(client.client, account_currency, payment_method_currency)
    data_logger = DataLogger(exRates.dict, 'pricelog.csv')
    
    while True:
        exRates = MyExRates(client.client, account_currency, payment_method_currency)
        account = client.client.get_account(transfers.wallet)

        spot_value = exRates.spot_price * float(account['balance']['amount'])
        
        print()
        print('Account Balance: ' + str(account['balance']['amount']) + ' ' + account['balance']['currency'])
        print('Spot Price: ' + str(exRates.spot_price))
        print('Spot Value: ' + str(spot_value))
        print('Spot value at ' + str("%.2f" % (spot_value / sell_target * 100)) + '% of target (' + str(sell_target) +').')

        if spot_value > sell_target * quote_sell_at:
            quote = client.client.sell(transfers.wallet,
                            amount=str(account['balance']['amount']),
                            currency='BTC',
                            payment_method=transfers.payment_method,
                            quote=True)

            print('Spot price within ' + str(quote_sell_at * 100) + '% of target - Getting quote')
            if float(quote['total']['amount']) > sell_target:
                print('Attempting Sell')
                sell = client.client.sell(transfers.wallet,
                                amount=str(account['balance']['amount']),
                                currency=account['balance']['currency'],
                                payment_method=transfers.payment_method,
                                quote=False)
                
                print('Sold ' + sell['total']['amount'])
            else:
                print('Quote of ' + quote['total']['amount'] + ' too low - No sell')

        data_logger.add_line(exRates.dict)
        time.sleep(10)
    

def main():

    
    connected = False
    while not connected:
        myClient = MyClient()
        connected = myClient.connected

    if connected:
        myUser = MyUser(myClient.client)
        myAccounts = MyAccounts(myClient.client)
        myPaymentMethods = MyPaymentMethods(myClient.client)
        transfers = set_transfers(myAccounts, myPaymentMethods)
        
        account_currency = MyCurrency(myClient.client,
                                    myAccounts.get_account(transfers.wallet)['currency'])

        payment_method_currency = MyCurrency(myClient.client,
                                           myPaymentMethods.get_payment_method(transfers.payment_method)['currency'])

        exRates = MyExRates(myClient.client, account_currency, payment_method_currency)
        

        loop(myClient, account_currency, payment_method_currency, transfers)

if __name__ == '__main__': 
    main()
    
