from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello() -> str:
	return "Hello World"

@app.route('/search4', methods=['POST'])
def results_page() -> 'html':
        connection = sqlite3.connect('database/{}.db'.format('funko_pop_prices'))
        c = connection.cursor()
        pop_name = request.form['phrase'].split()
        for i, word in enumerate(pop_name):
                pop_name[i] = '"%{}%"'.format(word)
        query = 'SELECT * FROM pop_prices_12_17 WHERE NAME LIKE {}'.format(pop_name[0])
        for word in pop_name[1:]:
                query = query + ' AND NAME LIKE {}'.format(word)
        c.execute(query)
        results = c.fetchall()
        return render_template('index.html', the_row_titles=['NAME', 'ORIGINAL PRICE', 'SALE PRICE', 'STORE'], results = results)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
	return render_template('entry.html',
                           the_title='Welcome to FUNKO POP! Price Searcher!')


app.run()
