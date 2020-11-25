# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium import webdriver
import time

# using similar code from class activities

def init_browser():
    # executable_path = {'executable_path': 'C:/Program Files/chromedriver_win32/chromedriver'}
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    # return Browser("chrome", **executable_path)
    # executable_path = {"executable_path": ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=False)
    executable_path = {'executable_path': '/Users/diazd/Downloads/chromedriver_win32/chromedriver'}
    return Browser("chrome", **executable_path)

# create scrape function
def scrape():
    browser = init_browser()

    # use browser to open the url 
    url = "https://mars.nasa.gov/news/"

    browser.visit(url)

    time.sleep(1)

    # scrape page into soup
    html = browser.html
    soup = bs(html, "html.parser")

    # --- MARS LATEST NEWS---
    # obtain the latest news title and paragraph
    data = soup.find("li", class_="slide")
    news_title = data.find("div", class_="content_title").a.text
    paragraph = data.find("div", class_="article_teaser_body").text
    

    # Mars Images
    # visit Mars' url to get the full image url
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # use browser to open the url for image
    browser.visit(image_url) 

    # create html to parse
    html = browser.html

    # create soup object to parse html
    soup = bs(html, "html.parser")

    # use beautifulsoup to navigate to the image
    image = soup.find("li", class_="slide").a["data-fancybox-href"]

    # create the url for the image
    featured_image_url = "https://www.jpl.nasa.gov" + image
   
    # ---MARS FACTS---
    # url for Mars's facts 
    marsfacts_url  = "https://space-facts.com/mars/"

    # # Use panda's `read_html` to parse the url
    table = pd.read_html(marsfacts_url)

    # convert the 1st table to pandas df  
    marsfacts_df = table[0]

    #rename the columns
    # rename the columns
    marsfacts_df.columns=["Description", "Value"]
    
    # reset the index for the df
    marsfacts_df.set_index("Description", inplace=True)

    # convert df to an html table string
    marsfacts_html = marsfacts_df.to_html()

    # ---MARS HEMISPHERES---
    # get the url and open it with browser
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    # create html & use bs to create soup object
    html = browser.html
    soup = bs(html, "html.parser")

    data = soup.find_all("div", class_="item")
    
    # list to hold data for hemispheres
    hemisphere_image_urls = []

    # loop the data list to find titles and img urls for hemispheres
    for link in data:
    
        title = link.find("h3").text

        img_url = link.a["href"]
    
        url = "https://astrogeology.usgs.gov" + img_url
    
        # using requests to get full images 
        response = requests.get(url)
    
        # create soup object
        soup = bs(response.text,"html.parser")
    
        # find full image url
        new_url = soup.find("img", class_="wide-image")["src"]
    
        # create full image url
        full_url = "https://astrogeology.usgs.gov" + new_url
        
        #append the dic with the image url string and the hemisphere title to a list
        hemisphere_image_urls.append({"title": title, "img_url": full_url})
        
    # return one Python dictionary containing all of the scraped data
    # create dictionary to hold the obtained Mars' data
    mars_data= {
        "news_title": news_title,
        "paragraph" : paragraph,
        "featured_image_url": featured_image_url,
        "marsfacts_html": marsfacts_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # close the browser after scraping
    browser.quit()

    # return results
    return mars_data


