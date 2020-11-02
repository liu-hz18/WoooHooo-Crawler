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

class NewsinaSpiderSpider(scrapy.Spider):
    name = 'newsina_spider'

    base_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page={}&r={}'

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

    def start_requests(self):
        #  可修改  这里设置爬取100页
        page_total = 100
        for page in range(1, page_total+1):
            #  按上面注释  可修改 这里"2509"代表"全部"类别的新闻
            lid = "2509"
            r = random.random()
            yield Request(self.base_url.format(lid, page, r), callback=self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        data_list = result.get('result').get('data')
        for data in data_list:
            item = NewsinaspiderItem()

            ctime = datetime.fromtimestamp(int(data.get('ctime')))
            ctime = datetime.strftime(ctime, '%Y-%m-%d %H:%M')

            item['ctime'] = ctime
            item['url'] = data.get('url')
            item['wapurl'] = data.get('wapurl')
            item['title'] = data.get('title')
            item['media_name'] = data.get('media_name')
            item['keywords'] = data.get('keywords')
            yield Request(url=item['url'], callback=self.parse_content, meta={'item': item})
