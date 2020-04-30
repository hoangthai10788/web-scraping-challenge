from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser


def title_and_para():

    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    article_heading_list = []

    for article_heading in soup.find_all('div',class_="content_title"):
    
        try:        
            article_heading_list.append(article_heading.find('a').text)
        except:
            pass
        
    news_title = article_heading_list[0]

    article_paragraph_list = []

    for article_para in soup.find_all('div',class_="article_teaser_body"):
        
        try:        
            article_paragraph_list.append(article_para.text)
        except:
            pass
        
    news_p = article_paragraph_list[0]

    title_paragraph_dict = {"news_title": news_title, "news_p": news_p}

    browser.quit()

    return title_paragraph_dict


def featured_image():

    browser = init_browser()

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    image_list = []
    results = soup.find_all("div", class_ = "img")
    for image in results:
        image_list.append(image.img["src"])
    
    feature_image = image_list[0]

    
    featured_image_url = "https://www.jpl.nasa.gov" + feature_image

    featured_image_dict = {"image": featured_image_url}

    browser.quit()

    return featured_image_dict

def mars_weather():

    browser = init_browser()

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(1)

    xpath = "/html/body/div/div/div/div[2]/main/div/div/div/div/div/div/div/div/div[2]/section/div/div/div[1]/div/div/div/article/div/div[2]/div[2]/div[2]/div[1]/div/span"

    if browser.is_element_present_by_xpath(xpath, wait_time = 5):
        title = browser.find_by_xpath(xpath).text

    mars_weather_dict = {"mars_weather": title}

    browser.quit()
    return mars_weather_dict

def mars_facts():

    url = "https://space-facts.com/mars/"

    tables = pd.read_html(url)

    df = tables[0]

    df.columns = df.columns.astype(str)

    df = df.rename(columns = {"0": "Parameters", "1": "Values"})

    df_to_html = df.to_html("mars_facts_table.html")

    df_to_html_dict = {"mars_fact": df_to_html}

    return df_to_html_dict

def mars_hemispheres():

    browser = init_browser()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    base_url = "https://astrogeology.usgs.gov"

    titles = []
    img_hrefs = []
    results_title = soup.find_all("div", class_ = "description")
    for result in results_title:
        titles.append(result.h3.text)
        full_href = base_url + result.a["href"]
        img_hrefs.append(full_href)

    full_resolution_img = []

    for i in range(len(img_hrefs)):
        url = img_hrefs[i]
        browser.visit(url)
        html = browser.html
        soup = bs(html, "html.parser")
        result = soup.find("img", class_ = "wide-image")["src"]
        full_resolution = base_url + result
        full_resolution_img.append(full_resolution)

    hemisphere_image_urls = []
    hemisphere_image_urls_dict = {}

    for i in range(4):
        hemisphere_image_urls_dict["title"] = titles[i]
        hemisphere_image_urls_dict["img_url"] = full_resolution_img[i]
        hemisphere_image_urls.append(hemisphere_image_urls_dict)
        hemisphere_image_urls_dict = {}

    browser.quit()
    return hemisphere_image_urls

    

if __name__ == "__main__":
    print("\nTesting Data Retrieval:....\n")
    print(title_and_para())
    print(featured_image())
    print(mars_weather())
    print(mars_hemispheres())
    print("\nProcess Complete!\n")


