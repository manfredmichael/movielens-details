import os
import pickle
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


browser = webdriver.Chrome('../chromedriver')
browser.implicitly_wait(5)


class IMDBPage:
    def __init__(self, browser=browser):
        self.browser = browser

    def get_details(self, movie_url):
        self.browser.get(movie_url)

        age_rating, year, movie_length = self.get_info()
        director, writer = self.get_crew()
        rating, reviewer = self.get_rating()
        description = self.get_description(movie_url)

        return {'description': description,
                'rating': rating,
                'reviewer': reviewer,
                'director': director,
                'writer': writer,
                'age_rating': age_rating,
                'year': year,
                'movie_length': movie_length}

    def get_info(self):
        info = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr']"))
        ).find_elements_by_tag_name('li')

        age_rating= info[0].text
        year = info[1].text
        movie_length = info[2].text
        return age_rating, year, movie_length

    def get_crew(self):
        crew = WebDriverWait(self.browser, 3).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='PrincipalCredits__PrincipalCreditsPanelWideScreen-hdn81t-0 iGxbgr']"))
        ).text

        director = crew.split('\n')[1]
        writer = crew.split('\n')[3]
        return director, writer 

    def get_rating(self):
        rating_box = WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='AggregateRatingButton__ContentWrap-sc-1ll29m0-0 hmJkIS']"))
        ).text
        
        rating = rating_box.split('\n')[0].strip() 
        reviewer = rating_box.split('\n')[-1].strip() 
        return rating, reviewer 

    def get_description(self, movie_url):
        description_url = movie_url.replace('?ref_=', 'plotsummary?ref_=')
        self.browser.get(description_url)

        description_box = WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//li[@class='ipl-zebra-list__item']"))
        )
        description = description_box.find_element_by_tag_name('p')
        return description.text.strip()
