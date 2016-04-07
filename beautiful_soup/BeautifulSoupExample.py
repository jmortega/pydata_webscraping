import urllib2
from bs4 import BeautifulSoup
import time

# This is method that scrape URL and if it doesnt get scraped, waits for 20 seconds and then tries again. (I use it because my internet connection sometimes get disconnects)
def tryAgain(passed_url):
    try:
        page  = requests.get(passed_url,headers = random.choice(header), timeout = timeout_time).text
        return page
    except Exception:
        while 1:
            print("Trying again the URL:")
            print(passed_url)
            try:
                page  = requests.get(passed_url,headers = random.choice(header), timeout = timeout_time).text
                print("-------------------------------------")
                print("---- URL was successfully scraped ---")
                print("-------------------------------------")
                return page
            except Exception:
                time.sleep(20)
                continue 
             
main_url = "http://www.example.com"
             
main_page_html  = tryAgain(main_url)
main_page_soup = BeautifulSoup(main_page_html)

# Scrape all TDs from TRs inside Table
for tr in main_page_soup.select("table.class_of_table"):
    for td in tr.select("td#id"):
        print(td.text)
        # For acnhors inside TD
        print(td.select("a")[0].text)
        # Value of Href attribute
        print(td.select("a")[0]["href"])