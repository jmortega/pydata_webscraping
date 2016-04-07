import mechanize
from bs4 import BeautifulSoup

def translate(home_language,target_language,text):
    text = text.replace(" ","%20");
    
    get_url = "https://translate.google.com/?sl="+home_language+"&tl="+target_language+"&text="+text
    #print get_url
    browser = mechanize.Browser()
    # Disable loading robots.txt
    browser.set_handle_robots(False)
    
    browser.addheaders = [('User-agent',
                     'Mozilla/4.0 (compatible; MSIE 5.0; Windows 98;)')]
    
    translated_text = browser.open(get_url)
    translated_text = translated_text.read().decode('UTF-8')
    
    soup = BeautifulSoup(translated_text, "lxml")
    div_content = soup.find('div', {'id' : 'gt-res-content'})
    converted_text = div_content.find('span', {'id':'result_box'}).text
    
    return converted_text    


print translate("en","es","hello world")