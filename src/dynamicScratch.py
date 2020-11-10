import pymongo
import time
from DynamicFunction import getTypeMap,getUpdatedNews,loadTencentNews,loadSinaNewsList,loadSohuNewsList,loadWangyiNewsList

if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost:30001/")
    Staticdb = myclient["NewsCopy"]
    Staticsave = Staticdb["news"]
    dynamicNews = Staticdb["dynamicNews"]
    type_map = getTypeMap()
    while True:
        updatedNews = getUpdatedNews(loadTencentNews(),loadSinaNewsList(),loadSohuNewsList(),loadWangyiNewsList())
        count = 0
        if dynamicNews.estimated_document_count() > 100:
            dynamicNews.drop()
        for news in updatedNews:
            if (Staticsave.count_documents({"title":news["title"]})==0 and Staticsave.count_documents({"url":news["url"]})==0 ):
                x = dynamicNews.insert_one(news)
                y = Staticsave.insert_one(news)
                if news['category'] in type_map.keys():
                    mycol = Staticdb[type_map[news['category']]]
                    mycol.insert_one(news)
                count = count+1
        print("not same:"+str(count))
        print("epoch end")
        time.sleep(60)


