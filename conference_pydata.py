import requests
import lxml.html
req = requests.get('http://pydata.org/madrid2016/schedule/')
tree = lxml.html.fromstring(req.text)
for tr in tree.xpath('//td[@class="slot slot-talk"]'):
    speakers = tr.xpath('//span[@class="speaker"]/text()')
    urls = tr.xpath('//span[@class="title"]//@href')
    talks = tr.xpath('//span[@class="title"]//a/text()')

index_speaker=0
for speaker in speakers:
    print speaker.strip()
    print urls[index_speaker]
    print talks[index_speaker]
    details =requests.get('http://pydata.org/'+urls[index_speaker])
    tree = lxml.html.fromstring(details.text)
    description = tree.xpath('//div[@class="description"]//p/text()')[0]
    print description.encode("utf-8")
    hour = tree.xpath('//div[@class="col-md-8"]//h4/text()')[0].replace("\n","").strip()
    print hour.encode("utf-8")
    
    index_speaker=index_speaker+1
    print "---------------------\n"
