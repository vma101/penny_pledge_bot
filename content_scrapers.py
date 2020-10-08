from datetime import date
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import re
import os
import sqlite3 as db

################################### DRIVERS ###################################
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--disable-dev-shm-usage")
driver=webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

################################### COMPANY SCRAPERS ###################################

def get_page(url):
    # driver = webdriver.Firefox()
    # driver = webdriver.Chrome()
    # try:
    #     driver = webdriver.Chrome()
    driver.get(url)
    return driver

#### UPCHIEVE SCRAPER
def upchieve(content_site):
    # name = 'upchieve'
    class_text = 'BlogList-item-title'
    driver = get_page(content_site)
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        title_list.append(post_list[i].text)
        post_url = post_list[i].get_attribute('href')
        url_list.append(post_url)
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract date
        post_date = driver.find_element_by_class_name("Blog-meta-item--date").text
        # extract text
        post_text = driver.find_element_by_class_name("sqs-col-12")
        post_text_clean = post_text.text.strip()
        # extract image??
        post_media = driver.find_elements_by_class_name("thumb-image loaded")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://static1") == False:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list
    
#### REDROVER SCRAPER
def redrover(content_site):
    # name = 'redrover'
    tag_text = 'article'
    driver = get_page(content_site)
    post_list = driver.find_elements_by_tag_name(tag_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        # title_list.append(post_list[i].find_element_by_class_name("entry-summary").text)
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for i in range(len(url_list_all)):
        if url_list_all[i].startswith("https://redrover.org/{}".format(date.today().strftime('%Y'))):
            url_list.append(url_list_all[i])
    ###
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_class_name("section--title").find_element_by_tag_name("h2").text
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_class_name("section--title").find_element_by_tag_name("time").text
        # extract text
        post_text = driver.find_element_by_class_name("post-content").find_elements_by_tag_name("p")
        post_text_clean = []
        for p in post_text[:-1]:
            post_text_clean.append(p.text.strip())
        # extract image??
        post_media = driver.find_element_by_class_name("post-content").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://redrover.org"):
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### PCRF
def pcrf(content_site):
    name = 'pcrf'
    class_text = 'fusion-post-content'
    driver = get_page(content_site)
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        # title_list.append(post_list[i].find_element_by_class_name("entry-summary").text)
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for i in range(len(url_list_all)):
        if url_list_all[i].startswith("https://pcrf-kids.org/"):
            url_list.append(url_list_all[i])
    ###
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_tag_name("title").text
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_element_by_class_name("post-content").find_elements_by_tag_name("p")
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        # extract image??
        title_media = driver.find_element_by_class_name("flex-active-slide").find_element_by_tag_name("a").get_attribute("href")
        post_media = driver.find_element_by_class_name("post-content").find_elements_by_tag_name("img")
        post_media_clean = []
        post_media_clean.append(title_media)
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://pcrf-kids.org"):
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Pat Tillman Foundation
def pat_tillman(content_site):
    name = 'pat tillman'
    class_text = 'post_container'
    driver = get_page(content_site)
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        # title_list.append(post_list[i].find_element_by_class_name("entry-summary").text)
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for i in range(len(url_list_all)):
        if url_list_all[i].startswith("https://pattillmanfoundation.org/"):
            url_list.append(url_list_all[i])
    ###
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_elements_by_class_name("content")
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        # extract image
        title_media = driver.find_element_by_class_name("featured_image").find_element_by_tag_name("img").get_attribute("src")
        post_media_clean = []
        post_media_clean.append(title_media)
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Peer Health Exchange
def phe(content_site):
    name = 'phe'
    class_text = 'thumb'
    driver = get_page(content_site)
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        # title_list.append(post_list[i].find_element_by_class_name("entry-summary").text)
        post_url = post_list[i].get_attribute("href")
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for i in range(len(url_list_all)):
        if url_list_all[i].startswith("https://www.peerhealthexchange.org/"):
            url_list.append(url_list_all[i])
    ###
    for i in range(0, 5):
        # print(i)
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_elements_by_class_name("entry")
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        # extract image
        post_media_clean = []
        try:
            title_media = driver.find_element_by_class_name("wp-block-image").find_element_by_tag_name("img").get_attribute("src")
            post_media_clean.append(title_media)
        except:
            title_media = ''
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Ripple Effect Images
def ripple_effect_images(content_site):
    name = 'ripple effect images'
    class_text = 'entry-title'
    driver = get_page(content_site)
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    url_list = url_list_all
    ###
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_class_name("entry-title").text
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_class_name("published").text
        # extract text
        post_text = driver.find_element_by_class_name("entry-content").find_elements_by_tag_name("p")
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("entry-content").find_elements_by_tag_name("iframe")
        post_media_clean = []
        for pic in post_media:
            post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### MENTOR
def mentor(content_site):
    name = 'mentor'
    class_text = 'hentry'
    driver = get_page(content_site)
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    url_list = url_list_all
    ###
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_class_name("hentry").find_element_by_tag_name("h1").text
        title_list.append(post_title)
        post_date = ""
        # extract date
        # post_date = driver.find_element_by_class_name("hentry").find_element_by_class_name("glyphicon-time").text
        # extract text
        post_text = driver.find_element_by_class_name("hentry").find_elements_by_tag_name("p")
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        # extract image
        try:
            post_media = driver.find_element_by_class_name("hentry").find_elements_by_tag_name("iframe")
        except:
            post_media = []
        post_media_clean = []
        for pic in post_media:
            post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Our Resilience
def our_resilience(content_site):
    name = 'our resilience'
    class_text = 'hentry'
    driver = get_page(content_site)
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    url_list = url_list_all
    ###
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_elements_by_class_name("entry-content")
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("entry-content").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://www.ourresilience.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Operation First Response
def operation_first_response(content_site):
    name = 'operation first response'
    driver = get_page(content_site)
    class_text = 'post-content'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    url_list = url_list_all
    ###
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
        # print(post_title) #
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_class_name("meta-date").text
        # extract text
        post_text = driver.find_elements_by_class_name("post-content")
        # print(len(post_text)) #
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("post-content").find_elements_by_tag_name("img")
        # print(len(post_media)) #
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://www.operationfirstresponse.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### 4 Paws for Ability
def four_paws_for_ability(content_site):
    name = 'four paws for ability'
    driver = get_page(content_site)
    class_text = 'post-content'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
        title_list = []
        ### Need to siphon out urls specific to their own website information
    url_list = url_list_all
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_class_name("meta-date").text
        # extract text
        post_text = driver.find_elements_by_class_name("post-content")
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("post-content").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://4pawsforability.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Team Gleason
def team_gleason(content_site):
    name = 'team gleason'
    driver = get_page(content_site)
    class_text = 'et_pb_post'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
        title_list = []
        ### Need to siphon out urls specific to their own website information
    url_list = url_list_all
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_element_by_class_name("entry-content").find_elements_by_tag_name("p")
        post_text_clean = []
        p_num = 0
        for p in post_text:
            p_num += 1
            if p_num != 1:
                post_text_clean.append(p.text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("entry-content").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://teamgleason.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Youthlinc
def youthlinc(content_site):
    name = 'youthlinc'
    driver = get_page(content_site)
    class_text = 'elementor-post'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    url_list = url_list_all
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_element_by_class_name("entry-content").find_elements_by_class_name("elementor-section-wrap")
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("entry-content").find_element_by_class_name("elementor-section-wrap").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://youthlincer.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Eye to Eye
def eye_to_eye(content_site):
    name = 'eye to eye'
    driver = get_page(content_site)
    class_text = 'a'
    post_list = driver.find_elements_by_tag_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        if post_url != None:
            url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for i in range(len(url_list_all)):
        if url_list_all[i].startswith("https://eyetoeyenational.org/news/") == True:
            if url_list_all[i] not in url_list:
                url_list.append(url_list_all[i])
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
        title_list.append(post_title)
        # extract date
        # post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        post_date = ''
        # extract text
        post_text = driver.find_elements_by_class_name("rich-text")
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        # extract image
        # post_media = driver.find_element_by_class_name("ytp-cued-thumbnail-overlay").find_element_by_class_name("elementor-section-wrap").find_elements_by_tag_name("img")
        post_media_clean = []
        # for pic in post_media:
        #     post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Leukemia Research
def leukemia_research(content_site):
    name = 'leukemia research'
    driver = get_page(content_site)
    class_text = 'uabb-blog-post-content'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        if post_url not in url_list_all:
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
            url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for i in range(len(url_list_all)):
        if url_list_all[i].startswith("https://allbloodcancers.org/"):
            url_list.append(url_list_all[i])
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_elements_by_class_name("post-heading-content")
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("pp-heading-content").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://allbloodcancers.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Bunker Labs
def bunker_labs(content_site):
    name = 'bunker labs'
    driver = get_page(content_site)
    class_text = 'article'
    post_list = driver.find_elements_by_tag_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        if post_url not in url_list_all:
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
            url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for i in range(len(url_list_all)):
        if url_list_all[i].startswith("https://stories.bunkerlabs.org/"):
            url_list.append(url_list_all[i])
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_class_name("post-title").text
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_tag_name("time").get_attribute("datetime")[0:10]
        # extract text
        post_text = driver.find_elements_by_class_name("post-content")
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        # extract image
        title_media = driver.find_element_by_class_name("the-post").find_element_by_tag_name("img").get_attribute('src')
        post_media = driver.find_element_by_class_name("post-content").find_elements_by_tag_name("img")
        post_media_clean = []
        post_media_clean.append(title_media)
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://stories.bunkerlabs.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Team Rubicon:
def team_rubicon(content_site):
    name = 'team rubicon'
    driver = get_page(content_site)
    class_text = 'entry-title'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
    ### Need to siphon out urls specific to their own website information
    url_list = url_list_all
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_elements_by_class_name("entry-content")
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        # extract image
        post_media_clean = []
        try:
            title_media = driver.find_element_by_class_name("blog-featured-image").find_element_by_tag_name("img").get_attribute('src')
            post_media_clean.append(title_media)
        except:
            title_media = ''
        post_media = driver.find_element_by_class_name("entry-content").find_elements_by_tag_name("img")
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://teamrubiconusa.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Bernies Book Bank:
def bernies_book_bank(content_site):
    name = "bernies book bank"
    driver = get_page(content_site)
    class_text = 'et_pb_post'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
    ### Need to siphon out urls specific to their own website information
    url_list = url_list_all
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_elements_by_class_name("entry-content")
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("et_pb_post").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://www.berniesbookbank.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Casa Central
def casa_central(content_site):
    name = "casa_central"
    driver = get_page(content_site)
    class_text = 'content'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
    ### Need to siphon out urls specific to their own website information
    url_list = url_list_all
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_tag_name("h1").text
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_class_name("date").text
        # extract text
        post_text = driver.find_elements_by_class_name("content")
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("main-content").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://www.casacentral.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Feeding America
def feeding_america(content_site):
    name = "feeding america"
    driver = get_page(content_site)
    class_text = 'node'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
    ### Need to siphon out urls specific to their own website information
    url_list = url_list_all
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_class_name("page-title").text
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_class_name("field--type-datetime").text
        # extract text
        post_text = driver.find_elements_by_class_name("field--name-body")
        post_text_clean = []
        for p in range(len(post_text)):
            if p == 0:
                post_text_clean.append(post_text[0].text.strip())
        # extract image
        post_media = driver.find_elements_by_class_name("field--type-image")
        post_media_clean = []
        for pic in post_media:
            if pic.find_element_by_tag_name('img').get_attribute('src').startswith("www.feedingamerica.org/") == True:
                post_media_clean.append(pic.find_element_by_tag_name('img').get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### GFI
def gfi(content_site):
    name = 'gfi'
    driver = get_page(content_site)
    class_text = 'a'
    post_list = driver.find_elements_by_tag_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
    ### Need to siphon out urls specific to their own website information
    for i in range(len(url_list_all)):
        if url_list_all[i].startswith("https://www.gfi.org/blog-") == True:
            url_list.append(url_list_all[i])
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@name='DC.date.issued']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_elements_by_class_name("normalFont")
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("blog-content").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://gfi.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### ICStars
def icstars(content_site):
    name = 'icstars'
    driver = get_page(content_site)
    class_text = 'hentry'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    url_list = url_list_all
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_element_by_class_name("post-content").find_elements_by_class_name("p")
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        post_link = driver.find_element_by_class_name("post-content").find_element_by_class_name("fusion-button").get_attribute("href")
        post_text_clean.append(post_link)
        # extract image
        # post_media = driver.find_element_by_class_name("entry-content").find_element_by_class_name("elementor-section-wrap").find_elements_by_tag_name("img")
        post_media_clean = []
        # for pic in post_media:
        #     if pic.get_attribute('src').startswith("https://youthlincer.org/") == True:
        #         post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### NAFC
def nafc(content_site):
    name = 'nafc'
    driver = get_page(content_site)
    class_text = 'views-field-title'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for url in url_list_all:
        if url.startswith("https://www.nafcclinics.org/"):
            url_list.append(url)
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_id("page-title").text
        title_list.append(post_title)
        # # extract date (could not find date)
        # post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        post_date = ''
        # extract text
        post_text = driver.find_elements_by_class_name("node-content")
        post_text_clean = []
        for p in post_text:
            post_text_clean.append(p.text.strip())
        # extract image
        try:
            post_media = driver.find_element_by_class_name("entry-content").find_element_by_class_name("elementor-section-wrap").find_elements_by_tag_name("img")
        except:
            post_media = []
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://www.nafcclinics.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Blessings in a Backpack
def blessings_in_a_backpack(content_site):
    name = 'blessings in a backpack'
    driver = get_page(content_site)
    class_text = 'hentry'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_class_name("entry-title").find_element_by_tag_name("a").get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for url in url_list_all:
        if url.startswith("https://www.blessingsinabackpack.org/"):
            url_list.append(url)
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_element_by_class_name("wpb_wrapper").find_elements_by_tag_name("p")
        post_text_clean = []
        for p in range(len(post_text) -2):
            post_text_clean.append(post_text[p].text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("wp-content").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://www.blessingsinabackpack.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### The Recyclery
def recyclery(content_site):
    name = 'recyclery'
    driver = get_page(content_site)
    class_text = 'hentry'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_class_name("post-title").find_element_by_tag_name("a").get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for url in url_list_all:
        if url.startswith("https://www.therecyclery.org/"):
            url_list.append(url)
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_elements_by_class_name("post-content")
        post_text_clean = []
        for p in range(len(post_text)):
            post_text_clean.append(post_text[p].text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("hentry").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://www.therecyclery.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Be the Match
def be_the_match(content_site):
    name = 'be the match'
    driver = get_page(content_site)
    class_text = 'blog-summary-tile'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for url in url_list_all:
        if url.startswith("https://bethematch.org/blog"):
            url_list.append(url)
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@name='dcterms:title']").get_attribute("content")
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@name='dcterms:date']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_elements_by_class_name("content")
        post_text_clean = []
        for p in range(len(post_text)):
            post_text_clean.append(post_text[p].text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("post").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://bethematch.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Opportunity Knocks
def opportunity_knocks(content_site):
    name = 'opportunity knocks'
    driver = get_page(content_site)
    class_text = 'hentry'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_class_name("entry-title").find_element_by_tag_name("a").get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for url in url_list_all:
        if url.startswith("https://www.opportunityknocksnow.org/"):
            url_list.append(url)
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_class_name("entry-title").text
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_class_name("updated").text
        # extract text
        post_text = driver.find_elements_by_class_name("post-content")
        post_text_clean = []
        for p in range(len(post_text)):
            post_text_clean.append(post_text[p].text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("post-content").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://www.opportunityknocksnow.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Her Justice
def her_justice(content_site):
    name = 'her justice'
    driver = get_page(content_site)
    class_text = 'archive-content'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for url in url_list_all:
        if url.startswith("https://herjustice.org/"):
            url_list.append(url)
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_elements_by_class_name("main-text")
        post_text_clean = []
        for p in range(len(post_text)):
            post_text_clean.append(post_text[p].text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("main-content").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://herjustice.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Urban Pathways
def urban_pathways(content_site):
    name = 'urban pathways'
    driver = get_page(content_site)
    class_text = 'entry-title'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for url in url_list_all:
        if url.startswith("https://www.urbanpathways.org/"):
            url_list.append(url)
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")[:-17]
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@itemprop='datePublished']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_elements_by_class_name("sqs-block-content")
        post_text_clean = []
        for p in range(len(post_text) - 7):
            if len(post_text[p].text)>0:
                post_text_clean.append(post_text[p].text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("entry-content").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in range(len(post_media) -1):
            if post_media[pic].get_attribute('src').startswith("https://images.squarespace-cdn.com/") == True:
                post_media_clean.append(post_media[pic].get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Bowery
def bowery_mission(content_site):
    name = 'bowery mission'
    driver = get_page(content_site)
    class_text = 'hentry'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for url in url_list_all:
        if url.startswith("https://www.bowery.org/updates"):
            url_list.append(url)
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")[:-30]
        title_list.append(post_title)
        # print(post_title) #
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_element_by_class_name("entry-content").find_elements_by_tag_name("p")
        # print(len(post_text)) #
        post_text_clean = []
        for p in range(len(post_text)):
            try:
                post_text_clean.append(post_text[p].text.strip())
            except:
                None
        # extract image
        try:
            title_media = driver.find_element_by_class_name("featured-media").find_element_by_tag_name("img").get_attribute('src')
        except:
            title_media = ''
        post_media = driver.find_element_by_class_name("entry-content").find_elements_by_tag_name("img")
        post_media_clean = []
        # print(len(post_media)) #
        if title_media != '':
            post_media_clean.append(title_media)
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://www.bowery.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Capital Area Food Bank
def capital_area_food_bank(content_site):
    name = 'capital area food bank'
    driver = get_page(content_site)
    class_text = 'feed-item__title'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        # post_title = post_list[i].find_element_by_class_name("post-header").find_element_by_tag_name("a").text
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for url in url_list_all:
        if url.startswith("https://www.capitalareafoodbank.org/"):
            url_list.append(url)
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")[:-25]
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_elements_by_class_name("page-body")
        post_text_clean = []
        for p in range(len(post_text)):
            post_text_clean.append(post_text[p].text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("page-body").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://www.capitalareafoodbank.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Girls Who Code
def girls_who_code(content_site):
    name = 'girls who code'
    driver = get_page(content_site)
    class_text = 'NewsList-item'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for url in url_list_all:
        if url.startswith("https://girlswhocode.com/news"):
            url_list.append(url)
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_class_name("NewsArticle-header").text
        title_list.append(post_title)
        # # extract date (cannot find date)
        # post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        post_date = ''
        # extract text
        post_text = driver.find_elements_by_class_name("NewsArticle-body")
        post_text_clean = []
        for p in range(len(post_text)):
            post_text_clean.append(post_text[p].text.strip())
        # # extract image (posts don't seem to have media)
        # post_media = driver.find_element_by_class_name("page-body").find_elements_by_tag_name("img")
        post_media_clean = []
        # for pic in post_media:
        #     if pic.get_attribute('src').startswith("https://www.capitalareafoodbank.org/") == True:
        #         post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Howard Brown
def howard_brown(content_site):
    name = 'howard brown'
    driver = get_page(content_site)
    class_text = 'buttons'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for url in url_list_all:
        if url.startswith("https://howardbrown.org/"):
            url_list.append(url)
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")[:-22]
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content")[0:10]
        # extract text
        post_text = driver.find_elements_by_class_name("content")
        post_text_clean = []
        for p in range(len(post_text)):
            post_text_clean.append(post_text[p].text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("content").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://howardbrown.org/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list

### Our Climate
def our_climate(content_site):
    name = 'our climate'
    driver = get_page(content_site)
    class_text = 'page-excerpt'
    post_list = driver.find_elements_by_class_name(class_text)
    title_list = []
    url_list_all = []
    url_list = []
    date_list = []
    content_list = []
    media_list = []
    for i in range(len(post_list)):
        post_url = post_list[i].find_element_by_tag_name("a").get_attribute("href")
        url_list_all.append(post_url)
        ### Need to siphon out urls specific to their own website information
    for url in url_list_all:
        if url.startswith("https://www.ourclimate.us/"):
            url_list.append(url)
    for i in range(0, 5):
        driver.get(url_list[i])
        # extract title
        post_title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
        title_list.append(post_title)
        # extract date
        post_date = driver.find_element_by_class_name("byline").text[-12:]
        # extract text
        post_text = driver.find_elements_by_class_name("content")
        post_text_clean = []
        for p in range(len(post_text)):
            post_text_clean.append(post_text[p].text.strip())
        # extract image
        post_media = driver.find_element_by_class_name("content").find_elements_by_tag_name("img")
        post_media_clean = []
        for pic in post_media:
            if pic.get_attribute('src').startswith("https://d3n8a8pro7vhmx.cloudfront.net/") == True:
                post_media_clean.append(pic.get_attribute('src'))
        # append back into list
        date_list.append(post_date)
        content_list.append(post_text_clean)
        media_list.append(post_media_clean)
    driver.quit()
    return url_list[0:len(title_list)-1], title_list, date_list, content_list, media_list


content_scraper = {
    'upchieve': upchieve,
    'redrover': redrover,
    'pcrf': pcrf,
    'pat tillman': pat_tillman,
    'ripple effect images': ripple_effect_images,
    'phe': phe,
    'mentor': mentor,
    'our resilience': our_resilience,
    'operation first response': operation_first_response,
    'four paws for ability': four_paws_for_ability,
    'team gleason': team_gleason,
    'youthlinc' : youthlinc,
    'eye to eye': eye_to_eye,
    'leukemia research': leukemia_research,
    'bunker labs': bunker_labs,
    'team rubicon': team_rubicon,
    'bernies book bank': bernies_book_bank,
    'casa central': casa_central,
    'feeding america': feeding_america,
    'gfi': gfi,
    'icstars': icstars,
    'nafc': nafc,
    'blessings in a backpack': blessings_in_a_backpack,
    'recyclery': recyclery,
    'be the match': be_the_match,
    'opportunity knocks': opportunity_knocks,
    'her justice': her_justice,
    'urban pathways': urban_pathways,
    'bowery mission': bowery_mission,
    'capital area food bank': capital_area_food_bank,
    'girls who code': girls_who_code,
    'howard brown': howard_brown,
    'our climate': our_climate
}
















