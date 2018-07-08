import csv,os
import lxml.html
import urllib.request
import re,os
import urllib.parse
import pickle
from urllib.parse import quote
from html.parser import HTMLParser
'''
用于缓存
'''
				
class Downloader:
	def	__init__(self,cache):
		self.cache=cache
		
	def __call__(self,url):
		result=None
		if self.cache:
			
			try:
				
				result=self.cache[url]
				print("已调入数据")
				
			except:
				pass
		if result==None:
			print("未能调取\t"+url)
			result=self.download(url)
			if self.cache:
				print(type(url))
				self.cache[url]=result
		return result
		
	def download(self,url,num_retry=2):
		headers={'User-agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)'}
		url=quote(url, safe='/:?=')
		request=urllib.request.Request(url,headers=headers)
		print('正在下载: '+str(url))
	
		try:
		
			html=urllib.request.urlopen(request).read()
			html=html.decode('utf-8')
			
		except urllib.error.HTTPError as e:
			if num_retry>0:
				if hasattr(e,'code') and 500<=e.code<600:
					download(url,num_retry=num_retry-1)
				else:
					html=None     #当页面出现4xx Not found错误时应当返回None，不然会出错
			else:html=None
		return(html)
				
		
	
class DiskCache:
	def __init__(self,cache_dir='Cache'):
		self.cache_dir=cache_dir
	def __getitem__(self,url):
		path=self.url_to_path(url)
		if os.path.exists(path):
			with open(path,'rb') as fp:
				return pickle.load(fp)
		
	def __setitem__(self,url,result):
		path=self.url_to_path(url)
		folder=os.path.dirname(path)
		if  not os.path.exists(folder):
			os.makedirs(folder)
		with open(path,'wb') as fp:
			fp.write(pickle.dumps(result))
			
	def url_to_path(self,url):
		components=urllib.parse.urlsplit(url)
		path=components.path
		if not path:   #即path为空
			path='nihao'
		elif path.endswith('/'):
			path+='index.html'
		filename=components.netloc+path+components.query
		filename=re.sub('[^/0-9a-zA-Z\-.,;_]','_',filename)
		filename='/'.join(segment[:255] for segment in filename.split('/'))
		return(os.path.join(self.cache_dir,filename))
		

			
			
if __name__=='__main__':
	a=Downloader(DiskCache())
	a.download('https://book.douban.com/subject/1059336/')
