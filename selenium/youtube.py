import random
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

browser.get("http://www.youtube.com")
search_bar=browser.find_element_by_id('masthead-search-term')
search_bar.send_keys("python programming")
search_bar.submit()

filter_button = browser.find_element_by_class_name("filter-button-container").find_element_by_tag_name("button")
filter_button.click()
time.sleep(1)
browser.find_element_by_link_text("Hoy").click()
time.sleep(1)

videos = browser.find_elements_by_class_name("yt-uix-tile-link")
videoIndex = random.randint(2,len(videos))
print videos[videoIndex]
videos[videoIndex].click()
