![Funko Pop!](http://diskingdom.com/wp-content/uploads/2015/01/pop-vinyls-vault-banner-1024x401.jpg)

# funko-price-scraper
This Python script utilizes BeautifulSoup, Requests, and Pandas to search daily for FUNKO Pop! Products pricing discrepancies across multiple online retailers. The script currently supports Hot Topic, Box Lunch, CHRONOTOYS, Funko, FYE, ToyTokyo Fugitive Toys and 7 Bucks a Pop. This repo current supports two versions of the script: one that stores results in .csv and one that stores results in a local SQL server. 

NOTE: Updating for the most recent prices usually take 4~5 minute because the script has to scrape multiple retailers.

# updates
Webapp for FUNKO Pop! Price Searcher in progress.

# prerequisites
1. Python 3.7
2. pip

# beginner tutorial
1. Click on "Clone or download", and then "Download Zip".
2. Unzip the repo anywhere.
3. Go into the "funko-price-scraper-master" folder, make sure you see files such as "requirements.txt" and "README". 
4. Hold Shift and Right Click anywhere in the folder, choose "Open PowerShell Window here..." or "Open Command Prompt here..."
5. Type `py -3 -m pip install -r requirements.txt`, wait for it to finish.
6. Run funko_price_scraper.py, check the stores you want prices from, and click Generate Data! (Getting data from All stores will take 5-6 minutes)
7. Wait for the status bar to go from "Getting data..." to "Done!".
8. Search for any Funko Pop! product on the search bar.


# usage
The first thing that you should do when you run the program is press "Generate data!" to get the most recent prices. Please check the store boxes to select the stores you want to get prices from. After the program finishes getting the data, you can enter the name of the Funko Pop! in the search bar and click "Search!" to search for its price. 

You will not have to generate the price again until the next day. For example, if you generated data on 09/22/2018, you can continue to search for prices until 09/23/2018, which is when the program will ask you to generate new pricing data. Additionally, you can always generate new price data if you want the most recent prices, or if you only searched a few stores and you want to search for more. 
   
# to-do
~create GUI~

add support for more stores

~add support for selecting which stores to check pricing~

add support for accessing pricing from older dates

add support for analysis of price trends in the form of graphs and charts

~improve GUI (format results table)~

~use Flask to create a website for the script, facilitating user experience as well as speeds up the process~
