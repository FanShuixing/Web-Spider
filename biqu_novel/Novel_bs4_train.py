import urllib.request
from bs4 import BeautifulSoup
import os
from novel_spider import Downloader
from novel_spider import DiskCache
import urllib.parse
os.chdir("E:/爬虫数据")
'''
用BeautifulSoup爬取的笔趣网的小说
采用了缓存
'''

def download(url):
	
	print("正在下载：",url)
	head={}
	head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
	req=urllib.request.Request(url,headers=head)
	html=urllib.request.urlopen(req).read()
	html=html.decode('gbk')
	# print(html)
	return html
	
def Content(html):
	'''
	提取网页中的文本
	'''
	soup_text=BeautifulSoup(html,'lxml')
	soup_text=soup_text.find_all(id='content')
	soup_text=BeautifulSoup(str(soup_text),'lxml')
	content=soup_text.div.text.replace('\xa0','')
	# print(content)
	return content
	
def Scrapy(download_url,cache):
	fr=open("大道朝天.txt",'w')
	root_html=download(download_url)
	soup=BeautifulSoup(root_html,'lxml')
	soup=soup.find_all('div',id='list') 
	chapter_soup=BeautifulSoup(str(soup),'lxml')
	#实现缓存
	cache=DiskCache()
	D=Downloader(cache)
	for each in chapter_soup.dl.children:
		# print(each)
		if each!='\n':
			if each.a!=None:
				name=each.a.string
				short_url=each.a.get('href')
				
				new_url=urllib.parse.urljoin(download_url,short_url)
				new_html=D(new_url)
				fr.write(name+'\n\n')
				
				text=Content(new_html)
				fr.write(text)
				fr.write("\n\n")
	fr.close()
	
	
if __name__=="__main__":
	# url='http://www.biquge.com.tw/18_18949/8702198.html'
	# html=download(url)
	# Content(html)
	Scrapy('http://www.biquge.com.tw/18_18949',DiskCache())