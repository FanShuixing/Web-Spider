from selenium import webdriver
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
browser=webdriver.Chrome()
wait=WebDriverWait(browser,15)

def crawle(key,page):
	url='https://www.1688.com/'
	browser.get(url=url)
	button=browser.find_element_by_class_name('identity-cancel')
	button.click()
	input=browser.find_element_by_id('alisearch-keywords')
	input.send_keys(key)
	sea_button=browser.find_element_by_id('alisearch-submit')
	sea_button.click()
	button_1=browser.find_element_by_class_name('s-overlay-close-l')
	button_1.click()
	button_deal=browser.find_elements_by_css_selector('.sm-widget-sort.fd-clr.s-widget-sortfilt li')[1]
	button_deal.click()
	try:
		browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
		browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
		wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#offer60')))
	except :
		print('*'*30,'超时加载','*'*30,'\n\n\n')
		
	if page>1:
		for page in range(2,page+1):
			get_more_page(key,page)
	
def get_more_page(key,page):
	page_input=browser.find_element_by_class_name('fui-paging-input')
	page_input.clear()
	page_input.send_keys(page)
	button=browser.find_element_by_class_name('fui-paging-btn')
	button.click()
	try:
		browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
		browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
		wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#offer60')))
	except :
		print('*'*30,'超时加载','*'*30,'\n\n\n')
	for item in get_products():
		save_to_mongo(item,key)
		
def get_products():
	html=browser.page_source
	doc=pq(html)
	items=doc('.sm-offer .fd-clr .sm-offer-item').items()
	index=0
	for item in items:
		index+=1
		print('*'*50)
		title=item.find('.s-widget-offershopwindowtitle').text().split('\n')
		title=' '.join(title)
		print(title)
		price_a=item.find('.s-widget-offershopwindowprice').text().split('\n')
		price=''.join(price_a[:2])
		deal=''.join(price_a[2:])
		#产品网址
		text=item.find('.s-widget-offershopwindowtitle')
		soup=BeautifulSoup(str(text),'lxml')
		a=soup.select('.s-widget-offershopwindowtitle a')[0]
		url=a['href']
		
		yield{
		'title':title,
		'deal':deal,
		'price':price,
		'url':url}
	print('	(●ˇ∀ˇ●)	'*5)
	print('一共%d条数据'%index)
	
import pymongo
client=pymongo.MongoClient()
db=client.alibaba
def save_to_mongo(item,key):
	#根据关键字动态存入相应的表
	collection=db[key]
	if item:
		collection.insert(item)
		print('成功存储到mongo')
	
def main():
	key_words=input('请输入想查询的类别:(ps:请用空格隔开)').split(' ')
	page=int(input('你想查询多少页的数据：'))
	for key in key_words:
		crawle(key,page)
		for item in get_products():
			save_to_mongo(item,key)

			
main()