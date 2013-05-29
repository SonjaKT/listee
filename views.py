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
	data_store = {"needs": [], "purchases": []}
	for i in db.items():
		if not i[1]: data_store["needs"].append(i[0])
	for i in db.items():
		if i[1]: data_store["purchases"].append(i)
	db.close()
	return render_template("index.html", data=data_store)
'''
@app.route('/add_item/', methods=['POST'])
def add_item():
	pass

@app.route('/log_purchase/', methods=['POST'])
def log_purchase():
	pass
'''

if __name__ == '__main__':
    app.run()

