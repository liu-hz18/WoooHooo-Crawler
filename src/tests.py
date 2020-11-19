import pytest
import requests
from .Scratchtest import get_html_text,get_standard_html_text,load_with_time,load_tencent_with_a,analyze_sina_url,analyze_sohu_url,analyze_wangyi_url,get_random_url,handle_news_list
from .HotFunction import get_hot_search,get_hot_detail,get_hot_click,get_hot_comment,get_now_date,hot_news_scratch
from .DynamicFunction import get_type_map,get_classify_map,get_tencent_channel,get_sina_channel,get_wangyi_channel,load_tencent_news,load_sina_news,load_sohu_news,load_wangyi_news
from .dynamicScratch import DynamicThread

class TestScratch:
    def test_dynamic_thread(self):
        thread_num = [0,1,2]
        threads = []
        for i in thread_num:
            temp_thread = DynamicThread(i)
            temp_thread.start()
            threads.append(temp_thread)
        for temp_thread in threads:
            temp_thread.join()

    def test_get_html_text(self):
        url_base = "https://new.qq.com/rain/a/20201115A0BGJQ00"
        result = get_html_text(url_base)
        r = requests.get(url_base, allow_redirects=False)
        assert result == r.text

    def test_get_standard_html_text(self):
        url_base = "https://finance.sina.com.cn/roll/2020-11-16/doc-iiznctke1777176.shtml"
        result = get_standard_html_text(url_base)
        r = requests.get(url_base, allow_redirects=False)
        r.encoding = 'utf-8'
        assert result == r.text

    def test_load_with_time(self):
        url_base = "https://new.qq.com/omn/20201107/20201107A008E800.html"
        news = load_with_time(url_base)
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

    def test_analyze_sina_url(self):
        url_dict = {}
        url_dict['url'] =  "https://finance.sina.com.cn/china/gncj/2020-11-07/doc-iiznezxs0513551.shtml"
        url_dict['type'] = 'politics'
        news = analyze_sina_url(url_dict)
        assert 'url' in news.keys()
        assert 'title' in news.keys()
        assert 'publish_time' in news.keys()
        assert 'content' in news.keys()
        assert 'category' in news.keys()
        assert 'source' in news.keys()
        assert 'imageurl' in news.keys()
        assert 'top_img' in news.keys()

    def test_analyze_sohu_url(self):
        url_base = "https://www.sohu.com/a/430176139_260616?spm=smpc.news-home.top-news3.2.1604735248153x1lIxBL&_f=index_chan08news_6"
        news = analyze_sohu_url(url_base)
        assert 'url' in news.keys()
        assert 'title' in news.keys()
        assert 'publish_time' in news.keys()
        assert 'content' in news.keys()
        assert 'category' in news.keys()
        assert 'source' in news.keys()
        assert 'imageurl' in news.keys()
        assert 'top_img' in news.keys()

    def test_analyze_wangyi_url(self):
        url_dict = {}
        url_dict['url'] = "https://dy.163.com/article/FQQQSHBC051481US.html?clickfrom=w_yw"
        url_dict['type'] = 'politics'
        news = analyze_wangyi_url(url_dict)
        assert 'url' in news.keys()
        assert 'title' in news.keys()
        assert 'publish_time' in news.keys()
        assert 'content' in news.keys()
        assert 'category' in news.keys()
        assert 'source' in news.keys()
        assert 'imageurl' in news.keys()
        assert 'top_img' in news.keys()

    def test_get_random_url(self):
        num = len(get_random_url())
        assert  num == 36**4

    def test_get_hot_search(self):
        hot_search_list = get_hot_search()
        for news in hot_search_list:
            assert 'title' in news.keys()
            assert 'value' in news.keys()

    def test_get_hot_click(self):
        now_date = get_now_date()
        hot_click = get_hot_click(now_date)
        assert len(hot_click) > 0

    def test_get_hot_detail(self):
        now_date = get_now_date()
        hot_comment = get_hot_comment(now_date)
        hot_comment_news = get_hot_detail(hot_comment)[0:10]
        for index in hot_comment_news:
            assert 'rank' in index.keys()
            assert 'title' in index.keys()
            assert 'publish_time' in index.keys()
            assert 'url' in index.keys()

    def test_hot_news_scratch(self):
        hot_news_list = hot_news_scratch()
        assert len(hot_news_list)>0

    def test_get_type_map(self):
        type_map = get_type_map()
        assert isinstance(type_map,dict)

    def test_get_classify_map(self):
        classify_map = get_classify_map()
        assert isinstance(classify_map,dict)

    def test_get_tencent_channel(self):
        tencent_channel = get_tencent_channel()
        assert len(tencent_channel) > 0

    def test_get_sina_channel(self):
        sina_channel = get_sina_channel()
        assert len(sina_channel)>0

    def test_get_wangyi_channel(self):
        wangyi_channel = get_wangyi_channel()
        assert len(wangyi_channel) > 0

    def test_load_tencent_news(self):
        tencent_news = load_tencent_news('24hours')
        assert len(tencent_news) > 0

    def test_load_sina_news(self):
        sina_news = load_sina_news("2510")
        assert len(sina_news) > 0

    def test_load_sohu_news(self):
        sohu_news = load_sohu_news()
        assert len(sohu_news) > 0

    def test_load_wangyi_news(self):
        wangyi_news = load_wangyi_news("guonei")
        assert len(wangyi_news) > 0

