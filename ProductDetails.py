from lxml import html
import csv, os, json
import requests
from requestsexceptions import *
from time import sleep
import sys
import pyodbc

def AmzonParser(url):
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
	page = requests.get(url,headers=headers)
	data = {}
	while True:
		try:
			doc = html.fromstring(page.content)
			XPATH_NAME = '//h1[@id="title"]//text()'
			XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
			XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
			XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
			XPATH_AVAILABILITY = '//div[@id="availability"]//text()'

			RAW_NAME = doc.xpath(XPATH_NAME)
			RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
			RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
			RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
			RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)

			NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
			SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
			CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
			ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
			AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
			URL = url
			if not ORIGINAL_PRICE:
				ORIGINAL_PRICE = SALE_PRICE

			if page.status_code!=200:
				raise ValueError('captha')
			data['NAME'] = NAME
			data['SALE_PRICE'] = SALE_PRICE
			data['CATEGORY'] =CATEGORY
			data['ORIGINAL_PRICE'] = ORIGINAL_PRICE
			data['AVAILABILITY']  = AVAILABILITY
			data['URL'] = url

			return data
		except Exception as e:
			print(e)

def ReadAsin(i):


		url = "http://www.amazon.com/dp/"+i
		print("Processing: "+url)
		extracted_data= AmzonParser(url)
		if extracted_data['NAME'] != None:
				print(extracted_data)
				#include below commented code to write the scrapped data into a csv file
				''' 
				with open('ProductList.csv', 'a', newline='', encoding='utf-8') as csvfile:
					fieldnames = ['Name and Description', 'Sale Price', 'Category', 'Original Price', 'Availability','URL']
					writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
					writer.writerow(
						{'Name and Description': extracted_data['NAME'], 'Sale Price': extracted_data['SALE_PRICE'],
						 'Category': extracted_data['CATEGORY'],
						 'Original Price': extracted_data['ORIGINAL_PRICE'],
						 'Availability': extracted_data['AVAILABILITY'], 'URL': extracted_data['URL']})
				'''

				#write data into an mssql database
				try:
					cnxn = pyodbc.connect(r'DRIVER={SQL Server}; SERVER=.\SQLEXPRESS; DATABASE=test;')
					cursor = cnxn.cursor()

					cursor.execute("insert into [ProductList] values ('{0}','{1}','{2}','{3}','{4}','{5}')".format(
						extracted_data['NAME'], extracted_data['SALE_PRICE'],
						extracted_data['CATEGORY'],
						extracted_data['ORIGINAL_PRICE'],
						extracted_data['AVAILABILITY'], extracted_data['URL']))
					cnxn.commit()
					cnxn.close()

				except:
					print(str(sys.exc_info()))



if __name__ == "__main__":
    ReadAsin()