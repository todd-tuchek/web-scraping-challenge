# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests 
import re
import pandas as pd
import pymongo
from selenium import webdriver
import time
import os

def init_browser(): 
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

mars = {}

# NASA MARS NEWS---------------------------------------------------------------
def scrape_info():
    # Visit the Nasa Mars News Site
    news_url = 'https://mars.nasa.gov/news/'
    response = requests.get(news_url)

    # Create an HTML object and parse with Beautiful Soup
    soup = bs(response.text, 'html.parser')

    # Extract latest news title and news paragraph
    news_title = soup.find('div', class_='content_title').a.text.strip()
    news_p = soup.find('div', class_='rollover_description_inner').text.strip()

    # Enter results into Dictionary
    mars['news_title'] = news_title
    mars['news_paragraph'] = news_p

    

    # JPL Mars Space Images - Featured Image--------------------------------------

    # Initialize Browser
    browser = init_browser()

    # Tell the browser below to go to img_url
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)

    time.sleep(1)

    # HTML object and parse with BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, 'html.parser')

    # Get background image url using style tag
    image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Connect image url to the website's main url
    main_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    featured_image_url = main_url + image_url

    # Display link to the features image url
    featured_image_url
    
    #Enter results into Dictionary
    mars['image_url'] = image_url

    browser.quit()
   

    # Mars Facts---------------------------------------------------------------------
 
    #Initialize Browser
    browser = init_browser()

    # Visit the Mars Facts webpage, use Pandas to scrape table of facts about Mars
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    time.sleep(1)

    # Read the HTML with pandas and parse the url to list the DataFrame
    tables = pd.read_html(facts_url)
    df = tables[1]

    # Assign columns and show esarth to mars comparison
    df.columns = ['Mars - Earth Comaprison', 'Mars', 'Earth']
    html_table = df.to_html(table_id="tablepress-p-mars", justify="left", index=False)
    df.to_dict(orient='records')
    df

    # Enter results into a dictionary
    mars['mars_table'] = html_table

    browser.quit()
    

    # Mars Hemispheres---------------------------------------------------------------------

    # Initizlize Browser
    browser = init_browser()

    # Mars Hemisphere url...tell browser to go to the link
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    
    time.sleep(1)

    # HTML Object and parse with Beautiful Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Final all items that contain mars hemisphere information
    title_list = soup.find_all('div', class_='description')

    # Create a list for hemisphere urls
    hemisphere_image_urls = []

    # Loop through the 'div' objects and scape the titles and urls of images
    for title in title_list: 
        # Navigate browser to page then click on title link to image page
        browser.visit(hemisphere_url)
        browser.click_link_by_partial_text(title.a.h3.text)

        # Grab the desitantion page HTML and make into Beautiful Soup Object
        html = browser.html
        soup = bs(html, 'html.parser')

        # Parse the image source ['src'] relative url and then append to domain name 
        img_url_list = soup.find('img', class_='wide-image')
        image_url = f"https://astrogeology.usgs.gov{img_url_list['src']}"

        # Create Dictionary with returned values and add dict to hemi_image_urls list
        post = {'title': title.a.h3.text, 'image_url': image_url}
        hemisphere_image_urls.append(post)

        # Display the hemisphere dictionary 
        hemisphere_image_urls


    mars['hemisphere_image_urls'] = hemisphere_image_urls
    browser.quit()
    return mars




