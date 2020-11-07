from .Scratchtest import getHTMLText,getstandardHTMLText,loadWithTime,analyzeSinaUrl,analyzeSohuUrl,analyzeWangyiUrl,getRandomUrl
import pytest
import requests

class TestScratch:
    def test_getHTMLText(self):
        url_base = "https://new.qq.com/rain/a/20201107A037ZB00"
        result = getHTMLText(url_base)
        r = requests.get(url_base, allow_redirects=False)
        assert result == r.text

    def test_getsatandardHTMLText(self):
        url_base = "https://new.qq.com/rain/a/20201107A037ZB00"
        result = getstandardHTMLText(url_base)
        r = requests.get(url_base, allow_redirects=False)
        r.encoding = 'utf-8'
        assert result == r.text

    def test_loadWithTime(self):
        url_base = "https://new.qq.com/omn/20201107/20201107A008E800.html"
        news = loadWithTime(url_base)
        assert 'url' in news.keys()
        assert 'title' in news.keys()
        assert 'publish_time' in news.keys()
        assert 'content' in news.keys()
        assert 'category' in news.keys()
        assert 'source' in news.keys()
        assert 'imageurl' in news.keys()
        assert 'top_img' in news.keys()

    def test_analyzeSinaUrl(self):
        url_base = "https://finance.sina.com.cn/china/gncj/2020-11-07/doc-iiznezxs0513551.shtml"
        news = analyzeSinaUrl(url_base)
        assert 'url' in news.keys()
        assert 'title' in news.keys()
        assert 'publish_time' in news.keys()
        assert 'content' in news.keys()
        assert 'category' in news.keys()
        assert 'source' in news.keys()
        assert 'imageurl' in news.keys()
        assert 'top_img' in news.keys()

    def test_analyzeSohuUrl(self):
        url_base = "https://www.sohu.com/a/430176139_260616?spm=smpc.news-home.top-news3.2.1604735248153x1lIxBL&_f=index_chan08news_6"
        news = analyzeSohuUrl(url_base)
        assert 'url' in news.keys()
        assert 'title' in news.keys()
        assert 'publish_time' in news.keys()
        assert 'content' in news.keys()
        assert 'category' in news.keys()
        assert 'source' in news.keys()
        assert 'imageurl' in news.keys()
        assert 'top_img' in news.keys()

    def test_analyzeWangyiUrl(self):
        url_base = "https://dy.163.com/article/FQQQSHBC051481US.html?clickfrom=w_yw"
        news = analyzeWangyiUrl(url_base)
        assert 'url' in news.keys()
        assert 'title' in news.keys()
        assert 'publish_time' in news.keys()
        assert 'content' in news.keys()
        assert 'category' in news.keys()
        assert 'source' in news.keys()
        assert 'imageurl' in news.keys()
        assert 'top_img' in news.keys()

    def test_getRandomUrl(self):
        num = len(getRandomUrl())
        assert  num == 36**4


