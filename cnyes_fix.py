
# coding: utf-8

# # cnyes (鉅亨網)

# # collect all the news ids

# In[ ]:

import requests
url = "http://news.cnyes.com/api/v3/news/category/headline?limit=30&startAt=1490889600&endAt=1491839999"

res = requests.get(url)
data = res.json()


# In[ ]:

data.keys()


# In[ ]:

last_page = data['items']['last_page']


# In[ ]:

import requests

url = "http://news.cnyes.com/api/v3/news/category/headline?limit=30&startAt=1490889600&endAt=1491839999"
res = requests.get(url)
data = res.json()
last_page = data['items']['last_page']
page = 1
urls = []
while page <= last_page:
    url = "http://news.cnyes.com/api/v3/news/category/headline?limit=30&startAt=1490889600&endAt=1491839999&page={}".format(page)
    res = requests.get(url)
    data = res.json()
    print(page,len(data['items']['data']))
    urls.append(["http://news.cnyes.com/news/id/"+str(_['newsId']) for _ in data['items']['data']])
    page += 1
urls = sum(urls,[])


# In[ ]:

urls


# # parse single page

# In[ ]:

import requests
from bs4 import BeautifulSoup


# In[ ]:

url = "http://news.cnyes.com/news/id/3763088"
res = requests.get(url)
soup = BeautifulSoup(res.text,"lxml")


# In[ ]:

# title
soup.find("span",{"itemprop":"headline"}).text


# In[ ]:

# source & from
soup.find_all("span",{"itemprop":"name"})


# In[ ]:

# article
soup.find("div",{"itemprop":"articleBody"}).find_all('p')# article


# # refactor

# In[1]:

import requests
from bs4 import BeautifulSoup


def getNewsData(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"lxml")
    data = {"title":soup.find("span",{"itemprop":"headline"}).text,
            "info":",".join([_.text for _ in soup.find_all("span",{"itemprop":"name"})]),
            "body":"\n".join([_.text for _ in soup.find("div",{"itemprop":"articleBody"}).find_all('p')]),
            "url":url}
    return data


# In[2]:

def listNewsUrls(url):
    res = requests.get(url)
    data = res.json()
    last_page = data['items']['last_page']
    page = 2
    urls = []
    while page <= last_page:
        url = url+"&page={}".format(page)
        res = requests.get(url)
        data = res.json()
        urls.append(["http://news.cnyes.com/news/id/"+str(_['newsId']) for _ in data['items']['data']])
        page += 1
    return sum(urls,[])


# In[3]:

urls = listNewsUrls("http://news.cnyes.com/api/v3/news/category/headline?limit=30&startAt=1490889600&endAt=1491839999")


# In[6]:

data  = map(getNewsData,urls[0:10])
list(data)


# In[ ]:

import pandas as pd
df = pd.DataFrame(list(data))


# In[ ]:

df


# # keep the data

# In[ ]:

get_ipython().system('conda install mysql-connector-python -y')


# In[ ]:

import mysql.connector
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:<password>@localhost:3306', echo=False)
conn = engine.connect()
conn.execute("create database News")


# In[ ]:

df.to_sql(name='posts', con=engine, if_exists = 'append', index=False, schema='News')


# In[ ]:

read_sql_df = pd.read_sql(sql="select * from News.posts",con=engine)
read_sql_df

