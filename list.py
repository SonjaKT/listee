db = {} 
'''db.keys() will be a list of request id numbers. The associated value will be a dictionary of the following form
{total_quantity: , requestor: (name, max_price), purchaser: (name, quantity, price_paid), purchase_price: , purchase_store: , purchase_store_type: , total_offer: }
'''
users = {}
'''
users dictionary. users.keys() are users names, values are {idnumber: price, ...}. price will be 0-max_price if it's a request, spent if it's a fulfillment of a request. 
'''
number = (i for i in range(10,000))
def unique_id():
	return number.next()

def add_new_request(name, item, max_price, quantity=1):
	todays_id = unique_id()
	db[todays_id] = {"requestor": [name], "quantity":quantity, "purchaser": "", "purchase_price": "", "purchase_store": "", "purchase_store_type": "", "total_offer": max_price}
	if name not in users:
		users[name] = {todays_id:{"max_price":max_price, "amt_spent":0}}
	else: 
		users[name][todays_id] = {"max_price":max_price, "amt_spent":0}

def append_request_join(name, max_price, request_id):
	db[request_id]["requestor"].append(name)
	db[request_id]["total_offer"] = db[request_id]["total_offer"] + max_price
	if name not in users:
		users[name] = {request_id: {"max_price":max_price, "amt_spent":0}}
	else:
		users[name][request_id] = {"max_price":max_price, "amt_spent":0}


def log_purchase(name, request_id, spent, store_name = "", store_type = "", quantity):
	db[request_id]["quantity"] = db[request_id]["quantity"]-quantity
	db[request_id]["purchaser"] = name
	db[request_id]["purchase_price"] = spent
	db[request_id]["purchase_store"] = store_name
	db[request_id]["purchase_store_type"] = store_type
	#users[name][request_id] = {request_id: {"max_price":"", "amt_spent": spent}}
	
	split_responsibity(request_id, name, spent) #this has to go after the above if/else


def split_responsibility(r_id, buyer_name, spent):
#	requestors = db[r_id]["requestor"] #list of tuples (name, max_price)
	total_offer = db[r_id]["total_offer"]
	difference = total_offer - spent
	if difference < 0: #effectively making the request and getting charged for it AT THE SAME DAMN TIME
		if r_id not in users[buyer_name]:
			users[buyer_name][r_id] = difference #meant to be called in log_purchase only for now
	for name_price in requestors:
		for request in users[name_price[0]]:
			if request[0] == r_id: 
				request[1] = 0-spent*name_price[1]/total_offer

def settle_scores(method="evenly"):
	if method == "evenly":
		n = len(users.keys()) 
		total_spent = sum([d["purchase price"] for d in db.values()]) 
		from_each = total_spent/n
