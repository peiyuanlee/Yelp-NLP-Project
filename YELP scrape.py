#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
import warnings
import time 
warnings.filterwarnings("ignore")
num = 0
Restaurants = []
Review = []
NumReview = []
CustomerReviews =  []
RestaurantReviews = []

while True:
    url = ("https://www.yelp.com/search?find_desc=Restaurants&find_loc=Tokyo%2C%20Japan&start="+str(num))
    try:
        html = requests.get(url, verify = False).text
        soup = BeautifulSoup(html, "lxml")
        tokyo = soup.find("main", id = "main-content")
        restaurants = tokyo.find_all("a", attrs = {"target":"_blank", "rel" : "noopener", "name": re.compile("..")})
        numReview = tokyo.find_all("span", class_ = re.compile("\AreviewCount.."))
        review = tokyo.find_all("div", attrs = {"role" : "img"})
        
        #get name, average review and number of reviews for each restaurant
        for k in range(len(restaurants)):
            url1 = "https://www.yelp.com" + str(restaurants[k].get("href"))
            html1 = requests.get(url1, verify = False).text
            soup1 = BeautifulSoup(html1, "lxml")
            page = soup1.find_all("li", class_ = "margin-b5__09f24__pTvws border-color--default__09f24__NPAKY")
            
            if(page != None):
                CustomerReviews = []
                
                #get comments from each restaurant
                for j in range(len(page)):
                    if(page[j].find("span", lang = "en") != None):
                        CustomerReviews.append(page[j].find("span", lang = "en").text)
                Restaurants.append(restaurants[k].text)
                Review.append((review[k]['aria-label']).split()[0])
                NumReview.append(numReview[k].text)
                RestaurantReviews.append(CustomerReviews)
            time.sleep(20)
       
        num += 10
        time.sleep(20)
    except AttributeError:
        break 
        
        
data1={'Restaurants':Restaurants,'Review':Review, "Number of Reviews": NumReview, "Customer Reviews": RestaurantReviews}

df1=pd.DataFrame(data1)

df1 


# In[2]:


df1[df1["Customer Reviews"].str.len() == 0]


# In[5]:


df1 = df1[df1["Customer Reviews"].str.len() != 0]


# In[10]:


df1.loc[98]["Customer Reviews"]


# In[6]:


from pathlib import Path  
filepath = Path('yelp.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df1.to_csv(filepath)

