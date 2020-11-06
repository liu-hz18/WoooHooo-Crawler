import requests
from bs4 import BeautifulSoup

def getHotSearch():
    base_url = "http://top.baidu.com/buzz?b=2"
    response = requests.get(base_url)
    response.raise_for_status()
    response.encoding = 'gbk'
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    title = soup.select("table.list-table >  tr > td.keyword > a.list-title")
    title_list = []
    for index in title:
        title_list.append(index.text)
    hot_value = soup.select("table.list-table >  tr > td.last > span")
    hot_value_list = []
    for index in hot_value:
        hot_value_list.append(index.text)
    hot_search_list = []
    for i in range(0,len(title_list)):
        hot_dict = {}
        hot_dict['title'] = title_list[i]
        hot_dict['value'] = hot_value_list[i]
        hot_search_list.append(hot_dict)
    print(hot_search_list)
    print(len(hot_search_list))

getHotSearch()