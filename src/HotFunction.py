import requests
import json
import datetime
from bs4 import BeautifulSoup

def getHotDetail(hot_top):
    hot_news = []
    count = 0
    for news in hot_top:
        count = count + 1
        news_dict = {}
        news_dict['rank'] = count
        news_dict['title'] = news['title']
        news_dict['url'] = news['url']
        news_dict['publish_time'] = news['create_date'] +" "+ news['create_time']
        hot_news.append(news_dict)
    print(hot_news)
    print(len(hot_news))
    return hot_news


def getHotClick(todayDate):
    base_url = "http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=www_www_all_suda_suda&top_time={}&top_show_num=100&top_order=DESC&js_var=all_1_data01"
    Request = base_url.format(todayDate)
    response = requests.get(Request)
    response.encoding = 'utf-8'
    content = response.text
    result = eval(json.dumps(content).replace('var all_1_data01 = ', '').replace(';',''))
    hot_click = json.loads(result)['data']
    return hot_click

def getHotComment(todayDate):
    base_url = "http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=qbpdpl&top_time={}&top_show_num=100&top_order=DESC&js_var=comment_all_data"
    Request = base_url.format(todayDate)
    response = requests.get(Request)
    response.encoding = 'utf-8'
    content = response.text
    result = eval(json.dumps(content).replace('var comment_all_data = ', '').replace(';',''))
    hot_comment = json.loads(result)['data']
    return hot_comment

def getNowDate():
    nowDate = str(datetime.datetime.now())
    nowDate = nowDate.replace('-', '')[:8]
    return nowDate

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
    print(hot_search_list)
    print(len(hot_search_list))
    return hot_search_list