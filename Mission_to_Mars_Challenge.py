#!/usr/bin/env python
# coding: utf-8

# # Module

# ### 10.3.3 Scrape Mars Data: The News

# In[1]:


#Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


#Set the executable path and initialize chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


#Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
#Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[5]:


slide_elem.find("div", class_='content_title')


# In[6]:


#Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[7]:


#Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### 10.3.4 Scrape Mars Data: Featured Image

# In[8]:


#Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[9]:


#Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


#Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


#Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


#Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# ### 10.3.5 Scrape Mars Data: Mars Facts

# In[13]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[14]:


df.to_html()


# In[15]:


browser.quit()


# In[ ]:





# # Challenge

# In[16]:


#Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[17]:


#Path to chromedriver
#!which chromedriver


# In[18]:


#Set the executable path and initialize chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[19]:


#Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

#Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[20]:


#Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[21]:


slide_elem.find("div", class_='content_title')


# In[22]:


#Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[23]:


#Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[24]:


#Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[25]:


#Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[26]:


#Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[27]:


#Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[28]:


#Use the base url to create an absolute url
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# ### Mars Facts

# In[29]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[30]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[31]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[32]:


#1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[33]:


html = browser.html
hemisphere_soup = soup(html, 'html.parser')


# In[34]:


#2. Create a list to hold the images and titles
hemisphere_image_urls = []

#3. Write code to retrieve the image urls and titles for each hemisphere
#Find hemisphere
hemisphere_pages = hemisphere_soup.find_all('div', class_='item')

#Base URL
base_url = 'https://astrogeology.usgs.gov'

for page in hemisphere_pages: 
    #Get title of hemisphere
    title = page.find('h3').get_text()
    #Navigate to each page
    page_url = page.find('a')['href']
    hemisphere_url = base_url + page_url
    browser.visit(hemisphere_url)
    #Parse
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_info = img_soup.find('div', class_='downloads')
    img_url = img_info.find('a')['href']
    
    hemispheres = {'img_url': img_url, 'title': title}
    hemisphere_image_urls.append(hemispheres)


# In[35]:


#4. Print the list that holds the dictionary of each image url and title
hemisphere_image_urls


# In[36]:


#5. Quit the browser
browser.quit()


# In[ ]:




