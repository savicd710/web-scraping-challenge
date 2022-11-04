# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import time

def scrape():
    
    # Open the browser using ChromeDriverManager and splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    time.sleep(.5)

    # Visit the Mars News Site
    browser.visit('https://redplanetscience.com')
    time.sleep(.5)

    # Scrape the title and preview text of the first article on the Mars landing page
    soup = bs(browser.html, 'html.parser')

    news_title = soup.find(class_='content_title').text.strip()

    news_preview = soup.find(class_='article_teaser_body').text.strip()

    # Visit the Featured Space Image Site
    browser.visit('https://spaceimages-mars.com')
    time.sleep(.5)

    # Scrape the Featured Space Image
    soup = bs(browser.html, 'html.parser')

    featured_space_image = 'https://spaceimages-mars.com/' + soup.find(class_='showimg fancybox-thumbs')['href']

    # Scrape the table containing facts about the planet using Pandas
    tables = pd.read_html('https://galaxyfacts-mars.com')

    # Find the table I need and clean it up
    facts_table = tables[0]
    facts_table.columns = facts_table.iloc[0]
    facts_table = facts_table[1:]

    # Create an html table using Pandas
    html_table = facts_table.to_html(index=False).replace('\n', '')

    # Visit the Astrogeology site for hemisphere images
    browser.visit('https://marshemispheres.com/')
    time.sleep(.5)

    soup = bs(browser.html, 'html.parser')

    # Get the click through sites to find full image jpegs
    hemisphere_links = []

    for i in soup.find(class_='collapsible results').find_all('a'):
        hemisphere_links.append(i['href'])

    hemisphere_links = list(dict.fromkeys(hemisphere_links))

    # Go to each hemisphere and grab the title and image url
    hemisphere_image_urls = []

    for i in hemisphere_links:
        hemisphere_dict = {}
        browser.visit('https://marshemispheres.com/' + i)
        soup = bs(browser.html, 'html.parser')
        hemisphere_dict["title"] = soup.find(class_='title').text.strip()
        hemisphere_dict["img_url"] = 'https://marshemispheres.com/' + soup.find(class_='downloads').find('a')['href']
        hemisphere_image_urls.append(hemisphere_dict)
        time.sleep(.5)

    browser.quit()

    mars_data = {
        'news_title': news_title,
        'news_preview': news_preview,
        'featured_space_image': featured_space_image,
        'html_table': html_table,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    return mars_data

