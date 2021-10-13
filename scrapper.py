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
        self.load_page(movie_url)
        age_rating, year, movie_length = self.get_info()
        director, writer = self.get_cast()
        rating, num_review = self.get_rating()
        description = self.get_description(movie_url)

        return {'description': description,
                'rating': rating,
                'num_review': num_review,
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

    def get_cast(self):
        try:
            cast_box = self.browser.find_element_by_xpath("//section[@data-testid='title-cast']")
        except NoSuchElementException:
            cast_box = None
        
        director_box, writer_box = tuple(cast_box.find_element_by_xpath("//ul[@class='ipc-metadata-list ipc-metadata-list--dividers-all StyledComponents__CastMetaDataList-y9ygcu-10 cbPPkN ipc-metadata-list--base']") \
                                                 .find_elements_by_xpath("//li[@class='ipc-metadata-list__item']")[:2])

        directors = director_box.find_elements_by_tag_name('li')
        directors = [director.find_element_by_tag_name('a').text for director in directors] 

        writers = writer_box.find_elements_by_tag_name('li')
        writers = [writer.find_element_by_tag_name('a').text for writer in writers] 

        return directors, writers

    def get_rating(self):
        rating_box = self.browser.find_element_by_xpath("//div[@class='AggregateRatingButton__ContentWrap-sc-1ll29m0-0 hmJkIS']").text
        
        rating = rating_box.split('\n')[0].strip() 
        num_review= rating_box.split('\n')[-1].strip() 
        return rating, num_review 

    def get_description(self, movie_url):
        description_url = movie_url.replace('?ref_=', 'plotsummary?ref_=')
        self.browser.get(description_url)

        description_box = WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//li[@class='ipl-zebra-list__item']"))
        )
        description = description_box.find_element_by_tag_name('p')
        return description.text.strip()

    def load_page(self, movie_url):
        self.browser.get(movie_url)
        WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='ipc-poster ipc-poster--baseAlt ipc-poster--dynamic-width Poster__CelPoster-sc-6zpm25-0 kPdBKI celwidget ipc-sub-grid-item ipc-sub-grid-item--span-2']"))
        )
