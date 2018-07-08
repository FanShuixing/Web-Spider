from bs4 import BeautifulSoup
import urllib.request
import os
from urllib.request import urlretrieve
from novel_spider import DiskCache
from novel_spider import Downloader
os.chdir("E:/爬虫数据")
'''
爬取图片
'''

def download(url):
	'''
	下载页面
	'''
	headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
	print("正在下载中：",url)
	req=urllib.request.Request(url,headers=headers)
	html=urllib.request.urlopen(req).read()
	html=html.decode('utf-8')
	return html
	
def Buf(html):
	'''
	返回页面中的所有图片的url
	'''
	soup=BeautifulSoup(html,'lxml')
	soup=soup.find_all(class_='item-img')
	url_list=[]
	for each in soup:	
		url=each.get('href')
		url_list.append(url)
	return url_list
	


def Img_dow(html):
	if html:
		soup=BeautifulSoup(html,'lxml')
		soup=soup.find_all('div',class_='wr-single-content-list')
		soup=BeautifulSoup(str(soup),'lxml')
	# print(soup)
		a=soup.img.get('src')
		name=soup.img.get('alt')
		img_url='http://www.shuaia.net'+a
		if 'images' not in os.listdir():
			os.makedirs('images')
		try:
			urlretrieve(url=img_url,filename='images/'+'%s.jpg'%name) 
		except:
			print("下载失败")
		print("下载%s.jpj完成"%name)
	

def Scrapy():
	url_list=[]
	
	cache=DiskCache()
	D=Downloader(cache)
	for num in range(1,3):
		if num==1:
			url='http://www.shuaia.net/index.html'
		else:
			url='http://www.shuaia.net/index_%d.html' %num
		url_list.append(url)
	# print(url_list)
	for url in url_list:
		html=D(url)
		# html=download(url)
		img_list=Buf(html)
		# print(img_list)
		for img_url in img_list:
			# print(img_url)
			html=D(img_url)
			# html=download(img_url)
			Img_dow(html)
	
if __name__=="__main__":
	# url='http://www.shuaia.net/meinv/2018-04-16/14924.html'
	# html=download(url)
	# Img_dow(html)
	Scrapy()
