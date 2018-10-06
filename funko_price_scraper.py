from tkinter import *
import pandas as pd
import datetime
import threading
import requests
import re
from bs4 import BeautifulSoup
from pathlib import Path
from tabulate import tabulate


class PriceGenerator:

    def __init__(self, master):
        # variables init
        self.data = pd.DataFrame(columns=['NAME', 'STORE', 'ORIGINAL PRICE', 'SALE PRICE'])

        # URL init
        self.hot_topic_url = [("https://www.hottopic.com/funko/?sz=60&start=" + str(num)) for num in range(0, 500, 60)]
        self.box_lunch_url = [("https://www.boxlunch.com/funko/?sz=60&start=" + str(num)) for num in range(0, 540, 60)]
        self.ht_bl_urls = [self.hot_topic_url, self.box_lunch_url]
        self.chronotoys_url = [("https://www.chronotoys.com/collections/pop-exclusives?page=" + str(num) + "&sort_by=title-ascending") for num in range(1, 7)]
        self.funko_url = [("https://shop.funko.com/catalog.html?p=" + str(num)) for num in range(32)]
        self.fye_url = [("https://www.fye.com/toys-collectibles/action-figures/funko/?sz=60&start=" + str(num))  for num in range(0, 2160, 60)]
        self.toytokyo_url = [("https://www.toytokyo.com/funko-pop/?sort=alphaasc&page=" + str(num)) for num in range(8)]
        self.fugitive_url = [("https://www.fugitivetoys.com/collections/funko-pop?page=" + str(num) + "&sort_by=title-ascending") for num in range(33)]
        self.seven_url = [("https://7bucksapop.com/collections/all-7-pops?page=" + str(num) + "&sort_by=title-ascending") for num in range(12)] 
        
        # GUI init
        frame = Frame(master)
        frame.grid(row=0, column=0)

        self.htVar = IntVar()
        self.bxVar = IntVar()
        self.cntVar = IntVar()
        self.fVar = IntVar()
        self.fyeVar = IntVar()
        self.ttVar = IntVar()
        self.fgtVar = IntVar()
        self.sevenVar = IntVar()
        self.allVar = IntVar()
        
        self.search_label = Label(frame, text="Please enter product to search:")
        self.search_label.grid(row=0, columnspan = 2, sticky=W)

        self.search = Entry(frame)
        self.search.bind('<Return>', self.pop_search)
        self.search.grid(row=0, column=2)

        self.search_enter = Button(frame, text="Search!", command=self.pop_search)
        self.search_enter.grid(row=0, column=3, sticky=W)
        
        self.status = StringVar()
        self.status_label = Label(frame, textvariable=self.status, bd=1, relief=SUNKEN, anchor=W)
        self.status_label.grid(row=3, column=0, columnspan=9, sticky=S+E+W)
        
        self.generate_data = Button(frame, text="Generate data!", command=self.run).grid(row=1, column=9, sticky=W)

        self.all_option = Checkbutton(frame, state=ACTIVE, variable=self.allVar, text='All').grid(row=1, column=8, sticky=W)
        self.ht_option = Checkbutton(frame, state=ACTIVE, variable=self.htVar, text='Hot Topic').grid(row=1, column=2, sticky="nsew")
        self.bx_option = Checkbutton(frame, state=ACTIVE, variable=self.bxVar, text='Box Lunch').grid(row=1, column=3, sticky="nsew")
        self.cnt_option = Checkbutton(frame, state=ACTIVE, variable=self.cntVar, text='CHRONOTOYS').grid(row=1, column=4, sticky="nsew")
        self.f_option = Checkbutton(frame, state=ACTIVE, variable=self.fVar, text='Funko').grid(row=1, column=5, sticky="nsew")
        self.fye_option = Checkbutton(frame, state=ACTIVE, variable=self.fyeVar, text='FYE').grid(row=1, column=6, sticky="nsew")
        self.tt_option = Checkbutton(frame, state=ACTIVE, variable=self.ttVar, text='ToyTokyo').grid(row=1, column=1, sticky="nsew")
        self.fgt_option = Checkbutton(frame, state=ACTIVE, variable=self.fgtVar, text='Fugitive Toys').grid(row=1, column=0, sticky="nsew")
        self.seven_option = Checkbutton(frame, state=ACTIVE, variable=self.sevenVar, text='7 Bucks a Pop').grid(row=1, column=7, sticky="nsew")

        self.search_result = StringVar()
        self.search_result_label = Label(frame, textvariable=self.search_result)
        self.search_result_label.grid(row=2, columnspan=10)
        
    def pop_search(self, event=None) -> None:
        now = datetime.datetime.now()
        self.results = pd.DataFrame(columns=['NAME', 'STORE', 'ORIGINAL PRICE', 'SALE PRICE'])
        try:
            pop_name = self.search.get()
            if pop_name != "":
                header = ['NAME', 'STORE', 'ORIGINAL PRICE', 'SALE PRICE']
                df = pd.read_csv("pop_prices_csv_" + str(now.month) + "_" + str(now.day) + ".csv", error_bad_lines=False)
                j = 0
                search = set(pop_name.lower().split(' '))
                for i in range(len(df)):
                        if len(search & set(df.loc[i, "NAME"].lower().split(' '))) >= len(search):
                                self.results.loc[j] = df.loc[i]
                                j += 1
                end = str(tabulate(self.results.fillna(value=0), headers=header, showindex=False, tablefmt='pipe'))
                self.search_result.set(end)
            else:
                self.status.set("Please enter a valid product name")
        except:
            self.status.set("No recent data found. Please generate new price data")

    def run(self) -> None:
        self.status.set("Getting data...")
        t1 = threading.Thread(target=self.generate)
        t1.start()

    def generate(self) -> 'DataFrame':
        now = datetime.datetime.now()
        i = 0
        error = []
        found = []
        if self.htVar.get() == 1 or self.bxVar.get() == 1 or self.allVar.get() == 1:
            try:
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
                found.append("Hot Topic/ Box Lunch")
            except:
                error.append("Hot Topic/ Box Lunch")
        if self.cntVar.get() == 1 or self.allVar.get() == 1:
            try:
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
                found.append("CHRONOTOYS")
            except:
                error.append("CHRONOTOYS")
        if self.fVar.get() == 1 or self.allVar.get() == 1:
            try:
                for url in self.funko_url:
                    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
                    product_tile = soup.findAll("div", {"class": "product-item-info"})
                    for product in product_tile:
                        self.data.at[i, "NAME"] = product.div.strong.a.text.strip()
                        self.data.at[i, "ORIGINAL PRICE"] = product.div.div.findAll("span", {"class": "price"})[0].text[1:]
                        self.data.at[i, "STORE"] = "FUNKO"
                        i += 1
                found.append("Funko")
            except:
                error.append("Funko")
        if self.fyeVar.get() == 1 or self.allVar.get() == 1:
            try:
                for url in self.fye_url:
                    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
                    product_tile = soup.findAll("div", {"class": "c-product-tile product-tile product-image"})
                    for product in product_tile:
                        self.data.at[i, "NAME"] = product.findAll("a", {"class": "c-product-tile__product-name-link"})[0].text
                        self.data.at[i, "STORE"] = "FYE"
                        price = product.findAll("div", {"class": "c-product-tile__price product-pricing"})[0].text
                        self.data.at[i, "SALE PRICE"] = price.split("\n")[1]
                        self.data.at[i, "ORIGINAL PRICE"] =  price.split("\n")[2]
                        i += 1
                found.append("FYE")
            except:
                error.append("FYE")
        if self.ttVar.get() == 1 or self.allVar.get() == 1:
            try:
                for url in self.toytokyo_url:
                        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
                        products = soup.findAll({"article": "product-item"})
                        for product in products:
                                self.data.at[i, "NAME"] = list(product.findAll({"h3": "product-item-title"}))[0].text.strip()
                                self.data.at[i, "STORE"] = "ToyTokyo"
                                self.data.at[i, "ORIGINAL PRICE"] = list(product.findAll({"span": "price-value"}))[0].text.strip()[1:]
                                i += 1
                found.append("ToyTokyo")
            except:
                error.append("ToyTokyo")
        if self.fgtVar.get() == 1 or self.allVar.get() == 1:
            try:
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
                found.append("Fugitive Toys")
            except:
                error.append("Fugitive Toys")
        if self.sevenVar.get() == 1 or self.allVar.get() == 1:
            try:
                for url in self.seven_url:
                    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
                    product_title = soup.findAll({'span': 'product-title'})
                    j = 7
                    for q in range(6, len(product_title)-5, 5):
                        self.data.at[i, "STORE"] = "7 Bucks a Pop"
                        self.data.at[i, "NAME"] = product_title[q].text.strip()
                        self.data.at[i, "ORIGINAL PRICE"] = product_title[j].text.strip()
                        j += 5
                        i += 1
                found.append("7 Bucks a Pop")
            except:
                error.append("7 Bucks a Pop")
        self.status.set("Done! Found data for " + str(found))
        if error != '':
            self.status.set("Can't connect to " + str(error) + " | Found data for " + str(found))
        return self.data.drop_duplicates().to_csv("pop_prices_csv_" + str(now.month) + "_" + str(now.day) + ".csv")


def main():
    root = Tk()
    root.title("FUNKO Pop! Price Search")
    root.iconbitmap(r'py.ico')
    main = PriceGenerator(root)
    root.mainloop()
 
 
if __name__ == '__main__':
    main()
