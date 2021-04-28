#!/usr/bin/env python
# coding: utf-8
# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
# import requests
# import pymongo


# In[194]:

def scrape():
#set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

# URL of page to be scraped
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    html=browser.html

# Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

# Scrape the Mars News Site and collect the latest News Title and Paragraph Text
    news_title = soup.find('div', class_='content_title').text
    news_p=soup.find('div', class_='article_teaser_body').text
    print(news_title)
    print(news_p)

# URL of page to be scraped
    image_url= 'https://spaceimages-mars.com/'
    browser.visit(image_url)
    html=browser.html
# Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

# find the image url for the current Featured Mars Image 
#and assign the url string to a variable called featured_image_url.
    relative_image_path=soup.find("a", class_="showimg fancybox-thumbs")["href"]

    featured_image_url=image_url+relative_image_path
    featured_image_url

#scrape the table containing facts about the planet including Diameter, Mass, etc.
    table_url="https://galaxyfacts-mars.com/"
    tables=pd.read_html(table_url)
    df=tables[0]
    df.columns=df.columns.get_level_values(0)
    df.columns=["Description","Mars","Earth"]
    df=df.set_index("Description")

    # Use Pandas to convert the data to a HTML table string
    from pprint import pprint
    html_table=df.to_html()
    html_table=html_table.replace("\n","")
    pprint(html_table)

    #save the table to a html file
    df.to_html("table.html")

    # URL of astrogeology site to be scraped
    hemisphere_url="https://marshemispheres.com/"
    browser.visit(hemisphere_url)
    html=browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())

    # scrape for titles and url for each of Mar's hemispheres
    hemisphere_pages=soup.find_all("div", class_="item")
    pages=[]
    for page in hemisphere_pages:
        title=page.find("h3").text
        link=page.find("a",class_="itemLink product-item")["href"]
        page_url=hemisphere_url+link
        pages.append((title,page_url))
    # loop through for pages for the hemisphere image links
    hemisphere_image_urls=[]
    for(title,page_url)in pages:
        browser.visit(page_url)
        html=browser.html
        soup=BeautifulSoup(html, 'html.parser')
        link=soup.find("img",class_="wide-image")["src"]
        image_url=hemisphere_url+link
        hemisphere_image_urls.append((title,image_url))

    mars_data={"news_title":news_title,
            "news_p":news_p,
            "featured_image_url":featured_image_url,
            "table":html_table,
            "hemisphere_image_urls":hemisphere_image_urls}
    browser.quit()
    return mars_data

