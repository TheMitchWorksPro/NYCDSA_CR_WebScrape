# NYCDSA_CR_WebScrape

## About This Project And Presentation Content Files

NYC DSA WebScraping Project - Mitch

This project scrapes desktop computer, laptop computer, and Google Chromebook reviews off the Consumer Reports (CR) website.  The presentation for this project can be found here

- [First part of Presentation - PDF](https://github.com/TheMitchWorksPro/NYCDSA_CR_WebScrape/blob/master/Adventures%20in%20Data%20Munging.pdf) - includes CR reviews word clouds.
- [Second Part - Review of Analysis Jupyter Notebook (as HTML)](http://htmlpreview.github.io/?https://github.com/TheMitchWorksPro/NYCDSA_CR_WebScrape/blob/master/TMWP_CR_Spec_TableAnalysis1.html) - has graphs and analysis of CR specification data
- \<blog coming soon\> - Content to tie this all together, talk about the process and updated positive reviews word cloud

## Guide To The Code Within This Project
### Web Scraping Code for Consumer Reports Site

A number of interim files get created and then used by different code files in this process.  You can find these files stored with the code in the folders where they are created/used.

Run the code in this order:

1. [Selenium Scripts to Scrape Indiv. Product URLs](https://github.com/TheMitchWorksPro/NYCDSA_CR_WebScrape/tree/master/WebScraping/):
   1. cr_computers_laptops.py  => scrapes products urls for laptops
   2. cr_computers_desktops.py => scrapes product urls for desktops
   3. cr_computers_cbks.py     => scrapes product urls for Chromebooks
  
2. Then run the [scrapy spider](https://github.com/TheMitchWorksPro/NYCDSA_CR_WebScrape/tree/master/WebScraping/cr_computers/cr_computers/spiders) 
   1. filename:  cr_computers_spider.py
   2. make sure the cr_reviewPageURLs_AllComputers.csv is located at this location in spider folder layout even though the spider file is nested deeper
   3. note: there is an "_TEST" file in the same folder you can use to test just a few records beore doing the full run.  You will see lines of code you can comment and switch to to use the test file while setting up to repeat the process
   
3. Finally, in the [same folder](https://github.com/TheMitchWorksPro/NYCDSA_CR_WebScrape/tree/master/WebScraping/) as the scripts from step (1), run this Selenium script to gather the user review data:
   - cr_computers_rvws.py

### Data Munging and Analysis Files

There is a little data munging in a few of the final analysis files but overall, the process is separated out.  To prepare
and preprocess the data, run the output files of the screen scraping process through these code files in this order:

1. [Webscraping](https://github.com/TheMitchWorksPro/NYCDSA_CR_WebScrape) folder -> CR_WebScraping_URLData_Consolidation_TMWP.ipynb
2. [Data Munging](https://github.com/TheMitchWorksPro/NYCDSA_CR_WebScrape/tree/master/Data_Munging) folder:
   1. TMWP_CR_ReviewsReorganization_TMWP.ipynb
   2. cr_dataTransforms1_R.Rmd
   3. cr_dataTransforms2_R.Rmd

#### Final Analysis Code

This is a list of the code files that that were used to create the analysis that was the goal of this project.  Not as much was done as I would have liked to.  Time was a factor.  But hopefully, you may find some of this interesting or useful.  :-)

These files are contained in the same folder as the "[Data Munging](https://github.com/TheMitchWorksPro/NYCDSA_CR_WebScrape/tree/master/Data_Munging)" scripts:

1. [TMWP_CR_Spec_TableAnalysis1.ipynb](https://github.com/TheMitchWorksPro/NYCDSA_CR_WebScrape/blob/master/Data_Munging/TMWP_CR_Spec_TableAnalysis1.ipynb) - Jupyter Notebook with Specification Data Analysis in it
2. WordCloudExp.Rmd - code updated for word cloud included in the blog
3. WordCloudExp2.Rmd - code for Negative Reviews (no words excluded from the cloud)
4. WordCloudExp3.Rmd - code for all reviews (no words excluded from the cloud)


