# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv
os.chdir("E:/爬虫数据")

class TenxuPipeline(object):
	def __init__(self):
		self.writer=csv.writer(open("tenxu_job.csv",'w'))
		self.writer.writerow(['职位名称','招聘人数','发布时间','发布城市','网址'])
		
	def process_item(self, item, spider):
		# print("阿三地方就")
		# print(item['title'])
		list=[item['title'],item['person_num'],item['time'],item['city'],item['url']]
		print("pipeline list:",list)
		self.writer.writerow(list)
	
		
