# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from Naruto.settings import IMAGE_STORE
import os 
import requests
class NarutoPipeline(object):
	def process_item(self, item, spider):
		print('item pipeline',item)
		if 'img_url' in item:
			# print("YES!!")
			images=[]
			img_path='%s/%s'%(IMAGE_STORE,item['dir_name'])
			
			if not os.path.exists(img_path):
				os.makedirs(img_path)
				
			for img_url in item['img_url']:
				houzhui = img_url.split('/')[-1].split('.')[-1]
				qianzhui = img_url.split('/')[-1].split('.')[0]
                #图片名
				image_file_name = '第' + qianzhui + '页.' + houzhui
				print('name\t',image_file_name)
				file_name='%s/%s'%(img_path,image_file_name)
				if os.path.exists(file_name):
					continue
				with open(file_name,'wb') as f:
					response=requests.get(url=img_url)
					for block in response.iter_content(1024):
						if not block :
							break
						f.write(block)
			item['img_path']=images
		return item

			
			