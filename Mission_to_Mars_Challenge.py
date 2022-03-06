#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as soup
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Set up Splinter (prepping our automated browser)
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Article Title and Summary

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=2)


# In[4]:


# Parse the HTML and return an object containing all of the html
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
type(slide_elem)


# In[5]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[6]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[7]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[8]:


# Find and click the full image button. Since a ctrl+F search in the devtools
# reveals there are only 3 button elements, we will select off the index 1
# button since the full image button is the second button element on the page
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[9]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[10]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Table of Mars Information

# In[11]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.drop([0], inplace=True)
df.set_index('Description', inplace=True)
df


# In[12]:


df.to_html()


# ## D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[13]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[14]:


# 2. Create a list to hold the images and titles.
# Variable to store dictionaries of the image urls and their titles
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemisphere_soup = soup(html, 'html.parser')
# Retrieve all the containers that have the anchor tags for the hemisphere
# images.
containers = hemisphere_soup.find_all('div', class_='item')

for container in containers:
    # Find the title in the only h3 tag.
    title = container.find('h3').get_text()
    # Find the href in the first anchor tag, this is a relative url.
    next_rel_url = container.find('a').get('href')
    # Build the next url to visit.
    next_url = f'{url}{next_rel_url}'
    
    browser.visit(next_url)
    html = browser.html
    next_hemisphere_soup = soup(html, 'html.parser')
    # Find the container that has the full resolution image relative url.
    next_container = next_hemisphere_soup.find('div', class_="wide-image-wrapper")
    # Find the href for the full resolution image, this is a relative url.
    hemi_img_rel_url = next_container.find('a').get('href')
    # Build the full url and append the dictionary containing the image url and
    # corresponding title
    hemisphere_image_urls.append({'img_url': f'{url}{hemi_img_rel_url}',
                                  'title': title})


# In[15]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[16]:


# 5. Quit the browser
browser.quit()

