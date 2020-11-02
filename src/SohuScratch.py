import requests
import demjson
from bs4 import BeautifulSoup
import json
from datetime import datetime

def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 30,allow_redirects=False)
        r.encoding = 'utf-8'
        r.raise_for_status()
        return r.text
    except:
        return ""

def analyzeSohuUrl(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    p = soup.select("article.article>p")
    timesource = soup.select("div.article-info > span")
    publish_time = timesource[0].text
    source = timesource[1].text[3:]
    title = p[0].text[4:]
    p.pop(0)
    p.pop(0)
    p.pop(-1)
    p.pop(-1)
    article = []  # 获取文章内容
    for singleP in p:
        if singleP.text!="":
            article.append(singleP.text)
    articleall = ''.join(article)
    images=soup.select("article.article> p >img")
    imagesurl = []
    for image in images:
        imagesurl.append(image.get('src'))
    top_imageurl = ""
    if len(imagesurl) != 0:
        top_imageurl = imagesurl[0]
    res_dict = {
        'url': url,
        'title': title,
        'publish_time': publish_time,
        'content': articleall,
        'category': "",
        'source': source,
        'imageurl': imagesurl,
        'top_img': top_imageurl
    }
    print(res_dict)
    return res_dict

analyzeSohuUrl("https://www.sohu.com/a/428821376_116237?spm=smpc.home.top-news2.4.1604285159855M0RnufR&_f=index_news_3")