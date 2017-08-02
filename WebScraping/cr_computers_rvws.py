# Selenium Script: Gather Reviews from Site
# ===========================================

# Website we want to scrape is: https://www.verizonwireless.com/smartphones/samsung-galaxy-s7/
# The documentatio of selenium is here: 
#  * http://selenium-python.readthedocs.io/index.html
#  * http://selenium-python.readthedocs.io/getting-started.html
#  * Simple Exmaple:
#    * https://gist.github.com/hugs/830011

# for the presentation on this:  https://www.pinterest.com/explore/presentation/?lp=true

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
import pandas as pd
import re
from datetime import datetime

startTime = re.split('[\s+|\.]', str(datetime.now()))

# content to block ads slowing this process down could go here:
# https://stackoverflow.com/questions/16800689/running-selenium-webdriver-using-python-with-extensions-crx-files

# Windows users need to specify the path to chrome driver you just downloaded.
# driver = webdriver.Chrome('path\to\where\you\download\the\chromedriver')
driver = webdriver.Chrome()
driver.maximize_window()      # // For maximizing window
# driver.implicitly_wait(10)  # // gives an implicit wait for x seconds (did not help)

# leveraging code from our scrapy project:
# how do we iterate over all our previously captured URLS? --

# used in early testing
test_urls1 = ["http://www.consumerreports.org/products/laptop/acer-spin-5-sp513-51-55zr-388098/user-reviews", 
 			"http://www.consumerreports.org/products/chromebooks/acer-chromebook-c810-t7zt-383569/user-reciews", 
			"http://www.consumerreports.org/products/desktop-computer/hp-envy-750-514-389328/user-reviews"]

# used in early testing
test_urls = ["https://www.consumerreports.org/products/laptop/apple-macbook-air-13-inch-mjve2ll-a-374086/user-reviews#user-reviews",
			"https://www.consumerreports.org/products/chromebooks/acer-chromebook-c810-t7zt-383569/user-reviews#user-reviews"]

### code to setup interaction with csvs in and out ############
url_list_csv = "./cr_computers/cr_reviewPageURLs_AllComputers.csv"
urls_df = pd.read_csv(url_list_csv)

start_urls = []   # urls to be added from dataframe generated from silineum

for index, row in urls_df.iterrows():
	# test_urls.append(row['url'] + "specs")
	start_urls.append(row['url'] + "user-reviews#user-reviews")    # add all urls from df to start_urls

print("csv url 1: ", start_urls[0], sep="")
print("csv url 2: ", start_urls[1], sep="")
print("Number urls: ", len(start_urls), sep="")

csv_file  = open('cr_computer_NoRvws.csv', 'w')
csv_file2 = open('cr_computer_rvws.csv', 'w')
# Windows users need to open the file using 'wb'

writer = csv.writer(csv_file)
writer2 = csv.writer(csv_file2)
writer.writerow( ['brand', 'model', "prod_class", "prod_short_descr", "has_reviews", 'url', 'reported_exceptions'] ) 
writer2.writerow(['brand', 'model', "prod_class", "prod_short_descr",
	"num_usr_reviews", "rec_rvw_rating", "has_reviews", "survey_cons", "survey_pros", "ratings_distribution",
	"user_rating", "user_rating_txt", 
	"user_rvw_hdln", "submit_dateTime", "submit_date", "submit_time",
	"rvw_username", "rvw_userLocation", "rvw_userCity", "rvw_userState", "rvw_userCountry",
	"verified_buyer", "verified_reviewer", "user_review_content", "btm_line_txt",	
	'url', 'reported_exceptions']) 

###################################################################

# Page index used to keep track of where we are.
index = 1
# nan_count = 0
no_rvw_count = 0
all_rvw_count = 0
wde_count = 0
reported_exceptions = ""   # global variable but gets reset for each page / csv record row
vw_uLocal_tmp = []

def log_reported_exceptions(descr_string, ee):
	global reported_exceptions
	reported_exceptions += descr_string + ": " + str(type(ee)) + "/n"

