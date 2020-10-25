import json
count=0
date=[]
monthday=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16',
          '17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
for i in range(0,30):
    date.append(f"202008{monthday[i]}")

for index in date:
    dateNews=[]
    with open(f"newsData/{index}.json", 'r', encoding='utf-8') as load_f:
        strF = load_f.read()
        if len(strF) > 0:
            dateNews = json.loads(strF)
        else:
            dateNews = []
    #print(len(dateNews))
    count=count+len(dateNews)
print(count)