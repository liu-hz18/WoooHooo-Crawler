from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from .models import News
import json

def newssave(request):
    def gen_response(code: int, data: str):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    #Get用来获取存取得新闻
    if request.method == 'GET':
        return gen_response(200, [{
                'title': news.title,
                'content': news.content,
                'publish_time': news.publish_time,
                'url': news.url,
                'source':news.source,
                'category':news.category,
                'top_img':news.top_img,
            }
            for news in News.objects.all()
        ])
    #用Post来完成新闻从爬虫的上传
    elif request.method == 'POST':
        try:
            newsData = json.loads(request.body.decode())
        except:
            return gen_response(400, "not a json")
        for index in newsData:
            title = index.get('title')
            content = index.get('content')
            publish_time=index.get('publish_time')
            url=index.get('url')
            source=index.get('source')
            category=index.get('category')
            top_img = index.get('top_img')
            try:
                news = News(title=title, url=url, publish_time=publish_time,content=content,source=source,category=category,top_img=top_img)
                news.full_clean()
                news.save()
            except:
                continue
        return gen_response(201, "news was sent successfully")

