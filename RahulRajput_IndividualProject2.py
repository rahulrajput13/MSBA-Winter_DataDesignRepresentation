#!/usr/bin/env python
# coding: utf-8

# In[302]:


import time
import os
import json
from bs4 import BeautifulSoup
import requests
import re
import pymongo
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    
    question2("https://opensea.io/collection/boredapeyachtclub?search[sortAscending]=false&search[stringTraits][0][name]=Fur&search[stringTraits][0][values][0]=Solid%20Gold")
    question3()
    question4()
    question5()
    question6()
    question7()
    question8()
    question9()
    ### DO everything in between
    
def question2(url):

    driver = webdriver.Chrome(executable_path='/Users/rahulrajput/Desktop/MSBA/Winter/422 - Data Design & Representation/chromedriver_mac_arm64/chromedriver')
    
    for i in range(0,8):
        driver.get(url);
        elements = driver.find_elements(By.CSS_SELECTOR,'a.sc-1f719d57-0.fKAlPV.Asset--anchor')
        #driver.execute_script("arguments[0].click();", elements[i])
        elements[i].click()
        time.sleep(5)
        content = driver.page_source
        with open(f"bayc_{i+1}.htm", "w", encoding="utf-8") as file:
            file.write(content)
            
        time.sleep(2)
    
    driver.quit()
    

def question3():
    
    client = MongoClient("mongodb://localhost:27017/")
    database = client["project2"]
    collection = database["bayc"]
    
    Ape_Soups = []
    for i in range(0,8):
        
        with open(f"bayc_{i+1}.htm", 'r', encoding="utf-8") as f:
            apesoup = BeautifulSoup(f, 'html.parser')

        Ape_Soups.append(apesoup)
        ape_name = apesoup.select("h1.sc-29427738-0.hKCSVX.item--title")[0].text

        ape_attributes = []
        attributes = apesoup.select('div.sc-d6dd8af3-0.hkmmpQ.item--property')

        for i in range(0,len(attributes)):
            attribute = dict.fromkeys(["type","value","rarity"])
            attribute['type'] = attributes[i].select('div.Property--type')[0].text.strip()
            attribute['value'] = attributes[i].select('div.Property--value')[0].text.strip()
            attribute['rarity'] = attributes[i].select('div.Property--rarity')[0].text.strip()

            ape_attributes.append(attribute)

        to_update = {"Name":ape_name, "Attributes":ape_attributes}
        collection.insert_one(to_update)    
    

def question4():
    
    location = "san francisco"
    num_results = 30
    ypurl = f"https://www.yellowpages.com/search?search_terms={search_term}&geo_location_terms={location}&num={num_results}%2C+CA"

    headers = {'authority': 'fls-na.amazon.com',
               'pragma': 'no-cache',
               'method': 'POST',
               'cache-control': 'no-cache',
               'dnt': '1',
               'upgrade-insecure-requests': '1',
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'sec-fetch-site': 'none',
               'sec-fetch-mode': 'navigate',
               'sec-fetch-dest': 'document',
               'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
              }

    session = requests.Session()
    page = session.get(ypurl, headers=headers)
    print("The status code for website access is :",page.status_code)

    with open ("sf_pizzeria_search_page.htm",'wb') as file:
        file.write(page.content)
    

