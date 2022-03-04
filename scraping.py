import datetime as dt

from bs4 import BeautifulSoup as soup
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment
    # Set up Splinter (prepping our automated browser)
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    facts = mars_facts()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "facts": facts,
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver
    browser.quit()

    return data

#---- Mars Article Title and Paragraph ----------------------------------------
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Parse the HTML and return an object containing all of the html
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Select the first div that holds the news article data
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as
        # `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

#---- JPL Space Images: Featured Image ----------------------------------------
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button. Since a ctrl+F search in the devtools
    # reveals there are only 3 button elements, we will select off the index 1
    # button since the full image button is the second button element on the page
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

#---- Facts About Mars --------------------------------------------------------
def mars_facts():
    try:
        # Use pandas pd.read_html() to capture all of the tables on the
        # webpage. We're only interested in the first table (index 0)
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Rename columns and set the index to the table headings
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Turn the DataFrame back into html
    return df.to_html()

if __name__ == "__main__":
    # If running as script, print scraped data
    data = scrape_all()
    print('-----------------------\n-----------------------')
    print(data)