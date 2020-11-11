import pymongo
import time
from HotFunction import hot_news_scratch

if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost:30001/")
    Staticdb = myclient["NewsCopy"]
    hot_save = Staticdb["hot"]
    while True:
        hot_news = hot_news_scratch()
        hot_save.drop()
        for news in hot_news:
            x = hot_save.insert_one(news)
        #print(hot_news)
        time.sleep(30)