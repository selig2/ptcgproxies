import sqlite3

def insertUser(signupHash):
	# @ desc takes in the signupHash returned from the signup form and inserts that user into the database
	# @ param signupHash the hash map returned from the signup form
	# @ return none 
	conn = sqlite3.connect("pokemontcg.db")
	cur = conn.cursor()

	query = "INSERT INTO User(email, username, password) VALUES(?, ?, ?)"
	cur.execute(query, (signupHash["email"], signupHash["username"], signupHash["password"]))

	conn.commit()
	conn.close()


def insertUserProxyCard(username, api_card_id):
	# @ desc takes in the username for the current user of the site and the card they want to proxy and inserts that pair into userProxy
	# @ param username the username of the current user
	# @ param api_card_id the id of the card they want to proxy
	# @ return none

	conn = sqlite3.connect("pokemontcg.db")
	cur = conn.cursor()

	query = "SELECT user_id FROM User WHERE username = ?"
	cur.execute(query, (username,))
	user_id = cur.fetchone()[0]

	query = "INSERT INTO userProxies(user_id, api_card_id) VALUES(?, ?)"
	cur.execute(query, (user_id, api_card_id))

	conn.commit()
	conn.close()

def removeUserProxyCard(username, api_card_id):
	# @ desc takes in the username for the current user of the site and the card they want to proxy and inserts that pair into userProxy
	# @ param username the username of the current user
	# @ param api_card_id the id of the card they want to proxy
	# @ return none

	conn = sqlite3.connect("pokemontcg.db")
	cur = conn.cursor()

	query = "SELECT user_id FROM User WHERE username = ?"
	cur.execute(query, (username,))
	user_id = cur.fetchone()[0]

	query = "DELETE FROM userProxies WHERE user_id = ? AND api_card_id = ? LIMIT 1"
	cur.execute(query, (user_id, api_card_id))

	conn.commit()
	conn.close()



# ----------------------------------------------------- #

def getAllCards():
	# @ desc goes through the cards table
	# @ returns all cards in a tuple format for the table
	conn = sqlite3.connect("pokemontcg.db")
	cur = conn.cursor()
	query = "SELECT name, card_set, card_id, api_card_id, imageURL FROM Card WHERE card_set = ?"
	cur.execute(query, ("Guardians Rising",))
	results = cur.fetchall()
	conn.close()
	return results

def getUserProxyCards(username):
	# @ desc gets the cards that the user has chosen to proxy
	# @ param username the username of the current user
	# @ returns all cards in a tuple format for the table

	conn = sqlite3.connect("pokemontcg.db")
	cur = conn.cursor()

	query = "SELECT user_id FROM User WHERE username = ?"
	cur.execute(query, (username,))
	user_id = cur.fetchone()[0]

	query = "SELECT api_card_id FROM userProxies WHERE user_id = ?"
	cards = [card[0] for card in cur.execute(query, (user_id,)).fetchall()]
	results = []
	for card in cards:
		query = "SELECT name, card_set, card_id, api_card_id FROM Card WHERE api_card_id = ?"
		cur.execute(query, (card,))
		results.append(cur.fetchone())
	conn.close()
	print "RESULTS: ", results
	return results

def removeUserProxyCards(username):
	# @ desc removes all cards that the user has chosen to proxy from their list in the db
	# @ param username the username of the current user
	# @ returns empty list

	conn = sqlite3.connect("pokemontcg.db")
	cur = conn.cursor()

	query = "SELECT user_id FROM User WHERE username = ?"
	cur.execute(query, (username,))
	user_id = cur.fetchone()[0]

	query = "DELETE FROM userProxies WHERE user_id = ?"
	cur.execute(query, (user_id,))
	conn.commit()
	conn.close()
	return []



