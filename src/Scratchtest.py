import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time

html_parser = "html.parser"
#得到html文本
def get_html_text(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.text
    except Exception:
        return ""

#得到HTML文本
def get_standard_html_text(url):
    try:
        r = requests.get(url, timeout = 30,allow_redirects=False)
        r.encoding = 'utf-8'
        r.raise_for_status()
        return r.text
    except Exception:
        return ""

#for links like http://new.qq.com/omn/time/newsID.html
def load_with_time(url):
    html = get_html_text(url)
    soup = BeautifulSoup(html, html_parser)
    title = soup.select("div.LEFT > h1")
    paras = soup.select("div.content-article > p.one-p")
    textcontent = ""
    for para in paras:
        if len(para) > 0:
            textcontent += para.get_text().replace('\n'," ")
    # 将爬取到的文章用字典格式来存
    temp = json.loads((soup.select('script')[5]).contents[0].split("=")[-1])
    time=temp["pubtime"]
    catalog=temp["catalog1"]
    source=temp['media']
    images = soup.select("div.content-article >p.one-p> img.content-picture")
    imagesurl = []
    for index in images:
        imagesurl.append(index.get('src'))
    top_image=""
    if len(images)!=0:
        top_image=images[0].get('src')
    article = {
        'url':url,
        'title': title[0].get_text(),
        'publish_time': time,
        'content': textcontent,
        'category': catalog,
        'source':"腾讯："+source,
        'imageurl':imagesurl,
        'top_img':top_image
    }
    return article

#解析rain/a形式的腾讯新闻
def load_tencent_with_a(url):
    html = get_html_text(url)
    soup = BeautifulSoup(html, html_parser)
    title = soup.select("div.LEFT > h1")[0].text
    temp = json.loads(soup.findAll('script')[5].contents[0].split("=")[-1])
    publish_time = temp['pubtime']
    source = temp['media']
    category = temp['catalog1']
    paragragh = soup.select("div.content-article > p.one-p")
    textcontent = ""
    for p in paragragh:
        if len(p) > 0:
            textcontent += p.get_text().replace('\n', " ")
    images = soup.select("div.content-article >p.one-p> img.content-picture")
    images_url = []
    for index in images:
        images_url.append(index.get('src'))
    top_image = ""
    if len(images) != 0:
        top_image = images[0].get('src')
    article = {
        'url': url,
        'title': title,
        'publish_time': publish_time,
        'content': textcontent,
        'category': category,
        'source': "腾讯：" + source,
        'imageurl': images_url,
        'top_img': top_image
    }
    #print(article)
    return article

#解析新浪新闻
def analyze_sina_url(url_dict):
    url = url_dict['url']
    html = get_standard_html_text(url)
    soup = BeautifulSoup(html, html_parser)
    title = soup.select('h1.main-title')[0].text
    publish_time = soup.select('div.date-source span')[0].text
    publish_time = datetime.strptime(publish_time, '%Y年%m月%d日 %H:%M')
    publish_time.strftime('%Y-%m-%d')
    try:
        source ="新浪：" + soup.select('div.date-source >a')[0].text  # 获取新闻来源
    except Exception:
        source = "新浪"
    images=soup.select("div.img_wrapper >img")
    imagesurl = []
    for image in images:
        imagesurl.append(image.get('src'))
    top_imageurl = ""
    if len(imagesurl)!=0:
        top_imageurl = imagesurl[0]
    article = []  # 获取文章内容
    if len(soup.select('div.article > p'))==0:
        raise Exception
    for p in soup.select('div.article > p'):
        article.append(p.text[2:])
    articleall = ''.join(article)
    res_dict = {
        'url': url,
        'title': title,
        'publish_time': publish_time.__format__('%Y-%m-%d %H:%M:%S'),
        'content': articleall,
        'category': url_dict['type'],
        'source': source,
        'imageurl': imagesurl,
        'top_img': top_imageurl
    }
    return res_dict

#解析搜狐新闻详情页
def analyze_sohu_url(url):
    html = get_standard_html_text(url)
    soup = BeautifulSoup(html, html_parser)
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
    for single_p in p:
        if single_p.text!="":
            article.append(single_p.text)
    article_all = ''.join(article)
    images=soup.select("article.article> p >img")
    imagesurl = []
    for image in images:
        imagesurl.append(image.get('src')[5:])
    top_imageurl = ""
    if len(imagesurl) != 0:
        top_imageurl = imagesurl[0]
    res_dict = {
        'url': url,
        'title': title,
        'publish_time': publish_time,
        'content': article_all,
        'category': "",
        'source': "搜狐："+source,
        'imageurl': imagesurl,
        'top_img': top_imageurl
    }
    return res_dict

#解析网易新闻
def analyze_wangyi_url(url_dict):
    url = url_dict['url']
    html = get_html_text(url)
    soup = BeautifulSoup(html, html_parser)
    title = soup.select('div.post_main > h1')[0].text
    sourcetime = soup.select('div.post_info')[0].text
    sourcetime = sourcetime.strip()
    publish_time = sourcetime[0:19]
    source = sourcetime[20:]
    source = source.replace(" ","")
    source = source[0:-2]
    article = []  # 获取文章内容
    p = soup.select('div.post_body >p')
    for single_p in p:
        if single_p.text != "":
            article.append(single_p.text[2:])
    article_all = ''.join(article)
    article_all.strip()
    images = soup.select("div.post_body > p >img")
    imagesurl = []
    for image in images:
        imagesurl.append(image.get('src')[6:])
    top_imageurl = ""
    if len(imagesurl) != 0:
        top_imageurl = imagesurl[0]
    res_dict = {
        'url': url,
        'title': title,
        'publish_time': publish_time,
        'content': article_all,
        'category': url_dict['type'],
        'source': "网易："+source,
        'imageurl': imagesurl,
        'top_img': top_imageurl
    }
    return res_dict

#得到四位随机数序列的所有组合形式
def get_random_url():
    element_list=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J',
                 'K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    random_list=[]
    for i in element_list:
        for j in element_list:
            for k in element_list:
                for l in element_list:
                    temp=i+j+k+l
                    random_list.append(temp)
    return random_list

def handle_news_list(type,urls):
    updated_news=[]
    for url in urls:
        if type == 0:
            try:
                try:
                    news = load_with_time(url)
                except Exception:
                    format_url = "https://new.qq.com/rain/a/"+url[32:-5]
                    news = load_tencent_with_a(format_url)
                updated_news.append(news)
            except Exception:
                continue
        elif type == 1:
            try:
                news = analyze_sina_url(url)
                updated_news.append(news)
                time.sleep(0.2)
            except Exception:
                continue
        elif type == 2:
            try:
                news = analyze_sohu_url(url)
                updated_news.append(news)
            except Exception:
                continue
        elif type ==3:
            try:
                news = analyze_wangyi_url(url)
                updated_news.append(news)
            except Exception:
                continue
    return updated_news
