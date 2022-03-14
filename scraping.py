import datetime as dt

from bs4 import BeautifulSoup as soup
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    """Scrape data from four Mars websites and return dictionary of results."""
    # Initiate headless webdriver for deployment
    # Set up Splinter (prepping the automated browser)
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=True)

    # Retrieve the data for each of the four sections of the webpage
    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere_images(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "facts": facts,
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_image_urls,
    }

    # Stop webdriver
    browser.quit()

    return data


# ---- Mars Article Title and Paragraph ----------------------------------------
def mars_news(browser):
    """Scrape article title and summary data and return tuple of results."""
    # Visit the mars nasa news site
    url = "https://redplanetscience.com"
    browser.visit(url)

    # Delay for loading the page
    browser.is_element_present_by_css("div.list_text", wait_time=1)

    # Parse the HTML and return an object containing all of the html
    html = browser.html
    news_soup = soup(html, "html.parser")

    # Add try/except for error handling
    try:
        # Select the first div that holds the news article data
        slide_elem = news_soup.select_one("div.list_text")

        # Use the parent element to find the first `a` tag
        news_title = slide_elem.find("div", class_="content_title").get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ---- JPL Space Images: Featured Image ----------------------------------------
def featured_image(browser):
    """Scrape featured Mars image url and return as a string."""
    # Visit URL
    url = "https://spaceimages-mars.com"
    browser.visit(url)

    # Find and click the full image button. Since a ctrl+F search in the
    # devtools reveals there are only 3 button elements, we will select off the
    # index 1 button since the full image button is the second button element
    # on the page.
    full_image_elem = browser.find_by_tag("button")[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, "html.parser")

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find("img", class_="fancybox-image").get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f"{url}/{img_url_rel}"

    return img_url


# ---- Facts About Mars --------------------------------------------------------
def mars_facts():
    """Scrape Mars-Earth comparison table and return as string of html."""
    try:
        # Use pandas pd.read_html() to capture all of the tables on the
        # webpage. We're only interested in the first table (index 0)
        df = pd.read_html("https://galaxyfacts-mars.com")[0]

    except BaseException:
        return None

    # Restructure and reorganize the DataFrame
    df.columns = ["Description", "Mars", "Earth"]
    df.drop([0], inplace=True)
    df.set_index("Description", inplace=True)

    # Convert the DataFrame back into an html table
    return df.to_html(
        justify="left",
        border=0,
        classes=["table", "table-dark", "table-striped", "table-sm"],
    )


# ---- Hemisphere Images -------------------------------------------------------
def hemisphere_images(browser):
    """Scrape Mars hemisphere image urls/titles, return as list of dicts."""
    url = "https://marshemispheres.com/"
    browser.visit(url)

    # Store dictionaries of the image urls and their titles
    hemisphere_image_urls = []

    html = browser.html
    hemisphere_soup = soup(html, "html.parser")
    # Retrieve all the containers that have the anchor tags for the hemisphere
    # images.
    containers = hemisphere_soup.find_all("div", class_="item")

    for container in containers:
        # Find the title in the only h3 tag.
        title = container.find("h3").get_text()
        # Find the href in the first anchor tag, this is a relative url.
        next_rel_url = container.find("a").get("href")
        # Build the next url to visit.
        next_url = f"{url}{next_rel_url}"

        browser.visit(next_url)
        html = browser.html
        next_hemisphere_soup = soup(html, "html.parser")
        # Find the container that has the full resolution image relative url.
        next_container = next_hemisphere_soup.find("div", class_="wide-image-wrapper")
        # Find the href for the full resolution image, this is a relative url.
        hemi_img_rel_url = next_container.find("a").get("href")
        # Build the full url and append the dictionary containing the image url
        # and corresponding title.
        hemisphere_image_urls.append(
            {"img_url": f"{url}{hemi_img_rel_url}", "title": title}
        )
    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    data = scrape_all()
