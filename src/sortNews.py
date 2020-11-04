import pymongo
if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost/")
    mydb = myclient["StaticNews"]
    newsSet = mydb["news"]
    mydata = newsSet.find().sort([("publish_time", pymongo.DESCENDING)])
    newsCopy = myclient["NewsCopy"]
    saveCopy = newsCopy["news"]
    title_map={}
    count = 0
    for news in mydata:
        if news["title"] not in title_map.keys():
            title_map[news["title"]] = 1
            x = saveCopy.insert_one(news)
        count = count + 1
        if count % 10000 == 0:
            print(count)


