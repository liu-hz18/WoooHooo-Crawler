import requests
import demjson
from bs4 import BeautifulSoup
import json
from datetime import datetime

def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 30,allow_redirects=False)
        r.raise_for_status()
        return r.text
    except:
        return ""

def analyzeWangyiUrl(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select('div.post_main > h1')[0].text
    sourcetime = soup.select('div.post_info')[0].text
    sourcetime = sourcetime.strip()
    publish_time = sourcetime[0:19]
    source = sourcetime[20:]
    source = source.replace(" ","")
    source = source[0:-2]
    article = []  # 获取文章内容
    p = soup.select('div.post_body >p')
    for singleP in p:
        if singleP.text != "":
            article.append(singleP.text[2:])
    articleall = ''.join(article)
    articleall.strip()
    images = soup.select("div.post_body > p >img")
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


analyzeWangyiUrl("https://dy.163.com/article/FQC603B0055040N3.html?f=post2020_dy_recommends")