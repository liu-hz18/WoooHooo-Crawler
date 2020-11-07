import requests
import demjson
import json
from bs4 import BeautifulSoup
import pymongo
import time
from .DynamicFunction import getTypeMap,getUpdatedNews,loadTencentNews,loadSinaNewsList,loadSohuNewsList,loadWangyiNewsList

if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost:30001/")
    Staticdb = myclient["NewsCopy"]
    Staticsave = Staticdb["news"]
    type_map = getTypeMap()
    while True:
        updatedNews = getUpdatedNews(loadTencentNews(),loadSinaNewsList(),loadSohuNewsList(),loadWangyiNewsList())
        count = 0
        for news in updatedNews:
            if (Staticsave.count_documents({"title":news["title"]}))==0:
                y = Staticsave.insert_one(news)
                if news['category'] in type_map.keys():
                    mycol = Staticdb[type_map[news['category']]]
                    mycol.insert_one(news)
                count = count+1
        print("not same:"+str(count))
        print("epoch end")
        time.sleep(60)