for url in start_urls:  #  True to run,  set to index < 10 or something to test
	try:
		driver.get(url)
		print("Scraping Page number " + str(index))
		print("Current url: " + url)

		# get the html to load by activitating "Reviews" tab link
		button_xpath = '//*[@id="user-reviewsanchor"]'
		print("Attempting To Click Load Button: ", button_xpath)
		try:
			button = driver.find_element_by_xpath(button_xpath)
			# full path excerpt:  .get_attribute('href') #  href="javascript:void(0)">
			# time.sleep(3)
			button.click()
			# time.sleep(2)

		except WebDriverException as wde:
			# path to exception: selenium.common.exceptions
			# this seemed to work in verizon test even though it does not make sense
			# if data is missing on real attempt, then we can look into wait / exception cases
		
			print("TabATagClick code Problem: You have encountered a WebDriverException:")
			print(wde)
			print(type(wde))
			index = index + 1
			wde_count =+ 1.    # simple count tells us how many times this happened at end of process
			continue

		# Find all the product review records:
		wait_review = WebDriverWait(driver, 5)
		reviews = wait_review.until(EC.presence_of_all_elements_located((By.XPATH,
			'//div[@class="col-lg-12 col-md-12 col-sm-12 col-xs-12"]')))

		# old code:
		# reviews = driver.find_elements_by_xpath('//div[@class="col-lg-12 col-md-12 col-sm-12 col-xs-12"]')

		# Get Header of page Info So we Know What Product Each Record Belongs To
		print("Creating reviewHead ...")
		reviewsHead = driver.find_element_by_xpath('//div[@class="product-model-name-container"]')  # //body
		# print(reviewsHead[0])
		# print(len(reviewsHead))

		# mainHead =  reviewsHead # reviewsHead[0]
		# model = mainHead.find_element_by_xpath('.//div[@class="product-model-name-container"]/h1').text
		model = reviewsHead.find_element_by_xpath('.//h1').text
		model = model.strip()
		# brand = mainHead.find_element_by_xpath('.//div[@class="product-model-name-container"]//strong').text
		brand = reviewsHead.find_element_by_xpath('.//strong').text

		prod_class = url.split('/')[4]

		reviewsHdrDescr = driver.find_element_by_xpath('//div[@class="product-model-description-section"]')
		prod_short_descr = reviewsHdrDescr.find_element_by_xpath('.//div[@class="product-model-short-description"]/p').text

		print("Brand: ", brand)
		print("Model: ", model)
		print("prod_class: ", prod_class)

		# is reviews right?  debug test statement:
		print("======================"*5)
		print(reviews[0])
		print(len(reviews))
		print("======================"*5)

		# does this page have reviews?
		review = reviews[2]   # note: reviews[2].find_element ... did not work
		reported_exceptions = ""      # re-initializing 
		                      #              when exception encountered anywhere in code, add type value here
		                      #              so we can see which records are 'breaking' and why
		                      #              highlights inconsistencies in tagging of site pages to fix xpaths
		                      #              builds list within each record that had a problem

		try:
			writeRvwMsg = review.find_element_by_xpath('.//a[@class="pr-snippet-write-review-link"]').text
		except Exception as ee:
			print(ee)
			print(type(ee))
			## assumes that if tags are not right ... then tags are missing and no reviews exist
			## this will be validated by spot checking urls it applies to from error log included in output csv
			log_reported_exceptions("writeRvwMsg Step: ", ee)
			writeRvwMsg == "Write the First Review"

		print("writeRvwMsg: " + writeRvwMsg) 

		if writeRvwMsg == "Write the First Review":
			print("No Reviews to record!")
			num_usr_reviews = 0
			rec_rvw_rating = np.nan
			has_reviews = False

			# not used ... update with more fields if we use this in the future
			user_rating = np.nan
			user_rating_txt = np.nan
			user_rvw_hdln = np.nan
			submit_date = np.nan
			rvw_username = np.nan
			rvw_userLocation = np.nan
			verified_buyer = np.nan
			verified_reviewer = np.nan
			user_review_content = np.nan
			btm_line_txt = np.nan

			# Create Dictionary and Write It To File(s):
			# --------------------------------------------
			# outputting these records to own table as sanity check ... can spotcheck URLs for records missed
			# Don't really need records with no reviews

			review_dict = {} 

			review_dict['brand'] = brand
			review_dict['model'] = model
			review_dict['prod_class'] = prod_class
			review_dict['prod_short_descr'] = prod_short_descr  # product advertising banner description (top of the page)
			review_dict['has_reviews'] = has_reviews
			review_dict['url'] = url
			review_dict['reported_exceptions'] = reported_exceptions			

			writer.writerow(review_dict.values())
			index += 1
			no_rvw_count +=1

			# bug fix: re-initialize after writing each row so we don't pick up error from previous row in exception_report
			reported_exceptions = "" 

		else:             # writeRvwMsg should == "Write A Review"
			print("Reviews Found:")
			# <span class="pr-snippet-review-count"                       # example: "6 reviews"
			# <div aria-hidden="true" class="pr-snippet-rating-decimal"   # example rating: 4.8

			try:
				num_usr_reviews = review.find_element_by_xpath('.//span[@class="pr-snippet-review-count"]').text
				num_usr_reviews = int(num_usr_reviews.split()[0])
				rec_rvw_rating = review.find_element_by_xpath('.//div[@class="pr-snippet-rating-decimal"]').text   # OVERALL RATING: out of 5			
				rec_rvw_rating = float(rec_rvw_rating)
			except Exception as ee:
				print("Warning: Number of user reviews not found.")
				log_reported_exceptions("Num User Rvws and / or rec rvw rtng Not Found: ", ee)

			has_reviews = True

			try:
				ratings_distribution = review.find_element_by_xpath('.//ul[@class="pr-ratings-histogram pr-histogram-list"]').text
				ratings_distribution = re.sub('Stars\n', 'Stars ', ratings_distribution)
			except Exception as ee:
				print("Warning: Ratings Distr ot Found", ee)

			print("Ratings Distr:")
			print("[[" + ratings_distribution + "]]")

			# survey_recoToFriend = driver.find_element_by_xpath('.//span[@class="pre-reco-value"]')  # fix in future iteration
			# print("Respondants Would Recomment To a Friend:")                                       # capture parent element in driver
			# print("[[" + survey_recoToFriend + "]]")                                                # then drill in with .//span ?

			try:
				survey_cons = review.find_element_by_xpath('.//section[@class="pr-review-snapshot-block pr-review-snapshot-block-cons"]').text
				survey_cons = re.sub(r'(\d+)', r'\1 ', survey_cons)
				survey_pros = review.find_element_by_xpath('.//section[@class="pr-review-snapshot-block pr-review-snapshot-block-pros"]').text
				survey_pros = re.sub(r'(\d+)', r'\1 ', survey_pros)
			except Exception as ee:
				log_reported_exceptions("Warning: Survey Pro or Con Not Found ", ee)

			print("Survey Overview: Pros:")
			print("[[" + survey_pros + "]]")
			print("Survey Overview Cons:")
			print("[[" + survey_cons + "]]")

			user_review_articles = review.find_elements_by_xpath('.//article[@class="pr-review"]')
			for ind, article in enumerate(user_review_articles):
				# note:  CHILD RECORDS BEGIN HERE:

				# next version notes:
				#  * can capture descriptive blurb of whole product at top of web page (js integration not required)
				#  * can integrate spider logic about url to categorize records: laptop, desktop, chromebook

				has_reviews = True
				user_rating = article.find_element_by_xpath('.//header//div[@class="pr-snippet-rating-decimal"]').text
				user_rating = float(user_rating)
				# <section class="pr-review-snippet-container " ...// ... span[@ ...].  <span class="pr-accessible-text" 

				try:
					user_rating_txt = article.find_element_by_xpath('.//span[@class="pr-accessible-text"]').text
				except Exception as ee:
					print(ee)
					print(type(ee))
					print("Warning:  problem with user_rating_txt element - can't find it.")
					log_reported_exceptions("Error with user_rating_txt: ", ee)     ## fix this in future iteration of code (xpath works on chrome but not working here)

				user_rvw_hdln = article.find_element_by_xpath('.//header//h2[@class="pr-rd-review-headline"]').text

				# <section class="pr-rd-description pr-rd-content-block" ... <time datetime="2017-05-17T18:11:30.681Z" ...
				#                                                        ... <p class="pr-rd-details pr-rd-author-nickname" 
				# section ... <p class="pr-rd-details pr-rd-author-location" => has span and text of auhor from? location
				submit_dateTime = article.find_element_by_xpath('.//section//time').get_attribute('datetime')
				## just in case need different formats, probably easier to do it here than later:
				### "submit_dateTime", "submit_date", "submit_time"

				print(submit_dateTime)

				submit_date = submit_dateTime[:-1].split('T')
				submit_time = submit_date[1]
				submit_date = submit_date[0]

				rvw_username = article.find_element_by_xpath('.//section//p[@class="pr-rd-details pr-rd-author-nickname"]').text
				rvw_username = re.sub('^By ', '', rvw_username)
				rvw_userLocation = article.find_element_by_xpath('.//section//p[@class="pr-rd-details pr-rd-author-location"]').text
				rvw_userLocation = re.sub('^From ', '', rvw_userLocation)

				# initialize so no errors if userLocation not split:
				rvw_userCity  = np.nan
				rvw_userState = np.nan
				rvw_userCountry = np.nan

				## create new location fields in case needed for analysis:
				rvw_uLocal_tmp = rvw_userLocation.split(",")
				if len(rvw_uLocal_tmp) == 1:
					rvw_userState = rvw_uLocal_tmp[0]
					rvw_userCountry = "USA"          # default if no country
				elif len(rvw_uLocal_tmp) >= 2:
					rvw_userCity  = rvw_uLocal_tmp[0]
					rvw_userState = rvw_uLocal_tmp[1]
					rvw_userCountry = "USA"          # default if no country
				if len(rvw_uLocal_tmp) >= 3:
					rvw_userCountry = rvw_uLocal_tmp[2]
				if len(rvw_uLocal_tmp) >= 4:         # replace w/ country if present
					reported_exceptions =+ "<<warning: rvw_userLocation had more than 3 elements>>"

				# bug fix:
				if rvw_userState.lower() == "usa":
					rvw_userCountry = "USA"
					rvw_userState = np.nan

				# section ... <svg viewBox="0 0 19 19" ... <title data-reactid-powerreviews=  => verified buyer?  # not used: svg[@viewBox] [@data-reactid-powerreviews]
				# section ... aside ... // <span class="pr-rd-badging-text"   = verified reviewer?
				# <section class="pr-rd-description pr-rd-content-block" ..> / <p class="pr-rd-description-text"  => should be review content

				try:
					verified_buyer = article.find_element_by_xpath('.//section//title').text
				except Exception as ee:
					print("Warning: verified_buyer not found")
					verified_buyer = np.nan
					log_reported_exceptions("Verified Buyer Not Found: ", ee)

				try:
					verified_reviewer = article.find_element_by_xpath('.//section//aside//span[@class="pr-rd-badging-text"]').text
				except Exception as ee:
					print("Warning: verified_reviewer not found")
					log_reported_exceptions("Verified Reviewer Not Found: ", ee)
					verified_reviewer = np.nan 

				try:	
					user_review_content = article.find_element_by_xpath('.//section/p[@class="pr-rd-description-text"]').text
				except Exception as ee:
					print("Warning: Review Content missing!")
					log_reported_exceptions("Content Missing!!! --> ", ee)
					user_review_content = np.nan 

				# <footer ...<span [2] => bottom line text
				btm_line_txt = article.find_element_by_xpath('(.//footer//span)[2]').text

				# Create Dictionary and Write It To File(s):
				# --------------------------------------------

				review_dict2 = {}

				review_dict2['brand'] = brand
				review_dict2['model'] = model
				review_dict2['prod_class'] = prod_class
				review_dict2['prod_short_descr'] = prod_short_descr  # product advertising banner description (top of the page)
				review_dict2['num_usr_reviews'] = num_usr_reviews
				review_dict2['rec_rvw_rating'] = rec_rvw_rating
				review_dict2['has_reviews'] = has_reviews
				review_dict2['survey_cons'] = survey_cons
				review_dict2['survey_pros'] = survey_pros
				review_dict2['ratings_distribution'] = ratings_distribution

				review_dict2['user_rating'] = user_rating 
				review_dict2['user_rating_txt'] = user_rating_txt 
				review_dict2['user_rvw_hdln'] = user_rvw_hdln 

				review_dict2['submit_dateTime'] = submit_dateTime
				review_dict2['submit_date'] = submit_date
				review_dict2['submit_time'] = submit_time 
				
				review_dict2['rvw_username'] = rvw_username 
				review_dict2['rvw_userLocation'] = rvw_userLocation 

				review_dict2['rvw_userCity'] = rvw_userCity
				review_dict2['rvw_userState'] = rvw_userState
				review_dict2['rvw_userCountry'] = rvw_userCountry

				review_dict2['verified_buyer'] = verified_buyer 
				review_dict2['verified_reviewer'] = verified_reviewer 
				review_dict2['user_review_content'] = user_review_content 
				review_dict2['btm_line_txt'] = btm_line_txt 
				review_dict2['url'] = url	
				review_dict2['reported_exceptions'] = reported_exceptions		

				writer2.writerow(review_dict2.values())
				# bug fix: re-initialize after writing each row so we don't pick up error from previous row in exception_report
				reported_exceptions = ""

				# other variables should re-initialize before next iteration as well as precaution
				num_usr_reviews = np.nan
				rec_rvw_rating = np.nan
				has_reviews = np.nan
				survey_cons = np.nan
				survey_pros = np.nan
				ratings_distribution = np.nan

				user_rating = np.nan
				user_rating_txt = np.nan
				user_rvw_hdln = np.nan

				submit_dateTime = np.nan
				submit_date = np.nan
				submit_time = np.nan
				
				rvw_username = np.nan
				rvw_userLocation = np.nan

				rvw_userCity = np.nan
				rvw_userState = np.nan
				rvw_userCountry = np.nan

				verified_buyer = np.nan
				verified_reviewer = np.nan
				user_review_content = np.nan
				btm_line_txt = np.nan

				# testing print statements (useful so left in)

				print("Article ", ind, ") User Fields:", sep="")
				print("user_rating: ", user_rating, sep="")
				print("user_rating_txt: ", user_rating_txt, sep="")   # Tested to here ...
				print("==============="*3)
				print("user_rvw_hdln: ", user_rvw_hdln, sep="")

				print("btm_line_txt: ", btm_line_txt, sep="")
				print("submit_date: ", submit_date, sep="")
				print("rvw_username: ", rvw_username, sep="")
				print("rvw_userLocation: ", rvw_userLocation, sep="")
				print("verified_buyer: ", verified_buyer, sep="")
				print("vverified_reviewer: ", verified_reviewer, sep="")
				print("CONTENT: ")
				print(user_review_content)

				index += 1
				all_rvw_count += 1

				# print("xxx: ", uxxx, sep="")

		print("Num Reviews: " + str(num_usr_reviews))
		print("User Rating: " + str(rec_rvw_rating))
		print("Running tallies: ")
		print("\t" + "Review Recs: " + str(all_rvw_count))
		print("\t" + "Recs w/ No Reviews: " + str(no_rvw_count))

		### sample code other scripts ...
		# .replace(r'[\$\.\,]', r'', regex=True).astype(float, coerce=True)
		# re.sub(r'[\s\()-]+', '_', spec_label)

		# break
		# break
		
		# print("nan_count: ", nan_count, sep="")

			# Test content:
			# for ind, review in enumerate(reviews):
			# 	print("iteration: " + str(ind))
			# 	print(review)

				# Test block:  Used to idenfity where content lived page: review 0, review 1, ... review 3				
				# try:
				# 	# print(review.find_element_by_xpath('./h2').text)  # ind = 2, has "user reviews"
				# 	# print("a tag content at pos(: ", ind, "): ", review.find_element_by_xpath('.//a[@class="pr-snippet-write-review-link"]').text, sep="")
				# 	# print("tag at pos (", ind, "): ", review.find_elements_by_xpath('.//article[@class="pr-review"]'), sep="") # found @ ind 2
				# except Exception as ex1:
				# 	print("Article not found Exception at ind: " + str(ind))
				# 	print(ex1)
				# 	print(type(ex1))

	except Exception as e:
		print(e)
		print(type(e))		
		csv_file.close()
		csv_file2.close()
		driver.close()
		print("wde_count: " + str(wde_count))  # tell us how many times the webdriver code that makes page access triggered exception handling
		                                       # note: this is for research and debugging, not sure if positive count truly indicates trouble
		endTime = re.split('[\s+|\.]', str(datetime.now()))
		print("Script Start / End Times:")
		print(startTime)
		print(endTime)
		break

# what if no exception to end the program ... 
# first noticed this when my start/end time did not ptint
# repeating termination code for normal end to code:
csv_file.close()
csv_file2.close()
driver.close()
print("wde_count: " + str(wde_count))  # tell us how many times the webdriver code that makes page access triggered exception handling
                                       # note: this is for research and debugging, not sure if positive count truly indicates trouble
endTime = re.split('[\s+|\.]', str(datetime.now()))
print("Script Start / End Times:")
print(startTime)
print(endTime)