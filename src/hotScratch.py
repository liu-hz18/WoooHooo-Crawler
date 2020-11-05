from bs4 import BeautifulSoup
import pymongo
import requests
import json

def getHotClick():
    todayDate = "20201105"
    base_url = "http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=www_www_all_suda_suda&top_time={}&top_show_num=100&top_order=DESC&js_var=all_1_data01"
    Request = base_url.format(todayDate)
    response = requests.get(Request)
    response.encoding = 'utf-8'
    content = response.text
    result = eval(json.dumps(content).replace('var all_1_data01 = ', '').replace(';',''))
    hot_click = json.loads(result)['data']
    print(hot_click)
    hot_news = []
    count = 0
    for news in hot_click:
        count = count +1
        news_dict = {}
        news_dict['rank'] = count
        news_dict['title'] = news['title']
        news_dict['url'] = news['url']
        news_dict['publish_time'] = news['create_date'] + news['create_time']
        hot_news.append(news_dict)
    print(hot_news)
    print(len(hot_news))

if __name__ == "__main__":
    getHotClick()