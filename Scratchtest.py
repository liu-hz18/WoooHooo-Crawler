import requests
import demjson
from bs4 import BeautifulSoup
import json

def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 30,allow_redirects=False)
        r.raise_for_status()
        return r.text
    except:
        return ""

# for links like https://news.qq.com/a/time/newsID.htm
def getContentwithA(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select("div.hd > h1")
    time = soup.select("div.a_Info > span.a_time")
    paras = soup.select("div.Cnt-Main-Article-QQ > p.text")
    textcontent=""
    for para in paras:
        if len(para) > 0:
            textcontent+=para.get_text()
    temp = soup.find('script', {'type': 'text/javascript'}).contents[0].replace("\n", "").split("||")[-1]
    keywords=demjson.decode(temp.replace("\'", "\""))["tags"]
    #将爬取到的文章用字典格式来存
    article = {
        'Title' : title[0].get_text(),
        'Time' : time[0].get_text(),
        'Paragraph' : textcontent,
        'keywords':keywords,
        'catalog1':"unknown",
        'catalog2':"unknown"
    }
    print(article)

#for links like http://new.qq.com/omn/time/newsID.html
def getContentWithTime(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    paras = soup.select("div.content-article > p.one-p")
    images=soup.select("div.content-article >p.one-p> img.content-picture")
    imagesurl=[]
    for index in images:
        imagesurl.append(index.get('src'))
    textcontent = ""

    for para in paras:
        if len(para) > 0:
            textcontent += para.get_text().replace('\n',"")
    return textcontent,imagesurl

#处理热点新闻列表
def handleNewslist(news_list):
    news_save=[]
    for news in news_list:
        news_dict = dict()
        try:
            content,images=getContentWithTime(news['url'])
            if content=="":
                continue
            news_dict['content']=content
            news_dict['imageurl']=images
            news_save.append(news_dict)
        except:
            continue
        news_dict['title']=news['title']
        news_dict['url']=news['url']
        news_dict['category']=news['category_cn']
        news_dict['tags']=news['tags']
        news_dict['source']=news['media_name']
        news_dict['publish_time']=news['publish_time']
        news_dict['top_img']=news['img']
    return news_save
#加载每天的热点新闻
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
        'limit': 199,
        'strategy': 1,
        'ext': "{\"pool\":[\"top\"], \"is_filter\":10, \"check_type\":true}",
    }
    news_save=[]
    for index in channels:
        try:
            params['sub_srv_id']=index
            response = requests.get(baseurls, params=params, headers=headers)
            news_list = demjson.decode(response.content)["data"]["list"]
            temp_news_save=handleNewslist(news_list)
            print(temp_news_save)
            news_save+=temp_news_save
        except:
            continue
        print(len(news_save))
    with open("1.json", 'w', encoding='utf-8') as json_file:
        json.dump(news_save, json_file, ensure_ascii=False)


#for links like http://new.qq.com/omn/time/newsID.html
def loadWithTime(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select("div.LEFT > h1")
    paras = soup.select("div.content-article > p.one-p")
    textcontent = ""
    for para in paras:
        if len(para) > 0:
            textcontent += para.get_text().replace('\n'," ")
    # 将爬取到的文章用字典格式来存
    temp = json.loads((soup.findAll('script')[5]).contents[0].split("=")[-1])
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
        'source':source,
        'imageurl':imagesurl,
        'top_img':top_image
    }
    return article

#得到四位随机数序列的所有组合形式
def getRandomUrl():
    elementList=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J',
                 'K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    randomList=[]
    for i in elementList:
        for j in elementList:
            for k in elementList:
                for l in elementList:
                    temp=i+j+k+l
                    randomList.append(temp)
    return randomList


