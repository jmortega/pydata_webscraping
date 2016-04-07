from Scraping import Scraping

if __name__ == "__main__":
	url = 'http://t3chfest.uc3m.es'
	scraping = Scraping()
	scraping.scrapingImagesPdf(url)
	scraping.scrapingBeautifulSoup(url)