import pymongo
from .DynamicFunction import getClassifyMap

def createIndex(mydb):
    kind_list = ["politics","history","social","chuguo","mil","finance","ent","sports","science","game"]
    for kind in kind_list:
        myCol=mydb[kind]
        myCol.create_index([('title', 1)], unique=True)
        myCol.create_index([('publish_time', pymongo.DESCENDING)])

if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost:30001/")
    mydb = myclient["NewsCopy"]
    newsSet = mydb["news"]
    type_map = getClassifyMap()
    createIndex(mydb)
    for news in newsSet.find():
        category=news['category']
        if category in type_map.keys():
            mycol=mydb[type_map[category]]
            mycol.insert_one(news)
        else:
            continue
    print(mydb.list_collection_names())
