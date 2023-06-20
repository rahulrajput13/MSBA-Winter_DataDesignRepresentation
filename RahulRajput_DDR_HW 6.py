#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
get_ipython().system('{sys.executable} -m pip install pymongo')


# In[11]:


import bson


# In[4]:


import json
import pymongo


# In[20]:


# Requires pymongo 3.6.0+
from pymongo import MongoClient

MONGO_URI="mongodb://<username>:<password>@cluster-details"
client = MongoClient("mongodb://localhost:27017/")
database = client["samples_pokemon"]
db_names = client.list_database_names()
print(db_names)
collection = database["samples_pokemon"]

# Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

query = collection.find().limit(10)

for q in query:
    print(q)


# In[21]:


query = collection.find().limit(5)

for q in query:
    print(q)


# ### Part 1

# #### Question 1
# Please write code (Python or Java) to query and print to screen all Pokémon character “name”s (and “_id” but not the entire document) with candy_count >= month + day of your birthday  (e.g., my birthday is 2/12 and I query candy_count >= 14 as 2+12 = 14).  (25% of points)   (Note:  the MongoDB operator for “>=” is “$gte”)

# In[34]:


query2 = collection.find({"candy_count":{"$gt":17}},{"name":1})

for q in query2:
    print(q)


# #### Question 2
# Please write code (Python or Java) to query and print to screen all Pokémon character “name”s (and “_id” but not the entire document) with num = month or num = day of your birthday  (e.g., my birthday is 2/12 and I have to query num = 2 or num = 12). 

# In[33]:


query3 = collection.find({"$or":[{"num":"004"},{"num":"013"}]},{"name":1})

for q in query3:
    print(q)


# ### Part 2

# In[32]:


client2 = MongoClient("mongodb://localhost:27017/")
database2 = client2["crunchbase"]
db_names2 = client2.list_database_names()
print(db_names2)
collection2 = database2["crunchbase_database"]

# Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

query4 = collection2.find().limit(10)

for q in query4:
    print(q)


# #### Question 3
# MongoDB supports RegEx.  The MongoDB operator for RegEx is “$regex”.  For example, to find all Crunchbase documents that have a (company) name that starts with a lower case character, we can search for “db.crunchbase_database.find({"name" : {$regex : "^[a-z].*"}})”
# 
# (And some RegEx as well …) Please write code (Python or Java) to query and print to screen all Crunchbase company “name”s (and “_id” but not the entire document) that have “text” in their “tag_list”.  (25% of points)

# In[38]:


query5 = collection2.find({"tag_list":{"$regex":".*text.*"}},{"name":1})

for q in query5:
    print(q)


# #### Question 4
# 
# Please write code (Python or Java) to query and print to screen all Crunchbase company “name”s and “twitter_username” (and “_id” but not the entire document) that (i) were founded between 2000 and 2010 (including 2000 and 2010), or (ii) email address is ending in “@gmail.com”.

# In[42]:


query6 = collection2.find({"$or":[{"founded_year":{"$gt":2000,"$lt":2010}},{"email_address":{"$regex":".*@gmail\.com$"}}]},{"name":1,"twitter_username":1})

for q in query6:
    print(q)

