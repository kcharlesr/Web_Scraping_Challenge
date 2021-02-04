# kcharlesr


#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests

# In[2]:

def init_browser():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


# In[3]:
mars_data = {}

def scrape_info():
    browser = init_browser() 
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)


# In[4]:


    html = browser.html
    soup = bs(html, 'html.parser')
    slide_element = soup.select_one("ul.item_list li.slide")


# In[5]:


    slide_element.find("div", class_ = "content_title")


# In[6]:


    news_title = slide_element.find("div", class_ = "content_title").get_text()
    print(news_title)


# In[7]:


    news_par = slide_element.find("div", class_ = "article_teaser_body").get_text()
    print(news_par)


# In[8]:


    url = "https://www.jpl.nasa.gov/images/?search=&category=Mars"
    browser.visit(url)


# In[15]:


    img_html=browser.html
    soup=bs(img_html, "html.parser")
    base_url = "https://www.jpl.nasa.gov"
    latest_img = soup.find_all('div', class_="SearchResultCard")
    img=latest_img[0]
    latest=img.find("a")["href"]
    new_url = base_url + latest


# In[16]:


    print(new_url)


# In[17]:


    browser.visit(new_url)
    img_html=browser.html
    soup=bs(img_html, "html.parser")
    large_img = soup.find_all('div', class_="BaseImagePlaceholder")
    large_img = large_img[0]
    featured_image_url = large_img.find('img')['src']
    print(featured_image_url)


# In[22]:


    mars_df = pd.read_html("https://space-facts.com/mars/")[0]
    print(mars_df)


# In[24]:


    mars_df.columns=["Description", "Value"]
    mars_df


# In[25]:


    mars_df.set_index('Description', inplace=True)
    mars_df


# In[27]:


    mars_html=mars_df.to_html(classes='table table-striped')
    mars_html=mars_html.replace('<tr style="text-align: right;">','<tr style="text-align: left;">')
    mars_html


# In[28]:


    print(mars_html)


# In[29]:


    hemisphere_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)


# In[31]:


    hem_url='https://astrogeology.usgs.gov'
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere_image_urls = []
    results=soup.find_all('div',class_='item')
    for result in results:
        try:    
            hem=result.find('h3').text
            image=result.find('a')["href"]
            hem_url2=hem_url+image
            browser.visit(hem_url2)
            img_html=browser.html
            soup=bs(img_html, 'html.parser')
            image=soup.find('img', class_='wide-image')['src']
            new_url=hem_url+image
            hemis_dict = {"title": hem, "img_url":new_url}
            hemisphere_image_urls.append(hemis_dict)
            print(hem)
            print(new_url)
        except Exception as e:
            print(e)


# In[ ]:




    return mars_data