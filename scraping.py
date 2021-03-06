#Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #Initialize headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    #Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


### 10.3.3 Scrape Mars Data: The News
def mars_news(browser):

    #Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    #Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        #Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        #Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p

### 10.3.4 Scrape Mars Data: Featured Image
def featured_image(browser):

    #Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    #Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None#Find the relative image url

    #Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url

### 10.3.5 Scrape Mars Data: Mars Facts
def mars_facts():
    #Add try/except for error handling
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
        
    except BaseException:
        return None

    #Assign columns and set index of dataframe        
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    
    #Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def hemispheres(browser):
    #1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')

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
    
    return hemisphere_image_urls

if __name__ == "__main__":
    #If running as script, print scrapted data
    print(scrape_all())