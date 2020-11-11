import time
import pymongo
from HotFunction import getHotSearch

if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost:30001/")
    Staticdb = myclient["NewsCopy"]
    hot_search_save = Staticdb["hot_search"]
    while True:
        hot_search = getHotSearch()
        delete_x = hot_search_save.delete_many({})
        save_x = hot_search_save.insert_many(hot_search)
        time.sleep(900)