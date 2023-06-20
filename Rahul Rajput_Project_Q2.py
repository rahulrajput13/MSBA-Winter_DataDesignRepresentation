#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import re
import time
import os


# In[67]:


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


# In[70]:


cookies = session_requests.cookies.get_dict()
print(cookies)
page2 = session_requests.get('https://www.fctables.com/tipster/my_bets/',cookies=cookies)
doc2 = BeautifulSoup(page2.content, 'html.parser')

with open ('/Users/rahulrajput/Desktop/MSBA/Winter/422 - Data Design & Representation/Project/trial2.html','w') as file:
    file.write(page2.text)


# In[72]:


print(bool(doc2.findAll(text = re.compile("Wolfsburg"))))

