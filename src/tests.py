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
