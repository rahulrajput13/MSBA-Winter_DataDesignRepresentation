#!/usr/bin/env python
# coding: utf-8

# ## Part 1

# In[206]:


from bs4 import BeautifulSoup
import requests
import re
import time
import os


# In[207]:


Username = "MikoyanG"
Password = "Blackbird"


# In[208]:


URL_homepage = "https://www.planespotters.net"

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'}

homepage = requests.get(URL_homepage, headers=headers)
print("The status code for website access is :",homepage.status_code)
homesoup = BeautifulSoup(homepage.text, 'html.parser')


# In[209]:


links = []
for i in homesoup.select('div.page__header_actions a'):
    print(i['href'])
    links.append(i['href'])


# In[242]:


URL_login = URL_homepage + links[0]

session_requests = requests.session()
loginpage = session_requests.get("https://www.planespotters.net/user/login", headers=headers)
loginsoup = BeautifulSoup(loginpage.text, 'html.parser')

print("The status code for website access is :",loginpage.status_code)


# In[243]:


cookies_get = session_requests.cookies.get_dict()
print(cookies_get)


# In[244]:


csrf = loginsoup.select("input[name=csrf]", type="hidden")[0].get("value")
rid = loginsoup.select("input[name=rid]", type="hidden")[0].get("value")


# In[247]:


logging_in = session_requests.post("https://www.planespotters.net/user/login",
                          data = {"username": "MikoyanG", "password": "Blackbird", "csrf":csrf, "rid":rid},
                          #cookies = cookies_get,
                          headers=headers)

print("The status code for website access is :",logging_in.status_code)


# In[248]:


cookies_post = session_requests.cookies.get_dict()
print(cookies_post)


# In[266]:


final = session.get("https://www.planespotters.net/member/profile", headers=headers ,cookies=cookies_post)
final_check = BeautifulSoup(final.content, 'html.parser')
print("The status code for website access is :",final.status_code)

# Part 5A
print(final_check)

# Part 5B
total_cookies = list(cookies_get.items()) + list(cookies_post.items())
print(total_cookies)

# with open("/Users/rahulrajput/Desktop/MSBA/Winter/422 - Data Design & Representation/test" + ".html", "w") as f:
#    f.write(str(final_check))

# Part 5C
print(bool(final_check.findAll(text = "MikoyanG")))


# ## Part 2
# ### Question 1

# In[276]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(executable_path='/Users/rahulrajput/Desktop/MSBA/Winter/422 - Data Design & Representation/chromedriver_mac_arm64/chromedriver')
driver.implicitly_wait(10)
driver.set_script_timeout(120)
driver.set_page_load_timeout(10)

driver.get("https://google.com");
selector = "input[type=text]"
inp = driver.find_element("css selector", selector)
inp.send_keys("askew\n")
time.sleep(5)

driver.get("https://google.com");
selector = "input[type=text]"
inp = driver.find_element("css selector", selector)
inp.send_keys("Google in 1998\n")
time.sleep(5)

driver.quit()


# ### Question 2

# In[290]:


driver = webdriver.Chrome(executable_path='/Users/rahulrajput/Desktop/MSBA/Winter/422 - Data Design & Representation/chromedriver_mac_arm64/chromedriver')
driver.implicitly_wait(10)
driver.set_script_timeout(120)
driver.set_page_load_timeout(60)

driver.get("https://www.bestbuy.com/");
dotd = "a[data-lid='hdr_dotd']"  
deal = driver.find_element("css selector", dotd);
deal.click()
time.sleep(5)

element = "div[aria-live='Assertive']"
print(driver.find_element("css selector",element).text)


reviews = "a.ratings-reviews-link"  
reviews_page = driver.find_element("css selector", reviews);
reviews_page.click()
time.sleep(5)

with open("/Users/rahulrajput/Desktop/MSBA/Winter/422 - Data Design & Representation/HW 4/bestbuy_deal_of_the_day.htm", "w", encoding='utf-8') as f:
    f.write(driver.page_source)

driver.quit()

