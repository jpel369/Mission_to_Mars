# import all dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time
import cssutils

# Function to initialize Splinter browser
def init_browser():
    executable_path = {"executable_path": "/Users/jamespelham/Downloads/chromedriver-3"}
    return Browser("chrome", **executable_path, headless=False)

# Define scrape function
def scrape():
    mars_info = {}

    # URL of page to be scraped
    nasa_url = 'https://mars.nasa.gov/news/'
    # Parsing site
    browser = init_browser()
    browser.visit(nasa_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Scraping latest article
    latest_article = soup.find("div", "list_text")
    news_title = latest_article.find("div", class_="content_title").text
    news_p = latest_article.find("div", class_="article_teaser_body").text
    print(news_title)
    print(news_p)

    # Adding to dict
    mars_info["news_title"] = news_title
    mars_info["teaser"] = news_p

    # Navigating to JPL site
    jpl_url = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    # Scraping JPL Mars site for image
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    carousel = soup.find('div', class_= 'carousel_items')
    div_style = carousel.find('article')['style']
    style = cssutils.parseStyle(div_style)
    part_url = style['background-image']
    print(part_url)

    part_url = part_url.replace('url(', '').replace(')', '')
    image_url = "https://jpl.nasa.gov" + partial_url
    print(image_url)

    # Adding to dict
    mars_info["image_url"] = image_url

    # Navigating to Twitter
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(tweet_url)

    # Pulling latest tweet
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.find("p", class_="tweet-text").text
    print(mars_weather)

    # Adding to dict
    mars_info["mars_weather"] = mars_weather

    # Mars facts site
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    # Scrape table
    facts = pd.read_html(facts_url)
    print(facts)

    facts_df = pd.DataFrame(facts[0])
    facts_df.columns=['Fact','Result - Mars', 'Result - Earth']
    facts_df.set_index('Fact')

    # Conver data table to html table string
    mars_table = facts_df.to_html(index=False, justify='left', classes='mars-table')
    mars_table = mars_table.replace('\n', ' ')

    # Adding to dict
    mars_info["mars_table"] = mars_table

    # Hemisphere image site
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)

    # Loop to scrape image info
    hemisphere_image_urls = []

    for i in range (4):
        time.sleep(10)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        part_url = soup.find("img", class_="wide-image")["src"]
        image_title = soup.find("h2",class_="title").text
        image_url = 'https://astrogeology.usgs.gov'+ part_url
        image_dict = {"title":image_title,"image_url":image_url}
        hemisphere_image_urls.append(image_dict)
        browser.back()

    # Adding to dict
    mars_info["hemispheres"] = hemisphere_image_urls

    # Quit browser
    browser.quit

    return mars_info


