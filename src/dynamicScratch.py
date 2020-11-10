import pymongo
import time
import json
import requests
from DynamicFunction import getTypeMap,getUpdatedNews,loadTencentNews,loadSinaNewsList,loadSohuNewsList,loadWangyiNewsList,get_hot_news

if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost:30001/")
    Staticdb = myclient["NewsCopy"]
    Staticsave = Staticdb["news"]
    #dynamicNews = Staticdb["dynamicNews"]
    hot_news_save = Staticdb["hot"]
    type_map = getTypeMap()
    while True:
        tencent_news,tencent_hot_news = loadTencentNews()
        sina_news, sina_hot_news = loadSinaNewsList()
        hot_news_list = get_hot_news(tencent_hot_news,sina_hot_news)
        hot_news_save.drop()
        for hot_news in hot_news_list:
            hot = hot_news_save.insert_one(hot_news)
        lucene_url = "http://49.233.52.61:30002"
        updatedNews = getUpdatedNews(tencent_news,sina_news,loadSohuNewsList(),loadWangyiNewsList())
        count = 0
        #if dynamicNews.estimated_document_count() > 100:
            #dynamicNews.drop()
        post_news_list = []
        for news in updatedNews:
            if (Staticsave.count_documents({"title":news["title"]})==0):
                post_news_list.append(news)
                #x = dynamicNews.insert_one(news)
                y = Staticsave.insert_one(news)
                if news['category'] in type_map.keys():
                    mycol = Staticdb[type_map[news['category']]]
                    mycol.insert_one(news)
                count = count+1
        post_news_dict = {}
        post_news_dict['news'] = post_news_list
        res = requests.post(url=lucene_url, data=post_news_dict)
        print("not same:"+str(count))
        print("epoch end")


