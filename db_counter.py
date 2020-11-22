from kiteconnect import KiteConnect,KiteTicker
import pandas as pd
import datetime,os,run
import time,pickle
# pahts of variables
path_of_accces_token = os.path.dirname(os.path.realpath(__file__))+"\\access_token.txt"
path_for_buy_stats = os.path.dirname(os.path.realpath(__file__))+"\\buy_stats.txt"
path_for_sell_stats = os.path.dirname(os.path.realpath(__file__))+"\\sell_stats.txt"
path_pickle_for_stock_names =  os.path.dirname(os.path.realpath(__file__))+"\\given.pickle"

# vairables 
api_key = "c993gnnc130qfi2p"
api_sec = "y9gnaz2ga4z11cdslsnbdd54ldqocmsm"
with open(path_of_accces_token,"r") as f:
    at = f.readline()
    # print(at)

# kite connect settings

kite = KiteConnect(api_key=api_key)
kite.set_access_token(at)
kws = KiteTicker(api_key, at)

# No need of thinking about the acces token
# if it is invalid it automatically ask's for the requet token

def acces_token_generator():
    global at
    print("[*] Generate access Token : ",kite.login_url())
    request_tkn = input("[*] Enter Your Request Token Here : ")[-32:]
    data = kite.generate_session(request_tkn, api_sec)
    with open(path_of_accces_token,"w") as f:
        f.write(data["access_token"])
    at = data["access_token"]
    print("Your access token is : " , data["access_token"])

# this is used to cath any accestoken exceptions 
kite.session_expiry_hook = acces_token_generator

trd_portfolio = pickle.load(open(path_pickle_for_stock_names, "rb"))
subscribe = []
for i in trd_portfolio:
    trd_portfolio[i]["bought"] = False
    trd_portfolio[i]["sold"] = False
    # subscribe.append("NSE:"+trd_portfolio[i])
    subscribe.append(i)

def mix_counter_order():
    while True:
        try:
            print("-----------------------------------------------------------------------------")
            t = time.perf_counter()
            c_positions = kite.positions()['net']
            # print((t-time.perf_counter()))

            if len(c_positions) > 0:
                # print("for positions ",(t-time.perf_counter()))
                
                for postion_retrived in c_positions:
                    c_quantity = postion_retrived["quantity"]
                    c_instrument_token = postion_retrived["instrument_token"]
                    # print("----------for  ",(t-time.perf_counter()))

                    if c_quantity > 0 and postion_retrived["product"] == "MIS":

                        n = datetime.datetime.now()
                        c_to = datetime.datetime(n.year, n.month, n.day,n.hour,n.minute)
                        c_from =  c_to - datetime.timedelta(minutes=1)
                        # c_df = pd.DataFrame(kite.historical_data(c_instrument_token,c_from,c_to,'minute'))
                        c_df = run.historical_data(c_instrument_token,c_from,c_to,'minute')
                        print(c_df)
                        # print((t-time.perf_counter()))

                        # c_9_ma = round((c_df["close"][-9:].mean()),2)
                        # print((t-time.perf_counter()))

                        c_name = postion_retrived["tradingsymbol"]

                        # c_ltp = c_df.iloc[-1]["close"]
                        # c_ltp = kite.ltp("NSE:"+c_name)["NSE:"+c_name]["last_price"]
                        
                        c_ltp = refiner_dict[c_instrument_token]["last_price"]

                        print(c_name ,c_ltp, c_df.iloc[0]["low"] ,c_quantity)
                        # print(c_name ,c_ltp , c_d.iloc[-2]["low"] ,c_quantity)

                        if not trd_portfolio[c_instrument_token]["sold"] and (c_ltp <  c_df.iloc[0]["low"]): 
                            # or c_ltp < c_9_ma) : 
                            # print(c_name ,c_ltp, c_df.iloc[-2]["low"] ,c_quantity)

                            try:
                                ord_id = kite.place_order(variety = kite.VARIETY_REGULAR , exchange = kite.EXCHANGE_NSE, tradingsymbol = c_name,quantity = c_quantity, product = kite.PRODUCT_MIS , transaction_type = kite.TRANSACTION_TYPE_SELL, order_type = kite.ORDER_TYPE_MARKET)
                                trd_portfolio[i]["sold"] = True
                                with open(path_for_sell_stats,"a") as f:
                                    co_o = "exited order "+str(ord_id) +c_name+" "+str(datetime.datetime.now())+ "\n"
                                    f.write(co_o)
                            except:
                                print("jj")
                            
                            print("exited order "+str(ord_id) , c_name , datetime.datetime.now())
                        
                    elif c_quantity < 0 and postion_retrived["product"] == "MIS":

                        n = datetime.datetime.now()
                        c_to = datetime.datetime(n.year, n.month, n.day,n.hour,n.minute)
                        c_from =  c_to - datetime.timedelta(minutes=1)
                       
                        # c_df = pd.DataFrame(kite.historical_data(c_instrument_token,c_from,c_to,'minute'))
                        
                        # print((t-time.perf_counter()))

                        # c_9_ma = round((c_df["close"][-9:].mean()),2)
                        # print((t-time.perf_counter()))

                        c_name = postion_retrived["tradingsymbol"]
                        # c_ltp = c_df.iloc[-1]["close"]
                        c_ltp = refiner_dict[c_instrument_token]["last_price"]
                        c_df = (run.historical_data(c_instrument_token,c_from,c_to,'minute'))
                        print(c_name)
                        print(c_df)
                        # print(c_name ,c_ltp, c_9_ma ,c_quantity)
                        print(c_name ,c_ltp , c_df.iloc[0]["high"] ,c_quantity)
                        # print(c_name ,c_ltp , c_d.iloc[-2]["low"] ,c_quantity)


                        if not trd_portfolio[c_instrument_token]["bought"] and c_ltp > c_df.iloc[0]["high"]:# or c_ltp > c_9_ma :
                            # print(c_name ,c_ltp, c_9_ma ,c_quantity)
                            try:
                                
                                ord_id = kite.place_order(variety = kite.VARIETY_REGULAR , exchange = kite.EXCHANGE_NSE, tradingsymbol =  c_name,quantity = -c_quantity, product = kite.PRODUCT_MIS , transaction_type = kite.TRANSACTION_TYPE_BUY, order_type = kite.ORDER_TYPE_MARKET)
                                with open(path_for_buy_stats,"a") as f:
                                    co_o = "exited order "+ord_id +c_name+" "+str(datetime.datetime.now())+ "\n"

                                    f.write(co_o)
                                trd_portfolio[c_instrument_token]["bought"] = True

                            except:
                                print("jj")
                            
                            print("exited order" , c_name , datetime.datetime.now())
                    else:
                    # elif c_quantity ==0:
                        # print("breaked")
                        break
                    print("for one loop ",(t-time.perf_counter()))

        except Exception as e :
            print("exception in counter ",e)
        
        time.sleep(1)
        print("Total ",(t-time.perf_counter()))



# mix_counter_order()

   
refiner_dict = {}
def on_ticks(ws,ticks):
    # print(datetime.datetime.now().time().second)

    for i in ticks:
        refiner_dict[i["instrument_token"]] = i
        # pass
    # print(len(ticks))
    ws.set_mode(ws.MODE_LTP, subscribe)


def on_connect(ws, response):
    ws.subscribe(subscribe)
    ws.set_mode(ws.MODE_LTP, subscribe)

kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.connect(threaded=True)

while True:
    mix_counter_order()
