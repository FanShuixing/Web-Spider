# -*- coding: utf-8 -*-
import scrapy
import re
from Naruto.items import NarutoItem
class ComicSpider(scrapy.Spider):
	name = 'comic'

	def __init__(self):
		self.root_url='http://comic.kukudm.com'
		self.allowed_domains = ['comic.kukudm.com']
		self.start_urls = ['http://comic.kukudm.com/comiclist/3/']
		self.root_img_url='http://n5.1whour.com/'

	def parse(self, response):
		dir_link=response.xpath("//dd/a[1]/@href").extract()
		dir_name=response.xpath("//dd/a[1]/text()").extract()
		items=[]
		for index in range(len(dir_link)):
			# print(self.root_url+dir_link[index])
			item=NarutoItem()
			item['dir_name']=dir_name[index]
			item['dir_link']=self.root_url+dir_link[index]
			
			# print(item)
			items.append(item)
		for item in items[:2]:
			print("正在parse中")
			yield scrapy.Request(url=item['dir_link'],meta={'item':item},callback=self.parse1)
			
	def parse1(self,response):
		print("prase1")
		item=response.meta['item']
		
		img_url= response.xpath('//script/text()').re('\+"(.*?)\'><span')[0]
		# print('img_url:',img_url)
		img_url=[self.root_img_url+img_url]
		# print("img_url:",img_url)
		item['img_url']=img_url
		# print("dir_link:",item['dir_link'])
		
		yield item
		# print("nihao")
		pag_num=response.xpath('//td/text()').re('共(.*?)页')[0]
		# print("%s页"%pag_num)
		for index in range(2,int(pag_num)+1):
			new_url=re.sub('/(\d+).htm','/%d',item['dir_link'])%index
			new_url=new_url+'.htm'
			# print('new_url',new_url)
			# print("pase1中的item:",item)
			yield scrapy.Request(url=new_url,callback=self.parse2,meta={'item':item})
			# print("pase1中的item:",item)
			
	def parse2(self,response):
		print("parse2 进行中")
		# print("pase2中的item:",item)
		item=response.meta['item']
		img_url= response.xpath('//script/text()').re('\+"(.*?)\'><span')[0]
		img_url=self.root_img_url+img_url
		item['img_url']=[img_url]
		# print("parse2 中的img_url:",img_url)
		yield item