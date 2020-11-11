import pymongo
import time
import json
import requests
from DynamicFunction import getTypeMap,getUpdatedNews,loadTencentNews,loadSinaNewsList,loadSohuNewsList,loadWangyiNewsList,get_hot_news

if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost:30001/")
    Staticdb = myclient["NewsCopy"]
    Staticsave = Staticdb["news"]
    hot_news_save = Staticdb["hot"]
    type_map = getTypeMap()
    while True:
        updatedNews = getUpdatedNews(loadTencentNews(),loadSinaNewsList(),loadSohuNewsList(),loadWangyiNewsList())
        count = 0
        post_news_list = []
        for news in updatedNews:
            if (Staticsave.count_documents({"title":news["title"]})==0):
                post_news_list.append(news)
                y = Staticsave.insert_one(news)
                if news['category'] in type_map.keys():
                    mycol = Staticdb[type_map[news['category']]]
                    mycol.insert_one(news)
                count = count+1
        post_news_dict = {}
        post_news_dict['news'] = post_news_list
        #res = requests.post(url=lucene_url, data=post_news_dict)
        print("not same:"+str(count))
        print("epoch end")


