import os
import pickle
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


browser = webdriver.Chrome('../chromedriver')
browser.implicitly_wait(5)


class IMDBPage:
    def __init__(self, browser=browser):
        self.browser = browser

    def get_details(self, movie_url):
        """
        TODO:
        - get video url
        - get age rating
        - get director & casts
        - get movie rating & num of reviews
        - get movie length
        """
        pass

    def get_description(self, movie_url):
        description_url = movie_url.replace('?ref_=', 'plotsummary?ref_=')
        self.browser.get(description_url)

        
        description_box = WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//li[@class='ipl-zebra-list__item']"))
        )
        description = description_box.find_element_by_tag_name('p')
        return description.text.strip()
