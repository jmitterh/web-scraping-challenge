# imports
from splinter import Browser
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time


# Connecting to chromedriver
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


# Master Scrape function
def scrape():
    '''
    Scrapping 5 url's relating to mars information:
    * 1. Latest Mars News
    * 2. Featured Mars Image
    * 3. Current Weather on Mars
    * 4. Mars Facts
    * 5. Mars High-Definition Hemispheres
    '''

    # dict to store all data
    mars_data = {}
    # calling chromedriver function
    browser = init_browser()

#1.    ######## LATEST MARS NEWS ########

    marsNews_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(marsNews_url)
    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    slide = soup.find_all('li', class_='slide')[0]
    title = slide.find('h3').text
    news_p = slide.find('div', class_='article_teaser_body').text
    # Store data in a dictionary
    mars_data["title"] = title
    mars_data["news_p"] = news_p

#2.    ######## FEATURED MARS IMAGE ########

    featuredImg_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featuredImg_url)
    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # Click the 'full image' button on each page
    try:
        new_peg = browser.click_link_by_id('full_image')
    except:
        print("Error, check the link id")
    fancybox = soup.find_all('a', class_='fancybox')[0]
    img = fancybox.get('data-fancybox-href')
    featured_image_url = f'https://www.jpl.nasa.gov/{img}'
    # Store data in a dictionary
    mars_data["featured_image_url"] = featured_image_url

#3.    ######## CURRENT WEATHER ON MARS ########

    marsWeather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(marsWeather_url)
    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_weather = soup.find('p', class_='TweetTextSize').text
    # Store data in a dictionary
    mars_data["mars_weather"] = mars_weather

#4.    ######## MARS FACTS ########

    marsFacts_url = "https://space-facts.com/mars/"
    # Use pandas to scrape tables within the url
    tables = pd.read_html(marsFacts_url)
    # Grab the first DF of Mars Facts
    df = tables[0]
    # Give column names
    df.columns = ['Description', 'Value']
    # set index to the description column
    df.set_index('Description', inplace=True)
    # Convert DF to HTLM
    html_table = df.to_html()
    # Remove any new line and extra white spaces
    html_table = html_table.replace('\n', ' ')
    # Store data in a dictionary
    mars_data["mars_facts"] = html_table

#5.    ######## MARS HIGH-DEFINITION HEMISPHERES ########

    marsHemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(marsHemi_url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    descriptions = soup.find_all('div', class_='description')
    # Defining  base url
    base_url = 'https://astrogeology.usgs.gov'
    # empty list for urls to get hd pic
    url_list = []
    # For loop to get url's with hd image
    for desc in descriptions:
        href = desc.find('a')['href']
        url_list.append(base_url + href)
    # list for dictionaries
    hemisphere_image_urls = []
    # For loop to iterate over list of url's to get url image and title
    for i in url_list:
        browser.visit(i)
        time.sleep(1)
        # Scrape page into Soup
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find('h2', class_='title').text
        wideimage = soup.find('img', class_='wide-image').get('src')
        img_url = base_url + wideimage
        dict = {'title': title, 'img_url': img_url}
        hemisphere_image_urls.append(dict)
    # Store data in a dictionary
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls
    # close the browser
    browser.quit()

    return mars_data
