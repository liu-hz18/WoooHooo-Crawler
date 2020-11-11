import requests
import json
import datetime
import demjson
import random
from bs4 import BeautifulSoup
from Scratchtest import handleNewslist

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

def hot_news_scratch():
    #爬取腾讯热点新闻
    tencent_base_url = " https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?"
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin': 'https://news.qq.com',
        'referer': 'https://news.qq.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    }
    params = {
        'sub_srv_id': '24hours',
        'srv_id': 'pc',
        'offset': 0,
        'limit': 199,
        'strategy': 1,
        'ext': "{\"pool\":[\"top\"], \"is_filter\":7, \"check_type\":true}",
    }
    tencent_hot_url_list = []
    response = requests.get(tencent_base_url, params=params, headers=headers)
    news_list = demjson.decode(response.content)["data"]["list"]
    for news in news_list:
        tencent_hot_url_list.append(news['url'])
    hot_news_list = handleNewslist(0,tencent_hot_url_list)
    #爬取新浪热点新闻
    sina_base_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page={}&r={}'
    sina_hot_url_list = []
    r = random.random()
    hot_request = sina_base_url.format("2509", 1, r)
    hot_response = requests.get(hot_request)
    hot_result = json.loads(hot_response.text)
    hot_data_list = hot_result.get('result').get('data')
    for news in hot_data_list:
        url_dict = {}
        url_dict['url'] = news['url']
        url_dict['type'] = ''
        sina_hot_url_list.append(url_dict)
    hot_news_list.extend(handleNewslist(1,sina_hot_url_list))
    #print(hot_news_list)
    print(len(hot_news_list))
    return hot_news_list


