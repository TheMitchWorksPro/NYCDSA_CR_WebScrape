# THIS SCRIPT NOT USED IN FINAL PROJECT
# ===========================================
# This was starting code from which other selenium scripts were developed
# laptops script replaces this one ...

# Website we want to scrape is: https://www.verizonwireless.com/smartphones/samsung-galaxy-s7/
# The documentatio of selenium is here: 
#  * http://selenium-python.readthedocs.io/index.html
#  * http://selenium-python.readthedocs.io/getting-started.html
#### ADDS CAUSING PROBLEMS?  TRY:
# * https://stackoverflow.com/questions/16800689/running-selenium-webdriver-using-python-with-extensions-crx-files

# Please follow the instructions below to setup the environment of selenium
# Step #1
# Windows users: download the chromedriver from here: https://chromedriver.storage.googleapis.com/index.html?path=2.30/
# Mac users: Install homebrew: http://brew.sh/
#			 Then run 'brew install chromedriver' on the terminal
#
# Step #2
# Windows users: open Anaconda prompt and switch to python3 environment. Then run 'conda install -c conda-forge selenium'
# Mac users: open Terminal and switch to python3 environment. Then run 'conda install selenium'
#            # used alternate conda-forge path to install selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time
import csv
import numpy as np

# Windows users need to specify the path to chrome driver you just downloaded.
# driver = webdriver.Chrome('path\to\where\you\download\the\chromedriver')
driver = webdriver.Chrome()

driver.get("http://www.consumerreports.org/products/laptop/ratings-overview/")

csv_file = open('cr_reviewPageURLs.csv', 'w')
# Windows users need to open the file using 'wb'
# csv_file = open('reviews.csv', 'wb')

writer = csv.writer(csv_file)
writer.writerow(['prod_class', 'brand', 'product_title', 'price', 'url']) 

# Page index used to keep track of where we are.
index = 1
nan_count = 0

while index < 10:  #  True to run,  set to index < 10 or something to test
	try:
		print("Scraping Page number " + str(index))

		# Find all the product review records:
		reviews = driver.find_elements_by_xpath('//div[@class="bootstrap-table"]//tr[@class="row-border"]')

		# is reviews right?  debug test statement:
		print("======================"*5)
		print(reviews[5])
		print(len(reviews))
		print("======================"*5)
		# break
		# break

		for review in reviews:
			# Initialize an empty dictionary for each review
			review_dict = {}
			# Example: Use Xpath to locate the title, content, username, date.
			# Once you locate the element, you can use 'element.text' to return its string.
			# To get the attribute instead of the text of each element, use 'element.get_attribute()'

			# failed idea:
			# tempElem = review.find_element_by_xpath('.//div[@class="text-wrap"]/')
			# brand = tempElem.find_element_by_xpath('./a/strong').text
			# url = tempElem.find_element_by_xpath('./a').get_attribute('href')


			brand = review.find_element_by_xpath('.//div[@class="text-wrap"]/a/strong').text
			print("brand: ", brand, sep="")

			url = review.find_element_by_xpath('.//div[@class="text-wrap"]/a').get_attribute('href')
			print(url)

			product_title = review.find_element_by_xpath('.//div[@class="text-wrap"]/a/span').text
			print("product_title: ", product_title, sep="")

			try:
				# price = review.find_element_by_xpath('.//div[@class="model__model-meta"]/div[3]/a/span').text
				price = review.find_element_by_xpath('.//span[contains(@class, "product-model-price-container price-model legacy")]').text
			except Exception as ee:
				print(ee)
				print(type(ee))
				price = np.nan
				nan_count += 1

			print("price: ", price, sep="")			

			review_dict['prod_class'] = 'laptop'
			review_dict['brand'] = brand
			review_dict['product_title'] = product_title
			review_dict['price'] = price
			review_dict['url'] = url			

			writer.writerow(review_dict.values())
        
		# Locate the next button on the page.
		index = index + 1

		button = driver.find_element_by_xpath('//li[@class="page-next"]/a')
		         # full path excerpt:  .get_attribute('href') #  href="javascript:void(0)">

		try:
			time.sleep(2)
			button.click()
			time.sleep(2)
		except WebDriverException as wde:
			# path to exception: selenium.common.exceptions
			# this seemed to work in verizon test even though it does not make sense
			# if data is missing on real attempt, then we can look into wait / exception cases
		
			print("ButtonClick code Exception: You have encountered a WebDriverException:")
			print(wde)
			print(type(wde))
			index = index + 1
			continue

		print("nan_count: ", nan_count, sep="")

	except Exception as e:
		print(e)
		print(type(e))		
		csv_file.close()
		driver.close()
		break


	# Better solution using Explicit Waits in selenium: http://selenium-python.readthedocs.io/waits.html?highlight=element_to_be_selected#explicit-waits

	# try:
	# 	wait_review = WebDriverWait(driver, 10)
	# 	reviews = wait_review.until(EC.presence_of_all_elements_located((By.XPATH,
	# 								'//ol[@class="bv-content-list bv-content-list-Reviews bv-focusable"]/li')))
	# 	print(index)
	# 	print('review ok')
	# 	# reviews = driver.find_elements_by_xpath('//ol[@class="bv-content-list bv-content-list-Reviews bv-focusable"]/li')
	#
	# 	wait_button = WebDriverWait(driver, 10)
	# 	button = wait_button.until(EC.element_to_be_clickable((By.XPATH,
	# 								'//div[@class="bv-content-list-container"]//span[@class="bv-content-btn-pages-next"]')))
	# 	print('button ok')
	# 	# button = driver.find_element_by_xpath('//span[@class="bv-content-btn-pages-next"]')
	# 	button.click()
	# except Exception as e:
	# 	print(e)
	# 	driver.close()
	# 	break
