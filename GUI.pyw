from tkinter import *
import pandas as pd
import datetime, threading, requests, re
from bs4 import BeautifulSoup
from pathlib import Path
from tabulate import tabulate
'''This is a WIP fdevelopment of a GUI for the funko_price_scraper.py script'''

class PriceGenerator:

    def __init__(self, master):
    	# URL and DataFrame init
        self.data = pd.DataFrame(columns=['NAME', 'STORE', 'ORIGINAL PRICE', 'SALE PRICE'])

        self.hot_topic_url = [("https://www.hottopic.com/funko/?sz=60&start=" + str(num)) for num in range(0, 500, 60)]
        
        self.box_lunch_url = [("https://www.boxlunch.com/funko/?sz=60&start=" + str(num)) for num in range(0, 540, 60)]

        self.ht_bl_urls = [self.hot_topic_url, self.box_lunch_url]

        self.chronotoys_url = [("https://www.chronotoys.com/collections/pop-exclusives?page=" + str(num) + "&sort_by=title-ascending") for num in range(1, 7)]

        self.funko_url = [("https://shop.funko.com/catalog.html?p=" + str(num)) for num in range(32)]

        self.fye_url = [("https://www.fye.com/toys-collectibles/action-figures/funko/?sz=60&start=" + str(num))  for num in range(0, 2160, 60)]

        self.toytokyo_url = [("https://www.toytokyo.com/funko-pop/?sort=alphaasc&page=" + str(num)) for num in range(8)]

        self.fugitive_url = [("https://www.fugitivetoys.com/collections/funko-pop?page=" + str(num) + "&sort_by=title-ascending") for num in range(33)]
        
        # GUI init
        frame = Frame(master)
        frame.pack(fill=BOTH)

        self.htVar = IntVar()
        self.bxVar = IntVar()
        self.cntVar = IntVar()
        self.fVar = IntVar()
        self.fyeVar = IntVar()
        self.ttVar = IntVar()
        self.fgtVar = IntVar()
        
        self.search_label = Label(frame, text="Please enter product to search:")
        self.search_label.pack(side=TOP, fill=BOTH)

        self.search = Entry(frame)
        self.search.pack(side=TOP, fill=BOTH)

        self.search_enter = Button(frame, text="Search!", command=self.pop_search)
        self.search_enter.pack(side=TOP, fill=BOTH)

        self.ht_option = Checkbutton(frame, state=ACTIVE, variable=self.htVar, text='Hot Topic').pack(side=BOTTOM, fill=BOTH)
        self.bx_option = Checkbutton(frame, state=ACTIVE, variable=self.bxVar, text='Box Lunch').pack(side=BOTTOM, fill=BOTH)
        self.cnt_option = Checkbutton(frame, state=ACTIVE, variable=self.cntVar, text='CHRONOTOYS').pack(side=BOTTOM, fill=BOTH)
        self.f_option = Checkbutton(frame, state=ACTIVE, variable=self.fVar, text='Funko').pack(side=BOTTOM, fill=BOTH)
        self.fye_option = Checkbutton(frame, state=ACTIVE, variable=self.fyeVar, text='FYE').pack(side=BOTTOM, fill=BOTH)
        self.tt_option = Checkbutton(frame, state=ACTIVE, variable=self.ttVar, text='ToyTokyo').pack(side=BOTTOM, fill=BOTH)
        self.fgt_option = Checkbutton(frame, state=ACTIVE, variable=self.fgtVar, text='Fugitive Toys').pack(side=BOTTOM, fill=BOTH)

        self.generate_data = Button(frame, text="Generate data!", command=self.run).pack(fill=BOTH)

    def pop_search(self):
        now = datetime.datetime.now()
        try:
            pop_name = self.search.get()
            header = ['NAME', 'STORE', 'ORIGINAL PRICE', 'SALE PRICE']
            df = pd.read_csv("pop_prices_csv_" + str(now.month) + "_" + str(now.day) + ".csv", error_bad_lines=False)
            self.results = pd.DataFrame(columns=header)
            j = 0
            search = set(pop_name.lower().split(' '))
            for i in range(len(df)):
                    if len(search & set(df.loc[i, "NAME"].lower().split(' '))) >= len(search):
                            self.results.loc[j] = df.loc[i]
                            j += 1
            end = str(tabulate(self.results.fillna(value=0), headers=header, showindex=False, tablefmt='psql'))
        except OSError as e:
            end = "No recent data found. Please generate new price data"
        results = Label(text=end).pack(fill=BOTH)

    def run(self):
        print("Getting data...")
        t1 = threading.Thread(target=self.generate)
        t1.start()

    def generate(self):
        now = datetime.datetime.now()
        i = 0
        if self.htVar.get() == 1:
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
        if self.cntVar.get() == 1:
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
        if self.fVar.get() == 1:
            for url in self.funko_url:
                soup = BeautifulSoup(requests.get(url).text, 'html.parser')
                product_tile = soup.findAll("div", {"class": "product-item-info"})
                for product in product_tile:
                    self.data.at[i, "NAME"] = product.div.strong.a.text.strip()
                    self.data.at[i, "ORIGINAL PRICE"] = product.div.div.findAll("span", {"class": "price"})[0].text[1:]
                    self.data.at[i, "STORE"] = "FUNKO"
                    i += 1
        if self.fyeVar.get() == 1:
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
        if self.ttVar.get() == 1:
            for url in self.toytokyo_url:
                    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
                    products = soup.findAll({"article": "product-item"})
                    for product in products:
                            self.data.at[i, "NAME"] = list(product.findAll({"h3": "product-item-title"}))[0].text.strip()
                            self.data.at[i, "STORE"] = "ToyTokyo"
                            self.data.at[i, "ORIGINAL PRICE"] = list(product.findAll({"span": "price-value"}))[0].text.strip()[1:]
                            i += 1
        if self.fgtVar.get() == 1:
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
        #done_generate_msg = Label(text="Finished getting data!").pack(fill=BOTH)
        print("Done!")

def main():
    root = Tk()
    main = PriceGenerator(root)
    root.mainloop()
 
if __name__ == '__main__':
    main()
