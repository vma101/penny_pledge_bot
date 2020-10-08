from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import platform as platform

import pandas as pd
from datetime import date

class Nonprofit:
    def __init__(self, name, site, content, scraper, EIN = ""):
        self.name = name
        self.site = site
        self.content = content
        self.content_scraper = scraper
        self.logo = ""
        self.tagline = ""
        self.mission = ""
        self.ein = EIN
        self.CharityNavigator = ""
        self.GreatNonprofits = ""
        self.Guidestar = ""

    def scrape_content(self):
        url_list, title_list, date_list, content_list, media_list = self.content_scraper(self.content)
        posts_dict = {'url': url_list, 'title': title_list, 'date': date_list, 'text': content_list, 'media': media_list}
        posts = pd.DataFrame(posts_dict)
        # posts.to_csv("{}_{}.csv".format(date.today().strftime("%Y%m%d"), self.name))
        # print("scraped {} posts for {}".format(len(url_list), self.name))
        return posts
    
    def scrape_general(self):
        # driver = webdriver.Firefox()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        # driver = webdriver.Chrome()
        driver.get(self.site)
        ### Attempt to scrape logo, tagline, mission"
        logo = ""
        tagline = ""
        try:
            logo = driver.find_element_by_class_name("logo").get_attribute("href")
            self.logo = logo
        except:
            print("Logo was not found")
        try:
            tagline = driver.find_element_by_xpath("//meta[@property='og:description']").get_attribute("content")
            self.tagline = tagline
        except:
            print("Tagline was not found")
        return print("Logo attribute was logged as {}, Tagline attribute was logged as {}".format(self.logo, self.tagline))

    def charity_navigator(self):
        if self.ein != "":
            driver = webdriver.Firefox()
            ein_strip = self.ein.strip("-")
            try:
                driver.get("https://charitynavigator.org/ein/{}".format(ein_strip))
                rating = ""
                self.CharityNavigator = rating
            except:
                print("Charity not logged on Charity Navigator")
            print("Charity Navigator rates {} with the following {}".format(self.name, self.charity_navigator))
        else:
            print("Missing EIN")
        return 

    def great_nonprofits(self):
        driver = webdriver.Firefox()

    def guidestar(self):
        if self.ein != "":
            driver = webdriver.Firefox()
            try:
                driver.get("https://www.guidestar.org/profile/{}".format(self.ein))
                rating = ""
                self.Guidestar = rating
                if self.mission == "":
                    mission = driver.find_element_by_id("mission-statement")
                    self.mission = mission
                if self.logo == "":
                    logo = driver.find_element_by_class_name("logo-container")
                    self.logo = logo
            except:
                print("Charity not logged on Guidestar")
                print("Charity Navigator rates {} with the following {}".format(self.name, self.guidestar))
        else:
            print("Missing EIN")
        return