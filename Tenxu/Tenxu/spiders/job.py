# -*- coding: utf-8 -*-
import scrapy
from Tenxu.items import TenxuItem

class JobSpider(scrapy.Spider):
	name = 'job'

	def __init__(self):
		self.allowed_domains = ['tencent.com']
		self.start_urls = ['https://hr.tencent.com/position.php?&start=']
		self.root_url='https://hr.tencent.com/'

	def parse(self,response):
		all_city=response.xpath('//a[@class="item"]/span/font/text() | //a[@class="item itemhide"]/span/font/text()').extract()[:19]
		all_city_url=response.xpath('//a[@class="item itemhide"]/@href | //a[@class="item"]/@href').extract()[:19]
		city_list=input("请输入待查询的城市名(ps:请用空格隔开,所有城市选择All)：").split(' ')
		# print(all_city,'\n\n',all_city_url)
		Falg=True
		if city_list[0]=="All":Falg=False
		if not Falg: city_list=all_city
		
		for each_city in city_list:
			item=TenxuItem()
			index=all_city.index(each_city)
			url=self.root_url+all_city_url[index]
			# print('url:',url)
			item['city']=all_city[index]
			item['url']=url
			# print("parse url:",url)
			yield scrapy.Request(url=url,meta={'item':item},callback=self.parse1)
			
	def parse1(self,response):
		item=response.meta['item']
		page_num=response.xpath('//div[@class="pagenav"]/a/text()').extract()[-2]
		
		for page in range(0,int(page_num)*10,10):
			page_url=item['url']+'&start=%d'%page
			print('page_url:',page_url)
			yield scrapy.Request(url=page_url,meta={'item':item},callback=self.parse2)
			
	def parse2(self,response):
		
		item=response.meta['item']
		#获取标题
		title=response.xpath("//td[@class='l square']/a/text()").extract()
		#获取每一页的链接
		url=response.xpath("//td[@class='l square']/a/@href").extract()
		#获取发布时间
		time=response.xpath("//tr[@class='odd']/td | //tr[@class='even']/td").re('\d+-\d+-\d+')
		#获取城市首页的页码数，根据页码数来爬取城市对应的所有职位
		person_num=response.xpath('//tr[@class="even"]/td | //tr[@class="odd"]/td').re('<td>(\d+)</td>')
		
		for index in range(len(title)):
			item['title']=title[index]
			new_url=self.root_url+url[index]
			item['url']=new_url
			item['time']=time[index]
			item['person_num']=person_num[index]
			yield item
		
		
	
		
