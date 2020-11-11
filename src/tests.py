import pytest
import requests
from .Scratchtest import getHTMLText,getstandardHTMLText,loadWithTime,load_tencent_with_a,analyzeSinaUrl,analyzeSohuUrl,analyzeWangyiUrl,getRandomUrl,handleNewslist
from .HotFunction import getHotSearch,getHotDetail,getHotClick,getHotComment,getNowDate,hot_news_scratch
from .DynamicFunction import getTypeMap,getClassifyMap,get_tencent_channel,get_sina_channel,get_wangyi_channel,loadTencentNews,loadSinaNews,loadSohuNews,loadWangyiNews
from .dynamicScratch import save_db,DynamicThread

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

    def test_load_tencent_with_a(self):
        url_base = "https://new.qq.com/rain/a/20201107A037ZB00"
        news = load_tencent_with_a(url_base)
        assert 'url' in news.keys()
        assert 'title' in news.keys()
        assert 'publish_time' in news.keys()
        assert 'content' in news.keys()
        assert 'category' in news.keys()
        assert 'source' in news.keys()
        assert 'imageurl' in news.keys()
        assert 'top_img' in news.keys()

    def test_analyzeSinaUrl(self):
        url_dict = {}
        url_dict['url'] =  "https://finance.sina.com.cn/china/gncj/2020-11-07/doc-iiznezxs0513551.shtml"
        url_dict['type'] = 'politics'
        news = analyzeSinaUrl(url_dict)
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
        url_dict = {}
        url_dict['url'] = "https://dy.163.com/article/FQQQSHBC051481US.html?clickfrom=w_yw"
        url_dict['type'] = 'politics'
        news = analyzeWangyiUrl(url_dict)
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

    def test_getHotSearch(self):
        hot_search_list = getHotSearch()
        for news in hot_search_list:
            assert 'title' in news.keys()
            assert 'value' in news.keys()

    def test_getHotClick(self):
        nowDate = getNowDate()
        hot_click = getHotClick(nowDate)
        assert len(hot_click) > 0

    def test_getHotDetail(self):
        nowDate = getNowDate()
        hot_comment = getHotComment(nowDate)
        hot_comment_news = getHotDetail(hot_comment)[0:10]
        for index in hot_comment_news:
            assert 'rank' in index.keys()
            assert 'title' in index.keys()
            assert 'publish_time' in index.keys()
            assert 'url' in index.keys()

    def test_hot_news_scratch(self):
        hot_news_list = hot_news_scratch()
        assert len(hot_news_list)>0

    def test_getTypeMap(self):
        type_map = getTypeMap()
        assert isinstance(type_map,dict)

    def test_getClassifyMap(self):
        classify_map = getClassifyMap()
        assert isinstance(classify_map,dict)

    def test_get_tencent_channel(self):
        tencent_channel = get_tencent_channel()
        assert len(tencent_channel) > 0

    def test_get_sina_channel(self):
        sina_channel = get_sina_channel()
        assert len(sina_channel)>0

    def test_get_wangyi_channel(self):
        wangyi_channel = get_wangyi_channel()
        assert len(wangyi_channel)

    def test_loadTencentNews(self):
        tencent_news = loadTencentNews('24hours')
        assert len(tencent_news) > 0

    def test_loadSinaNews(self):
        sina_news = loadSinaNews("2510")
        assert len(sina_news) > 0

    def test_loadSohuNews(self):
        Sohu_news = loadSohuNews()
        assert len(Sohu_news) > 0

    def test_loadWangyiNews(self):
        wangyi_news = loadWangyiNews("guonei")
        assert len(wangyi_news) > 0