from tkinter import *
import datetime
import threading
import requests
import re
from bs4 import BeautifulSoup
import sqlite3


class PriceGenerator:

    def __init__(self, master):
        # sql init
        self.sql_transaction = []
        self.connection = sqlite3.connect('database/{}.db'.format('funko_pop_prices'), check_same_thread=False)
        self.c = self.connection.cursor()

        self.htVar = IntVar()
        self.bxVar = IntVar()
        self.cntVar = IntVar()
        self.fVar = IntVar()
        self.ttVar = IntVar()
        self.allVar = IntVar()

        self.frame_existence = 1

        # GUI init
        frame = Frame(master)
        frame.grid(row=0, column=0)
        
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
        self.tt_option = Checkbutton(frame, state=ACTIVE, variable=self.ttVar, text='ToyTokyo').grid(row=1, column=1, sticky="nsew")

    # sql transaction builder
    def transaction_bldr(self):
        self.c.execute('BEGIN TRANSACTION')
        for s in self.sql_transaction:
            try:
                self.c.execute(s)
            except Exception as e:
                print('SQL Transaction', str(e), s)
        self.connection.commit()

    def sql_insertion(self, name, og_price, sale_price, store, table_name):
        try:
            sql = """INSERT INTO {} (NAME, ORIGINAL_PRICE, SALE_PRICE, STORE) VALUES ("{}", {}, {}, "{}")""".format(table_name, name, og_price, sale_price, store)
            self.sql_transaction.append(sql)
        except Exception as e:
            print("SQL Insertion Error: ", str(e))

    def pop_search(self, event=None):
        now = datetime.datetime.now()
        table_name = "pop_prices_" + str(now.month) + "_" + str(now.day)
        if self.frame_existence != 1:
            self.results_frame.grid_forget()
        try:
            pop_name = self.search.get()
            if pop_name != "":
                pop_name = pop_name.split()
                for i, word in enumerate(pop_name):
                    pop_name[i] = '"%{}%"'.format(word)
                query = 'SELECT * FROM pop_prices_12_17 WHERE NAME LIKE {}'.format(pop_name[0])
                for word in pop_name[1:]:
                    query = query + ' AND NAME LIKE {}'.format(word)
                self.c.execute(query)
                results = self.c.fetchall()
                self.results_frame = Frame()
                self.results_frame.grid(row=3, column=0)
                self.head_name = Label(self.results_frame, text="NAME")
                self.head_name.grid(row=3, column = 1)
                self.head_store = Label(self.results_frame, text="STORE")
                self.head_store.grid(row=3, column = 2)
                self.head_ogp = Label(self.results_frame, text="ORIGINAL PRICE")
                self.head_ogp.grid(row=3, column = 3)
                self.head_sp = Label(self.results_frame, text="SALE PRICE")
                self.head_sp.grid(row=3, column = 4)
                for i, result in enumerate(results):
                    self.results_name = Label(self.results_frame, text=result[0])
                    self.results_name.grid(row=i+4, column = 1)
                    self.results_store = Label(self.results_frame, text=result[1])
                    self.results_store.grid(row=i+4, column = 2)
                    self.results_ogp = Label(self.results_frame, text=result[2])
                    self.results_ogp.grid(row=i+4, column = 3)
                    self.results_sp = Label(self.results_frame, text=result[3])
                    self.results_sp.grid(row=i+4, column = 4)
                self.frame_existence = 2
            else:
                self.status.set("Please enter a valid product name")
        except Exception as e:
            self.status.set(str(e))

    def run(self) -> None:
        self.status.set("Getting data...")
        t1 = threading.Thread(target=self.generate)
        t1.start()
        return None

    # scrapes retailers for pricing depending on which stores the users chose
    def generate(self) -> 'DataFrame':
        now = datetime.datetime.now()
        table_name = "pop_prices_" + str(now.month) + "_" + str(now.day)
        error = set()
        found = set()
        self.c.execute("""DROP TABLE IF EXISTS {}""".format(table_name))
        self.c.execute("""CREATE TABLE IF NOT EXISTS {} (NAME TEXT, ORIGINAL_PRICE REAL, SALE_PRICE REAL, STORE TEXT);""".format(table_name))
        if self.htVar.get() == 1 or self.bxVar.get() == 1 or self.allVar.get() == 1:
            try:
                store_tracker = 0
                stores = ["Hot Topic", "Box Lunch"]
                hot_topic_url = [("https://www.hottopic.com/funko/?sz=60&start=" + str(num)) for num in range(0, 500, 60)]
                box_lunch_url = [("https://www.boxlunch.com/funko/?sz=60&start=" + str(num)) for num in range(0, 600, 60)]
                ht_bl_urls = [hot_topic_url, box_lunch_url]
                for url_set in ht_bl_urls:
                        for url in url_set:
                                headers = {"User-Agent": "Chrome/5.0"}
                                soup = BeautifulSoup(requests.get(url, headers=headers).text, 'html5lib')
                                product_tile = soup.findAll("div", {"class": "product-tile"})
                                for product in product_tile:
                                        name = product.div.a.img["title"].strip()
                                        price = product.findAll("div", {"class": "product-pricing"})[0].div.text.strip()
                                        if len(price) == 5 or len(price) == 6:
                                            og_price = price[1:]
                                        elif len(price) == 11:
                                            og_price = price[1:5]
                                            sale_price = price[-4:]
                                        elif len(price) == 12:
                                            og_price = price[1:6]
                                            sale_price = price[-4:]
                                        elif len(price) == 13:
                                            og_price = price[1:6]
                                            sale_price = price[-5:]
                                        store = stores[store_tracker]
                                        self.sql_insertion(name, og_price, sale_price, store, table_name)
                        found.add(stores[store_tracker])
                        store_tracker += 1
            except:
                error.add(stores[store_tracker])
        if self.cntVar.get() == 1 or self.allVar.get() == 1:
            try:
                chronotoys_url = [("https://www.chronotoys.com/collections/pop-exclusives?page=" + str(num) + "&sort_by=title-ascending") for num in range(1, 7)]
                for url in chronotoys_url:
                    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
                    product_tile = soup.findAll("div", {"class": "grid__item wide--one-fifth large--one-quarter medium-down--one-half"})
                    for product in product_tile:
                        name = product.div.p.text.replace('"', '""')
                        price = re.findall('\d+', product.div.findAll("p", {"class": "grid-link__meta"})[0].text)
                        og_price = '.'.join(price[0:2])
                        sale_price = '.'.join(price[2:4])
                        if not sale_price:
                            sale_price = 0
                        store = "CHRONOTOYS"
                        self.sql_insertion(name, og_price, sale_price, store, table_name)
                found.add("CHRONOTOYS")
            except:
                error.add("CHRONOTOYS")
        if self.fVar.get() == 1 or self.allVar.get() == 1:
            try:
                funko_url = [("https://shop.funko.com/catalog.html?p=" + str(num)) for num in range(35)]
                for url in funko_url:
                    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
                    product_tile = soup.findAll("div", {"class": "product-item-info"})
                    for product in product_tile:
                        name = product.div.strong.a.text.strip()
                        og_price = product.div.div.findAll("span", {"class": "price"})[0].text[1:]
                        sale_price = 0
                        store = "FUNKO"
                        self.sql_insertion(name, og_price, sale_price, store, table_name)
                found.add("Funko")
            except:
                error.add("Funko")
        if self.ttVar.get() == 1 or self.allVar.get() == 1:
            try:
                toytokyo_url = [("https://www.toytokyo.com/funko/?sort=alphaasc&page=" + str(num)) for num in range(9)]
                for url in toytokyo_url:
                        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
                        products = soup.findAll({"article": "product-item"})
                        for product in products:
                                name = list(product.findAll({"h3": "product-item-title"}))[0].text.strip().replace('"', '""')
                                store = "ToyTokyo"
                                og_price = list(product.findAll({"span": "price-value"}))[0].text.strip()[1:]
                                sale_price = 0
                                self.sql_insertion(name, og_price, sale_price, store, table_name)
                found.add("ToyTokyo")
            except:
                error.add("ToyTokyo")
        self.transaction_bldr()
        self.status.set("Done! Found data for " + str(found))
        if error != set() and found != set():
            self.status.set("Can't connect to " + str(error) + " | Found data for " + str(found))
        elif error != set() and found == set():
            self.status.set("Can't connect to " + str(error))

def main():
    root = Tk()
    root.title("FUNKO Pop! Price Search")
    main = PriceGenerator(root)
    root.mainloop()
 
 
if __name__ == '__main__':
    main()
