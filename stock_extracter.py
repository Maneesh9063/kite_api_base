from kiteconnect import KiteConnect
import os,pickle
# pahts of variables
path_of_accces_token = os.path.dirname(os.path.realpath(__file__))+"\\access_token.txt"
path_pickle_for_stock_names =  os.path.dirname(os.path.realpath(__file__))+"\\given.pickle"
path_for_buy_stats = os.path.dirname(os.path.realpath(__file__))+"\\buy_stats.txt"

api_key = "c993gnnc130qfi2p"
api_sec = "y9gnaz2ga4z11cdslsnbdd54ldqocmsm"
with open(path_of_accces_token,"r") as f:
    at = f.readline()
    # print(at)


kite = KiteConnect(api_key=api_key)
kite.set_access_token(at)
# kws = KiteTicker(api_key, at)

# pickle.dump(kite.instruments(),open("ins.pickle","wb"))
# print(pickle.load(open("ins.pickle","rb"))[0])
# print(kite.instruments())
d = kite.instruments()
g ={}


for i in d:
    if i["segment"] =="NSE":
        g[i["instrument_token"]] = {"name":i["tradingsymbol"]}

k ={}

l =[]
with open("stocks.txt","r") as f:
    s = f.readlines()
    for i in s:
        l.append(i.replace("\n",""))
    # print(l)

    for i in g:
        if g[i]["name"] in l:
            # print(g[i]["name"])

            k[i] = {"name":g[i]["name"]}
            # k[g[i]['name']] = i
    # print(k)

print(len(k))
pickle.dump(k , open("stock_names.pickle","wb"))
# pickle.dump(k , open("given.pickle","wb"))