def question5():
    with open ("sf_pizzeria_search_page.htm",'r', encoding="utf8") as file:
        page_html = file.read()
    
    pagesoup = BeautifulSoup(page_html,"html.parser")
    all_pizzerias = pagesoup.select("div.search-results.organic div.result")
    
    
    for i in range(0,len(all_pizzerias)):
        pizzeria = all_pizzerias[i]
        details = {}
        
        # Getting primary info
        if pizzeria.select('h2.n'):
            details['rank'] = re.search('([0-9]+)\.\s(.+)$',pizzeria.select('h2.n')[0].text).group(1)
            details['name'] = re.search('([0-9]+)\.\s(.+)$',pizzeria.select('h2.n')[0].text).group(2)
            details['list'] = pizzeria.select_one('h2.n a.business-name')['href']
        else:
            pass
        
        if pizzeria.select('div.ratings a span'):
            details['num_ratings'] = re.search('.*([0-9]+).*',str(pizzeria.select('div.ratings a span')[0])).group(1)
        else:
            pass
        
        if pizzeria.select('div.ratings a div'):
            details['star_rating'] = re.search('result-rating\s([a-z]+)',str(pizzeria.select('div.ratings a div')[0])).group(1)
        else:
            pass
        
        if bool(re.search('tripadvisor',str(pizzeria.select('div.ratings')[0]))):
            outputs = json.loads(pizzeria.select('div.ratings')[0]['data-tripadvisor'])
            details['tripadviser_ratings'] = outputs['rating']
            details['tripadviser_reviews_num'] = outputs['count']
        else:
            pass
        
        if pizzeria.select('div.ratings span'):
            details['tripadviser_count'] = pizzeria.select('div.ratings span')[0].text
        else:
            pass
        
        if pizzeria.select('div.amenities'):
            details['amenities'] = pizzeria.select('div.amenities div.amenities-info')[0].text
        else:
            pass
        
        if pizzeria.select('div.price-range'):
            details['price_range'] = len(pizzeria.select('div.price-range')[0].text)
        else:
            pass
        
        if pizzeria.select('div.years-in-business div.number'):
            details['years_in_business'] = pizzeria.select('div.years-in-business div.number')[0].text 
        else:
            pass
        
        if pizzeria.select('div.snippet p.body.with-avatar'):
            details['review'] = pizzeria.select('div.snippet p.body.with-avatar')[0].text
        else:
            pass
        
        print(details)
    
    return

def question6():

    client2 = MongoClient("mongodb://localhost:27017/")
    database = client2["project2"]
    collection2 = database["sf_pizzerias"]    
        
    with open ("sf_pizzeria_search_page.htm",'r', encoding="utf8") as file:
        page_html = file.read()
    
    All_Pizzeria_Details = []
    pagesoup = BeautifulSoup(page_html,"html.parser")
    all_pizzerias = pagesoup.select("div.search-results.organic div.result")
    
    for i in range(0,len(all_pizzerias)):
        pizzeria = all_pizzerias[i]
        details = {}
        
        # Getting primary info
        if pizzeria.select('h2.n'):
            details['rank'] = re.search('([0-9]+)\.\s(.+)$',pizzeria.select('h2.n')[0].text).group(1)
            details['name'] = re.search('([0-9]+)\.\s(.+)$',pizzeria.select('h2.n')[0].text).group(2)
            details['list'] = pizzeria.select_one('h2.n a.business-name')['href']
            restaurant_name = details['name']
        else:
            pass
        
        if pizzeria.select('div.ratings a span'):
            details['num_ratings'] = re.search('.*([0-9]+).*',str(pizzeria.select('div.ratings a span')[0])).group(1)
        else:
            pass
        
        if pizzeria.select('div.ratings a div'):
            details['star_rating'] = re.search('result-rating\s([a-z]+)',str(pizzeria.select('div.ratings a div')[0])).group(1)
        else:
            pass
        
        if bool(re.search('tripadvisor',str(pizzeria.select('div.ratings')[0]))):
            outputs = json.loads(pizzeria.select('div.ratings')[0]['data-tripadvisor'])
            details['tripadviser_ratings'] = outputs['rating']
            details['tripadviser_reviews_num'] = outputs['count']
        else:
            pass
        
        if pizzeria.select('div.ratings span'):
            details['tripadviser_count'] = pizzeria.select('div.ratings span')[0].text
        else:
            pass
        
        if pizzeria.select('div.amenities'):
            details['amenities'] = pizzeria.select('div.amenities div.amenities-info')[0].text
        else:
            pass
        
        if pizzeria.select('div.price-range'):
            details['price_range'] = len(pizzeria.select('div.price-range')[0].text)
        else:
            pass
        
        if pizzeria.select('div.years-in-business div.number'):
            details['years_in_business'] = pizzeria.select('div.years-in-business div.number')[0].text 
        else:
            pass
        
        if pizzeria.select('div.snippet p.body.with-avatar'):
            details['review'] = pizzeria.select('div.snippet p.body.with-avatar')[0].text
        else:
            pass
        
        print(details)
        
        All_Pizzeria_Details.append(details)
        
    collection2.insert_many(All_Pizzeria_Details)
        
