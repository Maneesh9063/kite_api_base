from kiteconnect import KiteConnect
import datetime,os,time


# pahts of variables
path_of_accces_token = os.path.dirname(os.path.realpath(__file__))+"\\access_token.txt"
path_pickle_for_stock_names =  os.path.dirname(os.path.realpath(__file__))+"\\given.pickle"
path_for_buy_stats = os.path.dirname(os.path.realpath(__file__))+"\\buy_stats.txt"

# vairables 
api_key = "c993gnnc130qfi2p"
api_sec = "y9gnaz2ga4z11cdslsnbdd54ldqocmsm"
with open(path_of_accces_token,"r") as f:
    at = f.readline()
    # print(at)

# kite connect settings

kite = KiteConnect(api_key=api_key)
kite.set_access_token(at)

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

while True:

    try:
        d = kite.orders()

        for i in d:

            time_at = i["order_timestamp"]
            try:
                if "TRIGGER PENDING" in i["status"]  and time_at  <= datetime.datetime.now() -datetime.timedelta(minutes= 3) :
                    print("cancelled" , kite.cancel_order(variety=kite.VARIETY_REGULAR ,order_id =i["order_id"]) , i["tradingsymbol"])
            except Exception as e:
                print("no order " , e)

        time.sleep(2)
    except Exception as e:
        print(e)
        continue

# d = kite.orders()
# print(d)
