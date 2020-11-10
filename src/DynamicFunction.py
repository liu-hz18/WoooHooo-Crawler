import random
import requests
import json
import time
from bs4 import BeautifulSoup
from Scratchtest import loadWithTime,load_tencent_with_a,analyzeSinaUrl,analyzeWangyiUrl,analyzeSohuUrl,getHTMLText,getstandardHTMLText
import demjson

#模拟访问腾讯新闻各个首页
def loadTencentNews():
    #各种频道
    channels = ['24hours', 'milite', 'cul', 'nstock','digi','history', 'politics',
                'zfw','newssh', 'edu','sports', 'kepu', 'ent',  'world', 'tech', 'finance', 'games']
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
        'sub_srv_id': 'video',
        'srv_id': 'pc',
        'offset': 0,
        'limit': 10,
        'strategy': 1,
        'ext': "{\"pool\":[\"top\"], \"is_filter\":10, \"check_type\":true}",
    }
    urls=[]
    for index in channels:
        try:
            params['sub_srv_id']=index
            response = requests.get(baseurls, params=params, headers=headers)
            news_list = demjson.decode(response.content)["data"]["list"]
            for news in news_list:
                urls.append(news['url'])
        except:
            continue
    return list(set(urls))

#处理热点新闻列表
def handleNewslist(type,urls):
    updatedNews=[]
    #print(len(urls))
    for url in urls:
        #print(url)
        if type == 0:
            try:
                try:
                    news = loadWithTime(url)
                except:
                    format_url = "https://new.qq.com/rain/a/"+url[32:-5]
                    news = load_tencent_with_a(format_url)
                updatedNews.append(news)
                #print(news)
            except:
                continue
        elif type == 1:
            try:
                news = analyzeSinaUrl(url)
                updatedNews.append(news)
                #print(news)
            except:
                continue
        elif type == 2:
            try:
                news = analyzeSohuUrl(url)
                updatedNews.append(news)
            except:
                continue
        elif type ==3:
            try:
                news = analyzeWangyiUrl(url)
                updatedNews.append(news)
            except:
                continue
    return updatedNews

#模拟访问新浪新闻滚动新闻页面
def loadSinaNewsList():
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
    #  可修改  这里设置爬取100页
    page_total = 1
    classify_map = {
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
    base_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page={}&r={}'
    url_list = []
    for lid in classify_map.keys():
        for page in range(1, page_total+1):
            r = random.random()
            Request=base_url.format(lid, page, r)
            response = requests.get(Request)
            result = json.loads(response.text)
            data_list = result.get('result').get('data')
            for news in data_list:
                url_dict = {}
                url_dict['url'] = news['url']
                url_dict['type'] = classify_map[lid]
                url_list.append(url_dict)
    #print(url_list)
    return url_list

#analyzeSohuUrl("https://www.sohu.com")
def loadSohuNewsList():
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
    return urls

#得到网易新闻列表中url
def loadWangyiNewsList():
    base_url = 'https://temp.163.com/special/00804KVA/cm_{}.js?callback=data_callback'
    classify_map = {
        "guonei": "politics",  # 时政
        "guoji": "chuguo",  # 国际
        "war": "mil",  # 军事
    }
    url_list = []
    for classify in classify_map.keys():
        url = base_url.format(classify)
        response = requests.get(url)
        content = response.text
        result = eval(eval((json.dumps(content)).replace('data_callback(','').replace(')','').replace(' ','')))
        for news in result:
            url_dict = {}
            url_dict['url'] = news["docurl"]
            url_dict['type'] = classify_map[classify]
            url_list.append(url_dict)
    return url_list

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

def getUpdatedNews(updatedurls,sinaUrl,sohuUrl,wangyiUrl):
    updatedNews = []
    if len(updatedurls) != 0:
        updatedNews.extend(handleNewslist(0, updatedurls))
    print("tencent end")
    if len(sinaUrl) != 0:
        updatedNews.extend(handleNewslist(1, sinaUrl))
    print("sina end")
    if len(sohuUrl) != 0:
        updatedNews.extend(handleNewslist(2, sohuUrl))
    print("souhu end")
    if len(wangyiUrl) != 0:
        updatedNews.extend(handleNewslist(3, wangyiUrl))
    print("wangyi end")
    print("total:" + str(len(updatedNews)))
    return updatedNews

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



