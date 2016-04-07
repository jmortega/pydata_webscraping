import mechanize
import cookielib

def create_browser():
    br = mechanize.Browser()           # Create basic browser
    cj = cookielib.LWPCookieJar()      # Create cookiejar to handle cookies
    br.set_cookiejar(cj)               # Set cookie jar for our browser
    br.set_handle_equiv(True)          # Allow opening of certain files
    br.set_handle_gzip(True)           # Allow handling of zip files
    br.set_handle_redirect(True)       # Automatically handle auto-redirects
    br.set_handle_referer(True)
    br.set_handle_robots(False)        # ignore anti-robots.txt
 
    # Necessary headers to simulate an actual browser
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'),
                   ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
                   ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
                   ('Accept-Encoding', 'gzip,deflate,sdch'),
                   ('Accept-Language', 'en-US,en;q=0.8,fr;q=0.6'),
                   ('Connection', 'keep-alive')
                  ]
    return br
	
url = "http://duckduckgo.com/html"
br = create_browser()
br.set_handle_robots(False) # ignore robots
br.open(url)
br.select_form(name="x")
br["q"] = "python"
res = br.submit()
for link in br.links():
	print link.url
content = res.read()
with open("mechanize_results.html", "w") as f:
    f.write(content)