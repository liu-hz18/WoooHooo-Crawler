import random
import requests
import json
import time
from bs4 import BeautifulSoup
from Scratchtest import loadWithTime,load_tencent_with_a,analyzeSinaUrl,analyzeWangyiUrl,analyzeSohuUrl,getHTMLText,getstandardHTMLText,handleNewslist
import demjson

def get_tencent_channel():
    #腾讯新闻的各种频道
    return ['24hours', 'milite', 'cul', 'nstock', 'digi', 'history', 'politics',
             'newssh', 'edu', 'sports', 'kepu', 'ent', 'world', 'tech', 'finance', 'games']

def get_sina_channel():
    return {
        "2510": "politics",  # 时政
        "2669": "social",  # 社会
        "2511": "chuguo",  # 国际
        "2514": "mil",  # 军事
        "2516": "finance",  # 财经
        "2518": "finance",
        "2517": "finance",
        "2513": "ent",  # 娱乐
        "2512": "sports",  # 体育
        "2515": "science",  # 科技
    }
    #     "2509": "全部",
    #     "2510": "国内",
    #     "2511": "国际",
    #     "2669": "社会",
    #     "2512": "体育",
    #     "2513": "娱乐",
    #     "2514": "军事",
    #     "2515": "科技",
    #     "2516": "财经",
    #     "2517": "股市",
    #     "2518": "美股",
    #     "2968": "国内_国际",
    #     "2970": "国内_社会",
    #     "2972": "国际_社会",
    #     "2974": "国内国际社会"
def get_wangyi_channel():
    return {
        "guonei": "politics",  # 时政
        "guoji": "chuguo",  # 国际
        "war": "mil",  # 军事
    }

#模拟访问腾讯新闻各个首页
def loadTencentNews(channel):
    baseurls = " https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?"
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
        'limit': 20,
        'strategy': 1,
        'ext': "{\"pool\":[\"top\"], \"is_filter\":10, \"check_type\":true}",
    }
    urls=[]
    if channel == "politics":
        response = requests.get("https://i.news.qq.com/trpc.qqnews_web.pc_base_srv.base_http_proxy/OpenApiSiteList?site=news_news_msh")
        news_list = demjson.decode(response.content)["data"][0:20]
        for news in news_list:
            urls.append(news['url'])
    else:
        try:
            params['sub_srv_id']=channel
            response = requests.get(baseurls,headers=headers ,params=params)
            news_list = demjson.decode(response.content)["data"]["list"]
            for news in news_list:
                urls.append(news['url'])
        except:
            pass
    tencent_news_list = list(set(urls))
    tencent_news = handleNewslist(0, tencent_news_list)
    return tencent_news

#模拟访问新浪新闻滚动新闻页面
def loadSinaNews(channel):
    page_total = 1
    sleep_time = random.randint(0,9)
    time.sleep(sleep_time)
    base_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page={}&r={}'
    url_list = []
    classify_map = get_sina_channel()
    for page in range(1, page_total+1):
        r = random.random()
        Request = base_url.format(channel, page, r)
        response = requests.get(Request)
        result = json.loads(response.text)
        data_list = result.get('result').get('data')
        for news in data_list:
            url_dict = {}
            url_dict['url'] = news['url']
            url_dict['type'] = classify_map[channel]
            url_list.append(url_dict)
    sina_news = handleNewslist(1, url_list)
    return sina_news


#analyzeSohuUrl("https://www.sohu.com")
def loadSohuNews():
    base_url="https://www.sohu.com/"
    html = getstandardHTMLText(base_url)
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    partyNews = soup.select("div.news > p > a")
    for News in partyNews:
        urls.append(News.get("href"))
    topNews = soup.select("div.list16 > ul > li > a")
    for News in topNews:
        urls.append(News.get("href"))
    sohu_news = handleNewslist(2, urls)
    return sohu_news

#得到网易新闻列表中url
def loadWangyiNews(channel):
    base_url = 'https://temp.163.com/special/00804KVA/cm_{}.js?callback=data_callback'
    classify_map = get_wangyi_channel()
    url_list = []
    url = base_url.format(channel)
    response = requests.get(url)
    content = response.text
    result = eval(eval((json.dumps(content)).replace('data_callback(','').replace(')','').replace(' ','')))
    for news in result:
        url_dict = {}
        url_dict['url'] = news["docurl"]
        url_dict['type'] = classify_map[channel]
        url_list.append(url_dict)
    wangyi_news = handleNewslist(3, url_list)
    return wangyi_news

def getTypeMap():
    return {
        "politics": "politics",  # 时政
        "history": "history",  # 文化
        "social": "social",  # 社会
        "cul": "social",
        "chuguo": "chuguo",
        "world": "chuguo",  # 国际
        "mil": "mil",  # 军事
        "finance": "finance",  # 财经
        "ent": "ent",  # 娱乐
        "travel": "ent",
        "comic": "ent",
        "sports": "sports",  # 体育
        "science": "science",  # 科技
        "digi": "science",
        "digital": "science",
        "tech": "science",
        "game": "game",  # 游戏
    }

def getClassifyMap():
    return {
        "politics":"politics",#国内
        "history":"history",#文化
        "social":"social",#社会
        "cul":"social",
        "chuguo":"chuguo",
        "world":"chuguo",#国际
        "mil":"mil",#军事
        "finance":"finance",#财经
        "ent":"ent",#娱乐
        "travel":"ent",
        "sports":"sports",#体育
        "science":"science",#科技
        "digi":"science",
        "digital":"science",
        "tech":"science",
        "game":"game",#游戏
    }


