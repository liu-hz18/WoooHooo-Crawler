import pymongo
import time
from DynamicFunction import getTypeMap,getUpdatedNews,loadTencentNews,loadSinaNewsList,loadSohuNewsList,loadWangyiNewsList,get_hot_news

if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost:30001/")
    Staticdb = myclient["NewsCopy"]
    Staticsave = Staticdb["news"]
    dynamicNews = Staticdb["dynamicNews"]
    hot_news_save = Staticdb["hot"]
    type_map = getTypeMap()
    while True:
        tencent_news,tencent_hot_news = loadTencentNews()
        sina_news, sina_hot_news = loadSinaNewsList()
        hot_news_list = get_hot_news(tencent_hot_news,sina_hot_news)
        hot_news_save.drop()
        for hot_news in hot_news_list:
            hot = hot_news_save.insert_one(hot_news)
        updatedNews = getUpdatedNews(tencent_news,sina_news,loadSohuNewsList(),loadWangyiNewsList())
        count = 0
        if dynamicNews.estimated_document_count() > 100:
            dynamicNews.drop()
        for news in updatedNews:
            if (Staticsave.count_documents({"title":news["title"]})==0):
                x = dynamicNews.insert_one(news)
                y = Staticsave.insert_one(news)
                if news['category'] in type_map.keys():
                    mycol = Staticdb[type_map[news['category']]]
                    mycol.insert_one(news)
                count = count+1
        print("not same:"+str(count))
        print("epoch end")
        time.sleep(60)


