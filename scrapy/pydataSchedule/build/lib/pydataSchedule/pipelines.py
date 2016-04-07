# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy import signals
from scrapy.exporters import XmlItemExporter
#from pony.orm import *
import codecs
import json
import csv

'''db = Database("sqlite", "pydataSchedule.sqlite", create_db=True)

class PyDataSession(db.Entity):
        """
        Pony ORM model of the pydata session table
        """
	id = PrimaryKey(int, auto=True)
	speaker = Required(str)
	talk = Required(str)
	description = Required(str)
	date = Required(str)'''

'''class PyDataSQLitePipeline(object):

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline
		
	def spider_opened(self, spider):
		
		db.generate_mapping(check_tables=True, create_tables=True)

	def spider_closed(self, spider):
		db.commit()
		 
	# Insert data in database
	@db_session
	def process_item(self, item, spider):
                # use db_session as a context manager
                with db_session:
                        try:
				
                                strSpeaker = str(item['speaker']).decode('utf-8')
                                strTalk = str(item['talk']).decode('utf-8')
                                strDescription = str(item['description']).decode('utf-8')
                                strDate = str(item['time']).decode('utf-8')
				
                                pydata_session = PyDataSession(speaker=strSpeaker,talk=strTalk,description=strDescription,date=strDate)

			
                        except Exception, e:
                                print "Error al procesar los items en la BD %s: %s" % (e.args[0], e.args[1])

                        return item'''


class PyDataXmlExport(object):
	
	def __init__(self):
		self.files = {}

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

	def spider_opened(self, spider):
		file = open('pydata_items.xml', 'w+b')
		self.files[spider] = file
		self.exporter = XmlItemExporter(file)
		self.exporter.start_exporting()

	def spider_closed(self, spider):
		self.exporter.finish_exporting()
		file = self.files.pop(spider)
		file.close()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item
	
class PyDataJSONPipeline(object):	
	def __init__(self):
		self.file = codecs.open('pydata_items.json', 'w+b', encoding='utf-8')

	def process_item(self, item, spider):
		line = json.dumps(dict(item), ensure_ascii=False,indent=4) + "\n"
		self.file.write(line.decode('utf-8'))
		return item

	def spider_closed(self, spider):
		self.file.close()

class PydataschedulePipeline(object):
	def process_item(self, item, spider):
		return item
