import copy
import pymongo
import json
import time
import threading
import requests
from DynamicFunction import get_tencent_channel,get_sina_channel,get_wangyi_channel,loadTencentNews,loadSinaNews,loadSohuNews,loadWangyiNews,getTypeMap
from HotFunction import hot_news_scratch
R = threading.Lock()

def save_db(updatedNews,hot_news):
    myclient = pymongo.MongoClient("mongodb://localhost:30001/")
    Staticdb = myclient["NewsCopy"]
    Staticsave = Staticdb["news"]
    hot_save = Staticdb["hot"]
    type_map = getTypeMap()
    hot_save.drop()
    for news in hot_news:
        copy_news = copy.deepcopy(news)
        x = hot_save.insert_one(copy_news)
    updateNews.extend(hot_news)
    http_prefix = "http:"
    host = "49.233.52.61"
    lucene_url = f"{http_prefix}//{host}:30002/postNews/"
    count = 0
    post_news_list = []
    for news in updatedNews:
        copy_news = copy.deepcopy(news)
        search_news = copy.deepcopy(news)
        if (Staticsave.count_documents({"url":news["url"]})==0):
            if(Staticsave.count_documents({"title":search_news["title"]})==0):
                post_news_list.append(copy_news)
                y = Staticsave.insert_one(news)
                if news['category'] in type_map.keys():
                    mycol = Staticdb[type_map[news['category']]]
                    try:
                        mycol.insert_one(news)
                    except:
                        pass
                count = count+1
    post_news_dict = {}
    post_news_dict['news'] = post_news_list
    post_news_json = json.dumps(post_news_dict)
    headers = {'Connection': 'close'}
    try:
        res = requests.post(url=lucene_url, data=post_news_json,headers=headers)
        print("success post")
    except:
        pass
    print("not same:"+str(count))
    print("epoch end")

class DynamicThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        global global_count
        updatedNews = []
        rank = self.threadID
        tencent_channel = get_tencent_channel()
        sina_channel = get_sina_channel()
        wangyi_channel = get_wangyi_channel()
        sina_channel_keys = list(sina_channel.keys())
        wangyi_channel_keys = list(wangyi_channel.keys())
        if rank < len(tencent_channel):
            updatedNews = loadTencentNews(tencent_channel[rank])
        elif rank >= len(tencent_channel) and rank<(len(tencent_channel)+len(sina_channel_keys)):
            try:
                updatedNews = loadSinaNews(sina_channel_keys[rank-len(tencent_channel)])
            except:
                updatedNews = []
        elif rank == (len(tencent_channel)+len(sina_channel_keys)):
            updatedNews = loadSohuNews()
        else:
            updatedNews = loadWangyiNews(wangyi_channel_keys[rank-len(tencent_channel)-len(sina_channel_keys)-1])
        print(str(rank)+":"+str(len(updatedNews)))
        R.acquire()  # 加锁，保证同一时刻只有一个线程可以修改数据
        global_count = global_count + 1
        R.release()  # 修改完成就可以解锁
        self.updatedNews = copy.deepcopy(updatedNews)

    def get_result(self):
        try:
            return self.updatedNews
        except Exception:
            return None


global_count =0
if __name__ == "__main__":
    # 创建新线程
    while True:
        threads=[]
        thread_num = len(get_tencent_channel())+len(get_sina_channel())+1+len(get_wangyi_channel())
        for i in range(0,thread_num):
            tempThread = DynamicThread(i)
            tempThread.start()
            threads.append(tempThread)
        for tempThread in threads:
            tempThread.join()
        while True:
            if global_count == thread_num:
                global_count = 0
                break
            time.sleep(5)

        updateNews = []
        for i in range(0,thread_num):
            updateNews.extend(threads[i].get_result())
        hot_news = hot_news_scratch()
        print(len(updateNews)+len(hot_news))
        save_db(updateNews,hot_news)
        time.sleep(60)


