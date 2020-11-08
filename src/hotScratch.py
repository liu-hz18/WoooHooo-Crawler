import pymongo
import time
from .HotFunction import getHotDetail,getHotClick,getHotComment,getNowDate

if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost:30001/")
    Staticdb = myclient["NewsCopy"]
    hot_click_save = Staticdb["hot_click"]
    hot_comment_save = Staticdb["hot_comment"]
    while True:
        nowDate = getNowDate()
        hot_click = getHotClick(nowDate)
        hot_comment = getHotComment(nowDate)
        hot_click_news = getHotDetail(hot_click)[0:10]
        hot_comment_news = getHotDetail(hot_comment)[0:10]
        delete_x = hot_click_save.delete_many({})
        delete_y = hot_comment_save.delete_many({})
        save_x = hot_click_save.insert_many(hot_click_news)
        save_y = hot_comment_save.insert_many(hot_comment_news)
        time.sleep(3600)