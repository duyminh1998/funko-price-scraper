from tkinter import *
import pandas as pd
import datetime
'''This is a WIP development of a GUI for the funko_price_scraper.py script.
   In order to use the GUI, the GUI.pyw must be in the same folder/directory as the most recent price csv.
   It is the best practice to leave GUI.pyw and funko_price_scraper.py in the same folder because the latter
   generates the csv that the former uses.'''

class PriceGenerator:

   def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.htVar = IntVar()
        self.bxVar = IntVar()
        self.cntVar = IntVar()
        self.fVar = IntVar()
        self.fyeVar = IntVar()
        self.ttVar = IntVar()
        self.fgtVar = IntVar()
        

        self.search_label = Label(frame, text="Please enter product to search:")
        self.search_label.pack(side=TOP)

        self.search = Entry(frame)
        self.search.pack(side=TOP)

        self.search_enter = Button(frame, text="Search!", command=self.pop_search)
        self.search_enter.pack(side=TOP)

        self.ht_option = Checkbutton(frame, state=ACTIVE, variable=self.htVar, text='Hot Topic').pack(side=BOTTOM)
        self.bx_option = Checkbutton(frame, state=ACTIVE, variable=self.bxVar, text='Box Lunch').pack(side=BOTTOM)
        self.cnt_option = Checkbutton(frame, state=ACTIVE, variable=self.cntVar, text='CHRONOTOYS').pack(side=BOTTOM)
        self.f_option = Checkbutton(frame, state=ACTIVE, variable=self.fVar, text='Funko').pack(side=BOTTOM)
        self.fye_option = Checkbutton(frame, state=ACTIVE, variable=self.fyeVar, text='FYE').pack(side=BOTTOM)
        self.tt_option = Checkbutton(frame, state=ACTIVE, variable=self.ttVar, text='ToyTokyo').pack(side=BOTTOM)
        self.fgt_option = Checkbutton(frame, state=ACTIVE, variable=self.fgtVar, text='Fugitive Toys').pack(side=BOTTOM)

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
