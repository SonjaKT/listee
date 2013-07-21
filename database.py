import redis
#request no, datetimestamp, item, r.max.price, rqstr, l_group, item_store, buyer, price_paid
r=redis.Redis("localhost")

def add_group(email, group):
	r.rpush(email, group) #for if u want to look up what groups a email is in
	r.rpush(group, email) 
#group : [email1, email2, email3, ... ]

def add_user(username, password, email):
	r.rpush(email, username)
	r.rpush(email, password)
	add_group(email, "ONE_GROUP")
#email : [username,password, group] <-a list
'''
def check_credentials(email, username, password):
	if r.lrange(email, 0, 1) == [username, password]:
		profile(email)
	if not r.lrange(email, 0, 0):
		render_template("login_fail.html", data = {email:False})
	else: render_template("login_fail.html", data = {email:True})
'''
def add_request(item, email):
	request_no = r.incr("request_no")
	r.rpush(request_no, email)
	r.rpush("{0}.r".format(email), request_no)
	r.rpush(request_no, item)
	r.set(item, request_no)

def purchases(email):
	L = []
	for request_no in r.lrange("{0}.b".format(email), 0, -1):
		L.append((r.lrange(request_no, 1, 1)[0], r.lrange(request_no, 2, 2)[0]))
	return L

def log_purchase(item, price_paid, buyer):
	if not r.exists(item):	#makes request if the item isnt already in the list of needs
		add_request(item, buyer)
		log_purchase(item, price_paid, buyer) #immediately notes purchase
	else:
		request_no = r.get(item)
		r.rpush(request_no, price_paid)
		r.rpush(request_no, buyer)
		r.rpush("{0}.b".format(buyer), request_no)
#email.b : [request_no]
#request_no : [email, item, price_paid, buyer]

def coallate_active_requests(group):
	L=[]
	for email in r.lrange(group, 0, -1):
		for request_no in r.lrange("{0}.r".format(email), 0, -1):
			r.sadd("requests", request_no)
		for request_no in r.lrange("{0}.b".format(email), 0, -1):
			r.sadd("bought", request_no)
	for request_no in list(r.sdiff("requests", "bought")):
		L.append(r.lrange(request_no, 1, 1))
	return L

def find_credits(u_mail):
	CR = 0
	if r.exists("{0}.b".format(u_mail)):
		for request_no in r.lrange("{0}.b".format(u_mail), 0, -1):
			CR = CR + float(r.lrange(request_no, 2, 2)[0])
	return CR

def find_debts(u_mail):
	debts = 0
	for request_no in r.lrange("{0}.r".format(u_mail), 0, -1):
		debts = debts + float(r.lrange(request_no, 3, 3))
	return debts

def settle_up(u_mail, group, method):
	greedy_pigs = 0
	credits = find_credits(u_mail)
	if method == "direct":	user_owes = credits - find_debts(u_mail)
	if method == "even weight":
		members = r.lrange(group, 0, -1)
		for email in members:
			greedy_pigs = greedy_pigs + find_credits(email)
		user_owes = credits - greedy_pigs/len(members)
	return user_owes

#def cred_lookup(email):
#	message = r.lrange(email, 0, 1)
#	return render_template("email_sent.html", data = message)

#	r.rpush(request_no, r_max_price)
#request_no : [rqstr, item, max_price, price_paid, buyer]
#email.r : [request_no]
#item : [request_no]
