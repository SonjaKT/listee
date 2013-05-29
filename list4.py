import shelve


	def add_new_request(string):
		db[string] = ""

	def log_purchase(string, spent):
		db[string] = spent

	def sum_purchases():
		spent = 0
		for i in db.items():
			if i[1]: spent = spent + float(i[1])
		return spent


def do_it():

	db = shelve.open("listee_dict")
	quit = False

	def add_new_request():
		string = raw_input("what do you want? ")
		db[string] = ""
		print "%s added to list" %(string)

	def log_purchase():
		string = raw_input("what did you buy? ")
		spent = raw_input("how much did it cost? ")
		db[string] = spent

	def list_needs():
		print "Things you need"
		for i in db.items():
			if not i[1]: print i[0]

	def list_purchases():
		print "Things you bought"
		for i in db.items():
			if i[1]: print "%s, $%s" %i

	def sum_purchases():
		spent = 0
		for i in db.items():
			if i[1]: spent = spent + float(i[1])
		return spent

	print "LISTEE"
	print "For list of needs ... press 1"
	print "For list of things bought ... press 2"
	print "To input need ... press 3"
	print "To input purchase ... press 4"
	print "To sum purchases ... press $"
	print "To exit type 'exit'"
	while not quit:
		a = raw_input("What do you want to do? ")
		if a == "1": list_needs()
		if a == '2': list_purchases()
		if a == "3": 
			add_new_request()
		if a == '4': 
			log_purchase()
		if a == "$": print sum_purchases()
		if a == 'exit': 
			db.close()
			quit = True
	if quit: exit()

if __name__ == "__main__":
	do_it()
