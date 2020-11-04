import pymongo
if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost/")
    mydb = myclient["StaticNews"]
    newsSet = mydb["news"]
    mydata = newsSet.find()
    title_list = []
    for news in mydata:
        if news['title'] not in title_list:
            title_list.append(news['title'])
            #print(news)
    print(len(title_list))


