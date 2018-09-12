from tkinter import *
import pandas as pd
import datetime
'''This is a WIP development of a GUI for the funko_price_scraper.py script'''

class PriceGenerator:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.search_label = Label(frame, text="Please enter product to search:")
        self.search_label.pack(side=LEFT)

        self.search = Entry(frame)
        self.search.pack(side=LEFT)

        self.search_enter = Button(frame, text="Search!", command=self.pop_search)
        self.search_enter.pack(side=RIGHT)

    def pop_search(self):
        now = datetime.datetime.now()
        try:
            df = pd.read_csv("pop_prices_csv_" + str(now.month) + "_" + str(now.day) + ".csv", error_bad_lines=False)
            pop_graph_df = pd.DataFrame(columns = ['NAME', 'STORE', 'ORIGINAL PRICE', 'SALE PRICE'])
            pop_name = self.search.get().lower()
            j = 0
            for i in range(len(df)):
                if pop_name in df.loc[i, "NAME"].lower():
                    pop_graph_df.loc[j] = df.loc[i]
                    j += 1
            end = pop_graph_df.drop_duplicates().to_string()
        except OSError as e:
            end = "No recent data found. Please run funko_price_scraper.py to generate new price data"
        results = Label(text=end)
        results.pack()

root = Tk()
main = PriceGenerator(root)
root.mainloop()
