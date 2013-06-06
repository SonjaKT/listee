from flask import render_template
from flask import Flask
from flask import jsonify
from flask import request
import shelve

# create the application
app = Flask(__name__)

@app.route('/')
def index():
	db = shelve.open("listee_dict")
	data_store = {"needs": [], "purchases": [], "outlays":0.0}
	outlays = 0.0
	for i in db.items():
		if not i[1]: data_store["needs"].append(i[0])
	for i in db.items():
		if i[1]: 
			data_store["purchases"].append(i)
			data_store["outlays"] += float(i[1])
	db.close()
	return render_template("index.html", data=data_store)

@app.route('/work_bitches')
def f():
	return 'WORK'

@app.route('/add_item/', methods=['POST'])
def add_item():
	db = shelve.open("listee_dict")
	db[str(request.form["item"])] = ""
	db.close()
	return render_template("success_redirect.html", data={})

@app.route('/log_purchase/', methods=['POST'])
def log_purchase():
	db = shelve.open("listee_dict")
	db[str(request.form["item"])] = str(request.form["price"])
	db.close()
	return render_template("success_redirect.html", data={})


if __name__ == '__main__':
    app.run(debug=True)

