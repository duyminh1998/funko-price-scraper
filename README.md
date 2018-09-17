![Funko Pop!](http://diskingdom.com/wp-content/uploads/2015/01/pop-vinyls-vault-banner-1024x401.jpg)

# funko-price-scraper
This Python script utilizes BeautifulSoup, Requests, and Pandas to search daily for FUNKO Pop! Products pricing discrepancies across multiple online retailers. The script currently supports Hot Topic, Box Lunch, CHRONOTOYS, Funko, FYE, ToyTokyo Fugitive Toys and 7 Bucks a Pop.

NOTE: Updating for the most recent prices usually take 4~5 minute because the script has to scrape multiple retailers.

# prerequisites
1. Python 3.7
2. pip

# usage
1. download or clone repo through github
2. `$ pip install -r requirements.txt`
3. run funko_price_scraper.py daily to get the most recent prices
4. (optional) run GUI.pyw as an alternative because it has a GUI that supports accessing price for specific stores rather than every store
   
# to-do
~create GUI~

add support for more stores

~add support for selecting which stores to check pricing~

add support for accessing pricing from older dates

add support for analysis of price trends in the form of graphs and charts

improve GUI
