from django.db import models
from django.forms import ModelForm

class News(models.Model):
    #标题
    title = models.CharField(unique=True, max_length=100)
    #发表时间
    publish_time = models.TextField()
    #具体内容
    content = models.TextField()
    #链接
    url = models.TextField()
    #来源
    source = models.TextField()
    #分类
    category=models.TextField()
    #图片链接
    top_img=models.TextField()


    def __str__(self):
        return self.title