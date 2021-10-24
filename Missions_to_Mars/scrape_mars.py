# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# note book to complete mission to mars scraping and analysis tasks
# 

# %%
# importing libraires needed to run code, scrape and view
import pandas as pd
import ssl
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time


# %%
# getting around SSL Error...need to fix proper still
try:
   _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


def scrape():
    # %%
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # %%
    # setting url and opeing in browser to scrape latest news title and paragraph

    red_url = 'https://redplanetscience.com/'
    browser.visit(red_url)

    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    # mars_data['news_title'] = news_title
    # mars_data['news_p'] = news_p


    # %%
    # scraping images of Mars
    spc_url = 'https://spaceimages-mars.com/'
    browser.visit(spc_url)

    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    image_url = soup.find('img', class_='headerimage fade-in')['src']
    feature_image_url = spc_url + image_url


    # %%
    #using pandas to scrape table of facts about Mars
    facts_url = 'https://galaxyfacts-mars.com'


    # %%
    # reading table of facts into dataframe
    facts_df = pd.read_html(facts_url)


    # %%
    # creating mars facts dataframe
    mars_facts_df = facts_df[1]
    mars_facts_df.columns = ['Mars Facts', 'Value']
    mars_facts_df.head(9)


    # %%
    # use pandas to convert the data frame to a HTML table string
    mars_facts_html = mars_facts_df.to_html(index=False)


    # %%
    # visit hemispheres website
    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)
    time.sleep(1)

    # Create HTML object
    html = browser.html

    # parse with beautiful soup
    soup = bs(html, 'html.parser')


    # %%
    # retrieve all parent dive tags for each hemisphere
    hemisphere_divs = soup.find_all('div', class_='item')

    # create an empty list for the python dictionary
    hemisphere_image_data = []

    # loop through each div item to get hemisphere title and image url
    for hemisphere in range(len(hemisphere_divs)):
        
        #  use splinter to click on each hemisphere's link
        hem_link = browser.find_by_css("a.product-item h3")
        hem_link[hemisphere].click()
        time.sleep(1)

        # create bs object with image url
        img_detail_html = browser.html
        imagesoup = bs(img_detail_html, 'html.parser')

        # create base url for the full image
        base_url = 'https://marshemispheres.com/'

        # retrieve the full-resolution image url
        hem_url = imagesoup.find('img', class_='wide-image')['src']

        #  creating the full image for the full resolution image
        img_url = base_url + hem_url

        # get the title of the hemisphere
        img_title = browser.find_by_css('.title').text

        # append the title and image url to the list
        hemisphere_image_data.append({'title': img_title, 
                                    'img_url': img_url})

        # click on the back button
        browser.back()


    # %%
    browser.quit()


