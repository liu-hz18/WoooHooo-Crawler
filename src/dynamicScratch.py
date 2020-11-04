import requests
import demjson
import json
from Scratchtest import *
from bs4 import BeautifulSoup
import pymongo
import time
import random

#模拟访问腾讯新闻各个首页
def loadTencentNews():
    #各种频道
    channels = ['24hours', 'video', 'milite', 'cul', 'nstock', 'comic', 'house', 'emotion', 'digi', 'astro', 'health',
                'visit', 'baby', 'pet', 'history', 'politics', 'zfw', 'football', 'newssh', 'rushidao', 'edu', 'licai',
                'sports', 'life', 'kepu', 'ent', 'antip', 'bj', 'world', 'tech', 'finance', 'auto', 'fashion', 'games']
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
    for url in urls:
        if type == 0:
            try:
                news = loadWithTime(url)
                updatedNews.append(news)
            except:
                continue
        elif type == 1:
            try:
                news = analyzeSinaUrl(url)
                updatedNews.append(news)
                time.sleep(0.1)
            except:
                continue
        elif type == 2:
            try:
                news = analyzeSohuUrl(url)
                updatedNews.append(news)
                time.sleep(0.1)
            except:
                continue
        elif type ==3:
            try:
                news = analyzeWangyiUrl(url)
                updatedNews.append(news)
                time.sleep(0.1)
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
    base_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page={}&r={}'
    url_list = []
    for page in range(1, page_total+1):
        #  按上面注释  可修改 这里"2509"代表"全部"类别的新闻
        lid = "2509"
        r = random.random()
        Request=base_url.format(lid, page, r)
        response = requests.get(Request)
        result = json.loads(response.text)
        data_list = result.get('result').get('data')
        for news in data_list:
            url_list.append(news['url'])
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
    base_url = 'https://temp.163.com/special/00804KVA/cm_yaowen20200213_0{}.js?callback=data_callback'
    url_list = []
    page = 2
    for i in range(2,page+1):
        url = base_url.format(i)
        response = requests.get(url)
        content = response.text
        result = eval(eval((json.dumps(content)).replace('data_callback(','').replace(')','').replace(' ','')))
        for news in result:
            url_list.append(news["docurl"])
    return url_list


if __name__ == "__main__":
    #myclient = pymongo.MongoClient("mongodb://localhost/")
    #mydb = myclient["DynamicNews"]
    #newsSet=mydb["news"]
    totalurls=[]
    #Staticdb=myclient["StaticNews"]
    #Staticsave=Staticdb["news"]
    while True:
        updatedurls = loadTencentNews()
        sinaUrl = loadSinaNewsList()
        sohuUrl = loadSohuNewsList()
        wangyiUrl = loadWangyiNewsList()
        #腾讯新闻去重
        for url in updatedurls:
            if url in totalurls:
                updatedurls.remove(url)
            else:
                totalurls.append(url)

        #新浪新闻去重
        for url in sinaUrl:
            if url in totalurls:
                sinaUrl.remove(url)
            else:
                totalurls.append(url)
        #搜狐新闻去重
        for url in sohuUrl:
            if url in totalurls:
                sohuUrl.remove(url)
            else:
                totalurls.append(url)
        #网易新闻去重
        for url in wangyiUrl:
            if url in totalurls:
                wangyiUrl.remove(url)
            else:
                totalurls.append(url)

        updatedNews = []
        if len(updatedurls)!=0:
            updatedNews.extend(handleNewslist(0,updatedurls))
        if len(sinaUrl)!=0:
            updatedNews.extend(handleNewslist(1,sinaUrl))
        if len(sohuUrl)!=0:
            updatedNews.extend(handleNewslist(2,sohuUrl))
        if len(wangyiUrl)!=0:
            updatedNews.extend(handleNewslist(3,wangyiUrl))
        print(updatedNews)
        #if len(updatedNews)!=0:
            #y = Staticsave.insert_many(newsSet.find())
            #newsSet.delete_many({})
            #x = newsSet.insert_many(updatedNews)
            #print(len(updatedNews))
        print("epoch end")
        time.sleep(60)



