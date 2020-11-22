import pandas as pd
import pymongo,datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["ticks"]


def historical_data(inst_token , _from , _to,m ):
    mycol = mydb[str(inst_token)]

    _to = _to + datetime.timedelta(minutes=1)
    # _to = datetime.datetime(_to.year,_to.month,_to.day,_to.hour , _to.minute+1)
    l=[]
    for doc in mycol.find({'timestamp': {'$gte': _from, '$lte': _to}}) :
        l.append(doc)
        
    return pd.DataFrame(l).set_index(['timestamp'])['last_price'].resample('5Min').ohlc().dropna()


