# -*- coding: utf-8 -*-
from cr_computers.items import CrComputersItem
import scrapy
import numpy as np
import pandas as pd
import re

class cr_computers(scrapy.Spider):
	name = "cr_computers"
	allowed_domains = ["http://www.consumerreports.org/"]
	# start_urls = []  # urls to be added from dataframe generated from silineum

    # test URLs:
	test_urls = ["http://www.consumerreports.org/products/laptop/acer-spin-5-sp513-51-55zr-388098/specs", 
 				"http://www.consumerreports.org/products/chromebooks/acer-chromebook-c810-t7zt-383569/specs", 
				"http://www.consumerreports.org/products/desktop-computer/hp-envy-750-514-389328/specs"]

	url_list_csv = "cr_reviewPageURLs_AllComputers.csv"
	urls_df = pd.read_csv(url_list_csv)

	start_urls = []   # urls to be added from dataframe generated from silineum

	for index, row in urls_df.iterrows():
		# test_urls.append(row['url'] + "specs")
		start_urls.append(row['url'] + "specs")    # add all urls from df to start_urls

	print("sample url: ", start_urls[0], sep="")
	print("Number urls: ", len(start_urls), sep="")

	def parse(self, response):
	# in scrapy shell ... test the url and try to get the data

		specs = response.xpath('//div[@class="product-model-spec-container"]//div[@class="row product-model-spec-item"]')

		for spec in specs:
			spec_value = spec.xpath('.//div[@class="col-lg-7 col-md-7 col-sm-6 col-xs-12 product-model-spec-item-value"]/text()').extract_first().strip()

			spec_label = spec.xpath('.//span[@class="product-model-spec-item-tooltip-text"]/strong/text()').extract_first().strip()
			spec_label = re.sub(r'[\s\()-]+', '_', spec_label)

			# model = response.xpath('//a[@class="product-model-eyebrow-link visible-xs"]/@data-modelname').extract_first()
			model = response.xpath('//div[@class="product-model-name-container"]/h1/text()').extract()[1].strip()
			# if model == "" or model == " " or model == np.nan:
			# 	model = "__NULL__"

			# brand = response.xpath('//a[@class="product-model-eyebrow-link visible-xs"]/@data-brandname').extract_first()
			brand = response.xpath('//div[@class="product-model-name-container"]//strong/text()').extract_first()
			# if brand == "" or brand == " " or model == np.nan:
			# 	brand = "__NULL__"

			prod_class = response.url.split('/')[4]            # request holds original URL passed into this function
			url = response.url

			item = CrComputersItem()
			item['prod_class'] = prod_class
			item['brand'] = brand 
			item['model'] = model
			item['spec_label'] = spec_label
			item['spec_value'] = spec_value
			item['url'] = url

			yield item
