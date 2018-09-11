import pandas as pd
from bs4 import BeautifulSoup
import requests
from pathlib import Path
import re
import datetime
from tabulate import tabulate
'''This script returns and generates pricing for FUNKO Pop! Products.'''


class PriceSearcher():
        def __init__(self) -> None: #initializes urls
                self.data = pd.DataFrame(columns=['NAME', 'STORE', 'ORIGINAL PRICE', 'SALE PRICE'])

                self.hot_topic_url = [("https://www.hottopic.com/funko/?sz=60&start=" + str(num)) for num in range(0, 500, 60)]
                
                self.box_lunch_url = [("https://www.boxlunch.com/funko/?sz=60&start=" + str(num)) for num in range(0, 540, 60)]

                self.ht_bl_urls = [self.hot_topic_url, self.box_lunch_url]

                self.chronotoys_url = [("https://www.chronotoys.com/collections/pop-exclusives?page=" + str(num) + "&sort_by=title-ascending") for num in range(1, 7)]

                self.funko_url = [("https://shop.funko.com/catalog.html?p=" + str(num)) for num in range(32)]

                self.fye_url = [("https://www.fye.com/toys-collectibles/action-figures/funko/?sz=60&start=" + str(num))  for num in range(0, 2160, 60)]

                self.toytokyo_url = [("https://www.toytokyo.com/funko-pop/?sort=alphaasc&page=" + str(num)) for num in range(8)]

                self.fugitive_url = [("https://www.fugitivetoys.com/collections/funko-pop?page=" + str(num) + "&sort_by=title-ascending") for num in range(33)]

        # parses pricing data from the csv
        def search_4_price_csv(self, pop_name: str) -> "DataFrame":
                header = ['NAME', 'STORE', 'ORIGINAL PRICE', 'SALE PRICE']
                df = pd.read_csv("pop_prices_csv_" + str(now.month) + "_" + str(now.day) + ".csv", error_bad_lines=False)
                self.results = pd.DataFrame(columns=header)
                j = 0
                search = set(pop_name.lower().split(' '))
                for i in range(len(df)):
                        if len(search & set(df.loc[i, "NAME"].lower().split(' '))) >= len(search):
                                self.results.loc[j] = df.loc[i]
                                j += 1
                print(tabulate(self.results.fillna(value=0), headers=header, showindex=False, tablefmt='psql'))

        # generates pricing data and stores into csv
        def generate(self) -> "csv":
                i = 0
                k = 0
                store = ["Hot Topic", "Box Lunch"]
                for url_set in self.ht_bl_urls:
                        for url in url_set:
                                headers = {"User-Agent": "Chrome/5.0"}
                                soup = BeautifulSoup(requests.get(url, headers=headers).text, 'html5lib')
                                product_tile = soup.findAll("div", {"class": "product-tile"})
                                for product in product_tile:
                                        self.data.at[i, "NAME"] = product.div.a.img["title"]
                                        price = product.findAll("div", {"class": "product-pricing"})[0].div.text.strip()
                                        if len(price) == 5 or len(price) == 6:
                                            self.data.at[i, "ORIGINAL PRICE"] = price[1:]
                                        elif len(price) == 11:
                                            self.data.at[i, "ORIGINAL PRICE"] = price[1:5]
                                            self.data.at[i, "SALE PRICE"] = price[-4:]
                                        elif len(price) == 12:
                                            self.data.at[i, "ORIGINAL PRICE"] = price[1:6]
                                            self.data.at[i, "SALE PRICE"] = price[-4:]
                                        elif len(price) == 13:
                                            self.data.at[i, "ORIGINAL PRICE"] = price[1:6]
                                            self.data.at[i, "SALE PRICE"] = price[-5:]
                                        self.data.at[i, "STORE"] = store[k]
                                        i += 1
                        k += 1
                for url in self.chronotoys_url:
                    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
                    product_tile = soup.findAll("div", {"class": "grid__item wide--one-fifth large--one-quarter medium-down--one-half"})
                    for product in product_tile:
                        self.data.at[i, "NAME"] = product.div.p.text
                        price = re.findall('\d+', product.div.findAll("p", {"class": "grid-link__meta"})[0].text)
                        self.data.at[i, "ORIGINAL PRICE"] = '.'.join(price[0:2])
                        self.data.at[i, "SALE PRICE"] = '.'.join(price[2:4])
                        self.data.at[i, "STORE"] = "CHRONOTOYS"
                        i += 1
                for url in self.funko_url:
                    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
                    product_tile = soup.findAll("div", {"class": "product-item-info"})
                    for product in product_tile:
                        self.data.at[i, "NAME"] = product.div.strong.a.text.strip()
                        self.data.at[i, "ORIGINAL PRICE"] = product.div.div.findAll("span", {"class": "price"})[0].text[1:]
                        self.data.at[i, "STORE"] = "FUNKO"
                        i += 1
                for url in self.fye_url:
                    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
                    product_tile = soup.findAll("div", {"class": "c-product-tile product-tile product-image"})
                    for product in product_tile:
                        self.data.at[i, "NAME"] = product.findAll("a", {"class": "c-product-tile__product-name-link"})[0].text
                        self.data.at[i, "STORE"] = "FYE"
                        product_tile = soup.findAll("div", {"class": "c-product-tile product-tile product-image"})
                        for product in product_tile:
                        	price = product.findAll("div", {"class": "c-product-tile__price product-pricing"})[0].text
                        	self.data.at[i, "SALE PRICE"] = price.split("\n")[1]
                        	self.data.at[i, "ORIGINAL PRICE"] =  price.split("\n")[2]
                        i += 1
                for url in self.toytokyo_url:
                	soup = BeautifulSoup(requests.get(url).text, 'html.parser')
                	products = soup.findAll({"article": "product-item"})
                	for product in products:
                		self.data.at[i, "NAME"] = list(product.findAll({"h3": "product-item-title"}))[0].text.strip()
                		self.data.at[i, "STORE"] = "ToyTokyo"
                		self.data.at[i, "ORIGINAL PRICE"] = list(product.findAll({"span": "price-value"}))[0].text.strip()[1:]
                		i += 1
                for url in self.fugitive_url:
                    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
                    products = soup.findAll({"span": "title"})
                    n = 10
                    k = 11
                    while n < 207:
                        self.data.at[i, "STORE"] = "Fugitive Toys"
                        self.data.at[i, "NAME"] = products[n].text.strip()
                        self.data.at[i, "ORIGINAL PRICE"] = products[k].text.strip()
                        n += 4
                        k += 4
                        i += 1
                self.data.drop_duplicates().to_csv("pop_prices_csv_" + str(now.month) + "_" + str(now.day) + ".csv")

def main():
    searcher = PriceSearcher()
    global now
    now = datetime.datetime.now()
    my_file = Path("pop_prices_csv_" + str(now.month) + "_" + str(now.day) + ".csv")
    while True:
            if my_file.is_file():
                    print("\n" + "FUNKO Pop! Pricing Search")
                    print("--Please try fewer words if the search fails--\n")
                    product_name = input("Please input product name to search or type quit to exit program: ")
                    if product_name == 'quit':
                        break
                    searcher.search_4_price_csv(pop_name=product_name)
            else:
                    print("Getting data...")
                    searcher.generate()
                    print("Done!")

if __name__ == '__main__':
        main()
