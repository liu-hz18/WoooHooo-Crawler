import requests
import demjson
from bs4 import BeautifulSoup
import json
from Scratchtest import *
import pymongo
import time
import random
from datetime import datetime

def loadTencentNews():
    #各种频道
    channels=['24hours','video','milite','cul','nstock','comic','house','emotion','digi','astro','health',
             'visit','baby','pet','history','politics','zfw','football','newssh','rushidao','edu','licai',
             'sports','life','kepu','ent','antip','bj','world','tech','finance','auto','fashion','games']
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
def handleTencentNewslist(urls):
    updatedNews=[]
    for url in urls:
        try:
            news=loadWithTime(url)
            updatedNews.append(news)
        except:
            continue
    return updatedNews

def getstandardHTMLText(url):
    try:
        r = requests.get(url, timeout = 30,allow_redirects=False)
        r.encoding = 'utf-8'
        r.raise_for_status()
        return r.text
    except:
        return ""

def analyzeSinaUrl(url):
    html = getstandardHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select('.main-title')[0].text
    publish_time = soup.select('.date-source span')[0].text
    publish_time = datetime.strptime(publish_time, '%Y年%m月%d日 %H:%M')
    publish_time.strftime('%Y-%m-%d')
    source =soup.select('.date-source span')[1].text  # 获取新闻来源
    images=soup.select("div.img_wrapper >img")
    imagesurl = []
    for image in images:
        imagesurl.append(image.get('src'))
    top_imageurl = ""
    if len(imagesurl)!=0:
        top_imageurl = imagesurl[0]
    article = []  # 获取文章内容
    for p in soup.select('div.article >p'):
        article.append(p.text[2:])
    articleall = ''.join(article)
    res_dict = {
        'url': url,
        'title': title,
        'publish_time': publish_time.__format__('%Y-%m-%d %H:%M:%S'),
        'content': articleall,
        'category': "",
        'source': "新浪"+source,
        'imageurl': imagesurl,
        'top_img': top_imageurl
    }
    return res_dict

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

def handleSinaNewslist(urls):
    updatedNews=[]
    for url in urls:
        try:
            news=analyzeSinaUrl(url)
            updatedNews.append(news)
            time.sleep(0.3)
        except:
            continue
    return updatedNews

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
        updatedNews = []
        if len(updatedurls)!=0:
            updatedNews.extend(handleTencentNewslist(updatedurls))
        if len(sinaUrl)!=0:
            updatedNews.extend(handleSinaNewslist(sinaUrl))
        print(updatedNews)
        #if len(updatedNews)!=0:
            #y = Staticsave.insert_many(newsSet.find())
            #newsSet.delete_many({})
            #x = newsSet.insert_many(updatedNews)
            #print(len(updatedNews))
        print("epoch end")
        time.sleep(120)



