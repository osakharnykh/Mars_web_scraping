# Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd

from splinter import Browser
from selenium import webdriver
import os
import time


def scrape():
    
    #Scrape NASA Mars News
    url_news='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    html_news = requests.get(url_news)
    soup_news = BeautifulSoup(html_news.text, 'lxml')
    results_title = soup_news.find_all(class_='content_title')
    news_t=results_title[0].text.strip()
    results_par = soup_news.find_all(class_='rollover_description_inner')
    news_p=results_par[0].text.strip()
    
    #JPL Mars featured image
    url_jpl='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser = Browser('chrome', headless=False)
    browser.visit(url_jpl)

    html_jpl = browser.html
    soup_jpl = BeautifulSoup(html_jpl, 'html.parser')

    images = soup_jpl.find_all(class_='button fancybox')

    featured_image_url='https://www.jpl.nasa.gov'+images[0]['data-fancybox-href'] 
    
    #Mars weather
    url_weather='https://twitter.com/marswxreport?lang=en'
    html_weather=requests.get(url_weather)
    soup_weather=BeautifulSoup(html_weather.text,'html.parser')

    results_weather = soup_weather.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_weather = results_weather[0].text

    #Mars facts
    url_facts='https://space-facts.com/mars/'

    table_facts = pd.read_html(url_facts)
    df=table_facts[0]
    df.columns= ['title','value']

    html_table = df.to_html()
    
    #Mars hemispheres
    cerberus={'title':'Cerberus Hemisphere',
              'img_url':'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif'}
    schiaparelli={'title':'Schiaparelli Hemisphere', 
                  'img_url':'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif'}
    syrtis_major={'title':'Syrtis Major Hemisphere',
                 'img_url':'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif'}
    valles_marineris={'title':'Valles Marineris Hemisphere',
                     'img_url':'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif'}
    hemisphere_image_urls=[cerberus,
                           schiaparelli,
                           syrtis_major,
                           valles_marineris]

    mars={}
    mars['news_p']=news_p
    mars['news_t']=news_t
    mars['featured_image_url']=featured_image_url
    mars['mars_weather']=mars_weather
    mars['html_table']=html_table
    mars['hemisphere_image_urls']=hemisphere_image_urls
    
    return mars
    
    