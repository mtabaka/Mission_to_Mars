from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import requests
import time
import pandas as pd

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
    

def mars_scrape():
    browser = init_browser()

  
    # URL of News Page to scrape
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_="content_title")
    news_p = soup.find('div', class_="article_teaser_body")

    # Latest Featured Image

    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA19968_hires.jpg"
    browser.visit(featured_image_url)

    #browser.click_link_by_partial_text('FULL IMAGE')
    #time.sleep(20)
    browser.click_link_by_partial_text('FULL IMAGE')

    image_html = browser.html

    soup = BeautifulSoup(image_html, "html.parser")

    image_path = soup.find('figure', class_='lede').a['href']
    featured_image_url = "https://www.jpl.nasa.gov/" + image_path

    #mars weather
    weather_url = "https://twitter.com/marswxreport?lang=en"
    page = requests.get(weather_url)
    browser.visit(weather_url)
    weather_html = browser.html
    soup = BeautifulSoup(weather_html, 'html.parser')
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    #mars facts
    marsfacts_url = "https://space-facts.com/mars/"
    browser.visit(marsfacts_url)

    mars_facts = browser.html

    soup = BeautifulSoup(mars_facts, 'html.parser')

    facts = soup.find('table', class_="tablepress tablepress-id-mars")

    tables = pd.read_html(marsfacts_url)
    df = tables[0]
    df.head()

    all_facts = facts.find_all('tr')
    labels = []
    values = []

    for tr in all_facts:
        td_elements = tr.find_all('td')
        labels.append(td_elements[0].text)
        values.append(td_elements[1].text)

    mars_facts_df = pd.DataFrame({
        "Label": labels,
        "Values": values
        })

    fact_table = mars_facts_df.to_html(header = False, index = False)
    fact_table

    # images url scrape
    # new url
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(usgs_url)

    usgs_html = browser.html
    soup = BeautifulSoup(usgs_html, "html.parser")

    # gets class holding hemisphere picture
    returns = soup.find('div', class_="collapsible results")
    hemispheres = returns.find_all('a')

    #setup list to hold dictionaries
    hemisphere_image_urls =[]

    for a in hemispheres:
         #get title and link from main page
        title = a.h3
        link = "https://astrogeology.usgs.gov" + a['href']
    
        #follow link from each page
        browser.visit(link)
        time.sleep(5)
    
        #get image links
        image_page = browser.html
        results = BeautifulSoup(image_page, 'html.parser')
        img_link = results.find('div', class_='downloads').find('li').a['href']
    
        # create image dictionary for each image and title
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = img_link
    
        hemisphere_image_urls.append(image_dict)
    
        print(hemisphere_image_urls)
    

    mars_dict = {
        "id": 1,
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "fact_table": fact_table,
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict
    
