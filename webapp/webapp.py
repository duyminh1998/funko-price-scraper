from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello() -> str:
	return "Hello World"

@app.route('/results')
def results_page() -> 'html':
	results = [('NAME', 'ORIGINAL PRICE', 'SALE PRICE', 'STORE'), ('NAME', 'ORIGINAL PRICE', 'SALE PRICE', 'STORE'), ('NAME', 'ORIGINAL PRICE', 'SALE PRICE', 'STORE'), ('NAME', 'ORIGINAL PRICE', 'SALE PRICE', 'STORE'), ('NAME', 'ORIGINAL PRICE', 'SALE PRICE', 'STORE'), ('NAME', 'ORIGINAL PRICE', 'SALE PRICE', 'STORE')]
	return render_template('index.html', the_row_titles=['NAME', 'ORIGINAL PRICE', 'SALE PRICE', 'STORE'], results = results)

@app.route('/entry')
def entry_page() -> 'html':
	return render_template('entry.html',
                           the_title='Welcome to FUNKO POP! Price Searcher!')


app.run()