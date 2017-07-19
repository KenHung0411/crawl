
# coding: utf-8

# # Yahoo Stock

# In this example, we're going to crawl the data from this page:
# ![yahoo_stock](../img/yahoo_stock.png)

# Before we actually dive into our code, you should notice that its URL is actually constructed with the stock ID like this:<br/>
# ![url_stock_id](../img/url_stock_id.png)
# 
# And through our observation, we know that our data lies within the HTML web page. So, **get web page, get data**.<br/><br/>
# By knowing this point, we can now roll up our sleeves and start coding!

# In[2]:

# First thing first, importing all the required libraries
import requests
import re
import pandas as pd
from datetime import datetime
import numpy as np


# In[3]:

# Defining the stock we want to get by its ID
stock_id = 2303

# Defining the url that we're about to call
url = 'https://tw.stock.yahoo.com/d/s/major_{stock_id}.html'.format(stock_id=stock_id)


# And we should be getting out web page by simply using **`requests.get()`**, easy peasy!

# In[4]:

r = requests.get(url=url)
r.raise_for_status()


# ![why](img/why.jpg)

# ---
# <h3>Note</h3>
# In some cases, the server would block the request if it detects that specific request comes from something other than web browsers (e.g. bots).<br/>
# In order to make the server believe that we're **a web browser**, we need to add some more information into our request header, just like what a regular browser would do.
# 
# ---
# 
# To solve this, we need to add some additional information into our request header so that the server won't _**think**_ that we're a bot. So, let's add **`User-agent`** into our request header and try again.

# In[12]:

header = {
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3)"\
    " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}
response = requests.get(url=url, headers=header)
response.raise_for_status()


# So it seems like there's no error, right? Just in case, let's take a look at the status code to see if everything works out okay. We can do so by calling `response.status_code`:

# In[13]:

response.status_code


# Awesome!
# ![my code works](../img/how_I_feel_when_my_code_works.png)

# The status code prints out as `200`, meaning `OK`, that we've got our result correctly! Hooray!!
# <br/>
# <hr/>
# Alright, now back onto our work, as we still need to parse the data from the web content...since I believe you won't call this thing below as _data_, right?
# <br/>
# ![raw_html](../img/raw_html_meme.png)

# Now, as the data varies every day, we would need to store the date along with everything. We can simply parse it from the web page as well.<br/><br/>
# Here we're using **_RegEx (Regular Expression)_** to parse the date on the web page.<br/><br/>If you don't know what RegEx is, don't worry, we'll explain it in our later course. Now, let's focus on how we can achieve this:

# In[14]:

response.text


# In[15]:

# Defining regex pattern to parse the date
date_pattern = re.compile(r'([0-9]+ /[0-9]+ /[0-9]+)')
date = list(map(int, date_pattern.findall(response.text)[0].split('/')))

# Adding 1911 to the first element as we don't want to store the date as R.O.C. calendar
date[0] = date[0] + 1911


# And convert the date into Python datetime object

# In[16]:

date = datetime(*date)


# Note that this line of code is identical as:
# 
#     date = datetime(year=date[0], month=date[1], day=date[2])
# 
# Here we're using **`*`** operator before an iterable to expand it within the function call.<br/>
# For more info, check out this [Stack Overflow post](http://stackoverflow.com/questions/3941517/converting-list-to-args-in-python).

# ### The Data Frame
# Here we're going to introduce **Data Frame**, which is the basic building block of how we process data. You can think of it as a table (in fact, it is a **table**, it's just a fancier name).<br/>
# <br/>
# What we're interested here is the main table within this page, as the `read_html` method would parse the whold HTML page into several data frames, including table object, we can assume the table we want is one of the entries in all the data frames.<br/>

# In[18]:

# Parse the whole HTML web page into several data frames
tables = pd.read_html(response.text)
print(tables)


# So far, what information we have can be used to identify the data frame and to extract it?<br/>

# <center><h2>Its shape</h2></center>

# As you might notice, the table we want has 8 columns, so we can see which data frame has exactly 8 columns, and that one should be our answer.<br/>

# To demonstrate, we can print out the # of columns of all the data frames by calling `Series.shape` method, which would return a tuple consists of height and width of a given data frame.<br/>

# The structure of the returning tuple would be: **`(# of row, # of column)`**, and since we're only interested in knowing the # of column each data frame has, we can just simply call **`Series.shape[1]`**.

# In[10]:

for idx, el in enumerate(tables):
    if tables[idx].shape[1] == 8:
        print('{0} < Here is the table we want.'.format(tables[idx].shape[1]))
    else:
        print(tables[idx].shape[1])


# So here we can see that only one data frame has 8 columns, which might be our answer; so we can use the `filter` method to filter out the unwanted data frames and leaving only one that we need.

# In[12]:

df = list(filter(lambda x:x.shape[1] == 8, tables))[0]
df


# Great job! Now that we have located our data frame, we can start processing the result and save it as a csv file, or store it into MySQL database, you name it.
# 
# ---
# 
# Okay, as we now have our table, we can try to think about how to store our data.<br/>
# <br/>
# Notice that we have some duplicated columns, and both **買超** and **賣超** are actually the difference between **Long** and **Short**; so we can save our space by not storing those 2 columns of data, and group everything into one table with only these columns:<br/><br/>
# <center>_**broker**_, _**long**_, _**short**_</center>
# <br/>
# Let's first extract the left-half and right-half of the table and see what we get:

# In[13]:

left = df.values[1:, 0:3]
print(type(left))
print('--------------------------')
print(left)


# In[14]:

right = df.values[1:, 4:7]
print(type(right))
print('--------------------------')
print(right)


# Note that both left-half and right-half of the table that we just extracted are in fact [N-dimensional arrays (`ndarray`)](https://docs.scipy.org/doc/numpy/reference/arrays.ndarray.html) of **`NumPy`**.<br/><br/>
# As we now want to concatenate both arrays into one, we're going to use **`numpy.r_`** ([See here for more info](https://docs.scipy.org/doc/numpy/reference/generated/numpy.r_.html).), which is a simple way to build up arrays quickly, to achieve this:

# In[5]:

d = np.r_[left, right]
type(d)
print(d)


# Now build up our final data frame

# In[16]:

stock_df = pd.DataFrame(d, columns=['broker', 'long', 'short'])

# We also need to know what stock ID is and the date
stock_df['stock_id'] = stock_id
stock_df['date'] = date

# Expliciitly changing the order of the columns
stock_df = stock_df[['date', 'stock_id', 'broker', 'long', 'short']]
stock_df


# Final step, assuming you might want to save your result as a csv file, we can achieve this easily by calling `pandas.DataFrame.to_csv`.

# In[ ]:

stock_df.to_csv('stock_{stock_id}.csv'.format(stock_id=stock_id))


# Great, our first crawler is finished!
# ![mission_accomplished](img/mission_accomplished.jpg)
