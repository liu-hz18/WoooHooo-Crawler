import requests
from bs4 import BeautifulSoup
import time
import pymongo

def getHotSearch():
    base_url = "http://top.baidu.com/buzz?b=2"
    response = requests.get(base_url)
    response.raise_for_status()
    response.encoding = 'gbk'
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    title = soup.select("table.list-table >  tr > td.keyword > a.list-title")
    title_list = []
    for index in title:
        title_list.append(index.text)
    hot_value = soup.select("table.list-table >  tr > td.last > span")
    hot_value_list = []
    for index in hot_value:
        hot_value_list.append(index.text)
    hot_search_list = []
    for i in range(0,len(title_list)):
        hot_dict = {}
        hot_dict['title'] = title_list[i]
        hot_dict['value'] = hot_value_list[i]
        hot_search_list.append(hot_dict)
    return hot_search_list

if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost:30001/")
    Staticdb = myclient["NewsCopy"]
    hot_search_save = Staticdb["hot_search"]
    while True:
        hot_search = getHotSearch()
        delete_x = hot_search_save.delete_many({})
        save_x = hot_search_save.insert_many(hot_search)
        print(hot_search)
        print(len(hot_search))
        time.sleep(900)