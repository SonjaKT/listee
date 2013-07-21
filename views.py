from flask import render_template
from flask import Flask
from flask import jsonify
from flask import request
import redis
import database as d
import send_mail as s_m

# create the application
app = Flask(__name__)

def do_it():
	app.run(debug=True)	

r=redis.Redis("localhost")
#r.set("request_no", 1)

def profile(email, group = "ONE_GROUP"):
	username = r.lrange(email, 0, 0)
	needs = d.coallate_active_requests(group)
	outlays = d.find_credits(email)
	purchases = d.purchases(email) #list of tuples (item, price)
	data_store = {"email": email, "needs": needs, "purchases": purchases, "outlays":outlays, "username": username}
	return render_template("index.html", data=data_store)

@app.route('/')
def listee():
	return render_template("login.html")

@app.route('/login_test/', methods = ["POST"])
def login_test():
	email = str(request.form["email"])
	password = str(request.form["password"])
	if r.exists(email): 
		if r.lrange(email, 1, 1) == [password]: return profile(email)
		else: return render_template("no_password.html", data={"username": r.lrange(email, 0, 0)})
	else: 
		return render_template("no_email.html", data = {"email":email})

@app.route('/login_create/', methods=['POST'])
def add_user():
	email = str(request.form["email"])
	username = str(request.form["username"])
	password = str(request.form["password1"])
	d.add_user(username, password, email)
	return profile(email)

@app.route('/email_retrieval/', methods=['POST'])
def cred_lookup():
	email = str(request.form["email"])
	message = "Hello {0}: Your password is {1}. Now get back on that horse!".format(r.lrange(email, 0, 0)[0], r.lrange(email, 1, 1)[0])
	subject = "Message from Listee"
	s_m.send_email([email], subject, message)
	return render_template("login.html")

@app.route('/add_item/', methods=['POST'])
def add_item():
	item = str(request.form["item"])
	email = str(request.form["email"])
	d.add_request(item, email)
	return profile(email)

@app.route('/log_purchase/', methods=['POST'])
def log_purchase():
	email = str(request.form["email"])
	d.log_purchase(str(request.form["item"]), float(request.form["price"]), email)
	return profile(email)

if __name__ == '__main__':
	do_it()
