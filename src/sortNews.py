import pymongo
if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost:30001/")
    mydb = myclient["StaticNews"]
    newsSet = mydb["news"]
    mydata = newsSet.find().sort([("publish_time", pymongo.DESCENDING)])
    newsCopy = myclient["NewsCopy"]
    saveCopy = newsCopy["news"]
    count = 0
    new_count = 0
    for news in mydata:
        if (saveCopy.count_documents({"title": news["title"]}) == 0):
            x = saveCopy.insert_one(news)
            new_count = new_count + 1
        count = count + 1
        if count % 10000 == 0:
            print(count)
            print("not same"+str(new_count))


