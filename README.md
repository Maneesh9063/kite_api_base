# kite_api_base

stocks.txt -> MongoDB will fetch Historical data for the stocks mentioned in this list.we can update the list by simply pasting the stocks line by line.

stock_extractor -> 
It needs to be run after updating the stocks.txt file 
It takes the list in txt file and creates key value pair with stock names with id's and stores them in stock_names.pickle file


mango.py -> starts db and stores the data from kite ticker
