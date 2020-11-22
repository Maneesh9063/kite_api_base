import pymongo
import pickle,time,datetime
from kiteconnect import KiteConnect,KiteTicker
import concurrent.futures,threading,os


print(datetime.datetime.now())
# pahts of variables
path_of_accces_token = os.path.dirname(os.path.realpath(__file__))+"\\access_token.txt"
path_pickle_for_stock_names =  os.path.dirname(os.path.realpath(__file__))+"\\stock_names.pickle"

d  = pickle.load(open(path_pickle_for_stock_names,"rb"))
# subscribe=[1215745]
subscribe=[]

for i in d:
    subscribe.append(i)

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

# acces_token_generator()
# this is used to cath any accestoken exceptions 
# kite.session_expiry_hook = acces_token_generator

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["ticks"]


def insert(ticks):
    
    # print(str(i["instrument_token"]))
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["ticks"]

    for i in ticks:
        mycol = mydb[str(i["instrument_token"])]
        # i["_id"] = i.pop("timestamp")
        try:
            mycol.insert_one(i)
        except Exception as e:
            print(e)
            pass


number_of_threads = 10

def on_ticks(ws,ticks):
    # ticks = ticks[:50]
    ticks_len = len(ticks)
    t1 = time.perf_counter()
    

    try:
        t = threading.Thread(target=insert,args=(ticks,))
        t.start()
        # mycol.insert_one(i)
    except Exception as e:
        print(e)
        pass


    print(time.perf_counter()-t1 , ticks_len)    
    
# subscribe = subscribe[:50]
def on_connect(ws, response):
    ws.subscribe(subscribe)
    ws.set_mode(ws.MODE_FULL, subscribe)

kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.connect()