def question7():

    client3 = MongoClient("mongodb://localhost:27017/")
    database = client3["project2"]
    collection3 = database["sf_pizzerias"]
    
    for element in collection3.find({},{"Details.list":1, "Details.rank":1}):
        url_pizza = "https://www.yellowpages.com" + element['Details']['list']
        print(url_pizza)
        rank = element['Details']['rank']

        headers = {'authority': 'fls-na.amazon.com',
                   'pragma': 'no-cache',
                   'method': 'POST',
                   'cache-control': 'no-cache',
                   'dnt': '1',
                   'upgrade-insecure-requests': '1',
                   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                   'sec-fetch-site': 'none',
                   'sec-fetch-mode': 'navigate',
                   'sec-fetch-dest': 'document',
                   'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                  }

        session7 = requests.Session()
        page7 = session7.get(url_pizza, headers=headers)
        print("The status code for website access is :",page7.status_code)

        with open (f"sf_pizzerias_{rank}.htm",'wb') as file:
            file.write(page7.content)        

            
def question8():
    
    q8 = []
    
    for i in range(1,31):
        with open (f"sf_pizzerias_{i}.htm",'r', encoding="utf8") as file:
            page8_html = file.read()
    
        pizzeria_page = BeautifulSoup(page8_html,"html.parser")
        #shop’s address, phone number, and website
        pizza_place = dict.fromkeys(['address','phone_num','website'])

        if pizzeria_page.select('section.inner-section span.address'):
            address = pizzeria_page.select('section.inner-section span.address')
            print(address[0].text)
            pizza_place['address'] = address[0].text

        if pizzeria_page.select('section.inner-section a.phone.dockable'):
            phnum = pizzeria_page.select('section.inner-section a.phone.dockable')
            print(phnum[0].text)
            pizza_place['phone_num'] = phnum[0].text

        if pizzeria_page.select('section.inner-section a.website-link.dockable'):
            website = pizzeria_page.select('section.inner-section a.website-link.dockable')[0]
            print(website['href']) 
            pizza_place['website'] = website['href']
            
        print(pizza_place)
    
        q8.append(pizza_place)
    
    return q8

def question9():
    import http.client, urllib.parse
    api_access_key = "e4cbb693bd389b3bd623cd45b7417c32"    
    client4 = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client4["mydatabase"]
    collection4 = database["sf_pizzerias"]
    
    for i in range(1,31):
        with open (f"sf_pizzerias_{i}.htm",'r', encoding="utf8") as file:
            page8_html = file.read()
    
        pizzeria_page = BeautifulSoup(page8_html,"html.parser")
        #shop’s address, phone number, and website
        pizza_place = dict.fromkeys(['address','phone_num','website'])

        if pizzeria_page.select('section.inner-section span.address'):
            address = pizzeria_page.select('section.inner-section span.address')
            print(address[0].text)
            pizza_place['address'] = address[0].text
            conn = http.client.HTTPConnection('api.positionstack.com')
            params = urllib.parse.urlencode({
                'access_key': api_access_key,
                'query': pizza_place['address'],
                'region': 'San Francisco',
                'limit': 1,
                })

            conn.request('GET', '/v1/forward?{}'.format(params))
            
            res = conn.getresponse()
            data = res.read()

            print(data.decode('utf-8'))

        if pizzeria_page.select('section.inner-section a.phone.dockable'):
            phnum = pizzeria_page.select('section.inner-section a.phone.dockable')
            print(phnum[0].text)
            pizza_place['phone_num'] = phnum[0].text

        if pizzeria_page.select('section.inner-section a.website-link.dockable'):
            website = pizzeria_page.select('section.inner-section a.website-link.dockable')[0]
            print(website['href']) 
            pizza_place['website'] = website['href']
            
        print(pizza_place)

        collection4.update_one({"rank":i},{"$set": {"geolocation":data.decode('utf-8')}})
        

    
if __name__ == "__main__":
    main()

