
from nsepython import *
import logging
from kiteconnect import *

'''
# The BankNIFTY Golden Ratio Strategy
##Scrip = BANKNIFTY Futures

## Golden Number = ((Previous Day High - Previous Day Low) + Opening Range of Today's First 10 minutes))*61.8%

### Buy Above = (Previous Day Close + Golden Number)
### Sell Below = (Previous Day Close - Goldern Number)

#### Stop Loss at 0.5% Target at 2%
'''



'''
Zerodha info
'''
zerodha_id = ""
zerodha_password = ""
zerodha_pin = ""
zerodha_api_key = ""
zerodha_api_secret = ""
zerodha_access_token = ""


banknifty_info = nse_quote_meta("BANKNIFTY", "latest", "Fut")

fetch_url = "https://www.nseindia.com/api/historical/fo/derivatives?&expiryDate=" + str(
    banknifty_info['expiryDate']) + "&instrumentType=FUTIDX&symbol=BANKNIFTY"
historical_data = nsefetch(fetch_url)
historical_data = pd.DataFrame(historical_data['data'])
previous_day_high = float(historical_data['FH_TRADE_HIGH_PRICE'].iloc[0] )
previous_day_low = float(historical_data['FH_TRADE_LOW_PRICE'].iloc[0])

range_high = banknifty_info['highPrice']
range_low = banknifty_info['lowPrice']
opening_range = range_high - range_low

golden_number = (float(previous_day_high) - float(previous_day_low) + opening_range) * .618

previous_day_close = float(banknifty_info['prevClose'])
buy_above = int(previous_day_close + golden_number)
sell_below = int(previous_day_close - golden_number)

print("Buy BankNIFTY Above: " + str(buy_above) + ".")
print("Sell BankNIFTY Below: " + str(sell_below) + ".")

# Entering the Trade



# Managing the Trade
def main():
    global kite
    kite = KiteConnect(api_key=zerodha_api_key)
    #get_access_token()
    kite.set_access_token(zerodha_access_token)
    # print(kite.orders())
    while True:

        bn_ltp = nse_quote_ltp("BANKNIFTY", "latest", "Fut")
        print("Current Value of BankNIFTY: " + str(bn_ltp))

        is_triggered = "NONE"

        #  Test
        bn_ltp = 21249

        if (bn_ltp > buy_above): ## also need to check open positions
            print("Buy Order executed at: " + str(bn_ltp) + ". Entry Time is " + str(run_time) + ".")
            is_triggered = "BUY"
            stop_loss = bn_ltp * (.995)
            target = bn_ltp * (1.02)
            try:
                kite.place_order( variety= kite.VARIETY_BO,
                                exchange= kite.EXCHANGE_NFO,            # NFO or NSE
                                tradingsymbol="BANKNIFTY20SEPFUT",
                                transaction_type= kite.TRANSACTION_TYPE_BUY,
                                quantity=25,
                                product= kite.PRODUCT_BO,
                                order_type= kite.ORDER_TYPE_LIMIT,
                                price=bn_ltp,
                                validity=None,
                                disclosed_quantity=None,
                                trigger_price=None,
                                squareoff=target - bn_ltp,
                                stoploss=bn_ltp - stop_loss,
                                trailing_stoploss=None,
                                tag= "algo_test")
            except Exception as e :
                print("Error while placing order : {}".format(e.args))
            break
        elif (bn_ltp < sell_below):
            print("Sell Order executed at: " + str(bn_ltp) + ". Entry Time is " + str(run_time) + ".")
            is_triggered = "SELL"
            stop_loss = bn_ltp * (1.005)
            target = bn_ltp * (.98)
            try:
                kite.place_order( variety= kite.VARIETY_BO,
                                exchange= kite.EXCHANGE_NFO,            # NFO or NSE
                                tradingsymbol="BANKNIFTY20SEPFUT",
                                transaction_type= kite.TRANSACTION_TYPE_SELL,
                                quantity=25,
                                product= kite.PRODUCT_BO,
                                order_type= kite.ORDER_TYPE_LIMIT,
                                price=bn_ltp,
                                validity=None,
                                disclosed_quantity=None,
                                trigger_price=None,
                                squareoff= bn_ltp - target,
                                stoploss= stop_loss - bn_ltp,
                                trailing_stoploss=None,
                                tag= "algo_test")
            except Exception as e :
                print("Error while placing order : {}".format(e.args))

            break
        time.sleep(10)

if __name__ == '__main__':
    main()