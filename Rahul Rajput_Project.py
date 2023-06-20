#!/usr/bin/env python
# coding: utf-8

# ### Question 1.2

# In[286]:


from BeautifulSoup import BeautifulSoup
import requests
import re
import time


# ##### Part A

# In[287]:


# Part A

URL = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1"

session = requests.Session()
page = session.get(URL, headers={'User-Agent': 'Mozilla/5.0'})
print("The status code for website access is :",page.status_code)
#soup = BeautifulSoup(page.text, 'lxml')

with open("/Users/rahulrajput/Desktop/MSBA/Winter/422 - Data Design & Representation/Project/Ebay_Search_Pages/amazon_gift_card_01.htm", "w") as f:
        f.write(page.text)
        


# ##### Part B

# In[288]:


# Part B

for i in range(2,11):
    url_search_page = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn={}".format(i)
    search_page = requests.Session().get(url_search_page, headers={'User-Agent': 'Mozilla/5.0'})
    print("The status code for website access is :",search_page.status_code)
    #search_page_soup = BeautifulSoup(search_page.text, 'lxml')
    
    with open("/Users/rahulrajput/Desktop/MSBA/Winter/422 - Data Design & Representation/Project/Ebay_Search_Pages/amazon_gift_card_0{}.htm".format(i), "w") as f:
        f.write(search_page.text)
        
    time.sleep(10)


# ##### Part C

# In[289]:


# Part C

import os
directory = '/Users/rahulrajput/Desktop/MSBA/Winter/422 - Data Design & Representation/Project/Ebay_Search_Pages'
Search_Pages = []

for filename in os.listdir(directory):
    path = os.path.join(directory, filename)

    with open(path, "rb") as file:
      search_page_soup = BeautifulSoup(file)
    
    Search_Pages.append(search_page_soup)


# ##### Part D

# In[292]:


items = []
output_text = ""

for a in range(0,10):
    page = Search_Pages[a].select('div.s-item__wrapper.clearfix')
    
    for i in page:
        item_details = dict.fromkeys(('title','price','shipping_price','numeric_shipping_price','face_value'))
        
        for j in i.select('div.s-item__title'):
            #print(j.text)
            item_details['title'] = j.text
        
        for k in i.select('div.s-item__detail.s-item__detail--primary span.s-item__price'):
            #print(k.text)
            item_details['price'] = k.text
        
        for l in i.select('div.s-item__detail.s-item__detail--primary span.s-item__shipping.s-item__logisticsCost'):
            #print(l.text)
            item_details['shipping_price'] = l.text
        
        #print()
        
        items.append(item_details)
        


# In[291]:


items = items[1:]


# In[278]:


for x in range(0,len(items)):
    
    face = None if re.search('.*?([0-9]+[.]*[0-9]*).*',str(items[x]['title'])) == None else re.search('.*?([0-9]+[.]*[0-9]*).*',str(items[x]['title'])).group(1)
    items[x]['face_value'] = None if face == None else float(face)
    
    price = "0" if re.search('([0-9.]+)',str(items[x]['price'])) == None else re.search('([0-9.]+)',str(items[x]['price'])).group(1)
    items[x]['price'] = None if price == None else float(price)
    
    if items[x]['shipping_price'] == 'Free shipping':
        items[x]['numeric_shipping_price'] = 0
    else:
        ship_price = "0" if re.search('([0-9.]+)', str(items[x]['shipping_price'])) == None else re.search('([0-9.]+)', str(items[x]['shipping_price'])).group(1)
        items[x]['numeric_shipping_price'] = None if ship_price == None else float(ship_price)


# In[279]:


items


# In[263]:


items_safe_copy


# ##### Part E

# In[282]:


Above_Face_Value = []
for x in range(0,len(items)):
    if items[x]['face_value'] != None and items[x]['numeric_shipping_price'] != None and items[x]['price'] != None:
        if items[x]['face_value'] < items[x]['numeric_shipping_price'] + items[x]['price']:
            Above_Face_Value.append(items[x])


# In[285]:


len(Above_Face_Value)*100/len(items)


# ##### Part F
# Approximately 42% of the gift cards sell above the Face Value. The most likely cause would be shipping price which can be quite high compared to the actual value of the gift card.

# ### Question 2.1

# In[295]:


from bs4 import BeautifulSoup
import requests
import re
import time
import os


# In[296]:


URL = "https://www.fctables.com/user/login/"
session_requests = requests.Session()

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'}

res = session_requests.post(URL, data = {"login_action": "1",
                                         "login_username": "idislikebayernaswell",
                                         "login_password": "gomanchesterunited",
                                         "user_remeber": "1"},
                                         timeout = 15, 
                                         headers=headers)
print(res.status_code)


# In[297]:


cookies = session_requests.cookies.get_dict()
print(cookies)
page2 = session_requests.get('https://www.fctables.com/tipster/my_bets/',cookies=cookies)
doc2 = BeautifulSoup(page2.content, 'html.parser')

with open ('/Users/rahulrajput/Desktop/MSBA/Winter/422 - Data Design & Representation/Project/trial2.html','w') as file:
    file.write(page2.text)


# In[298]:


print(bool(doc2.findAll(text = re.compile("Wolfsburg"))))

