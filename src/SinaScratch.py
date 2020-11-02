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

def analyzeSinaUrl(url):
    html = getHTMLText(url)
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
        'source': source,
        'imageurl': imagesurl,
        'top_img': top_imageurl
    }
    print(res_dict)
    return res_dict

analyzeSinaUrl("https://finance.sina.com.cn/stock/hkstock/ggscyd/2020-11-01/doc-iiznctkc8925536.shtml")