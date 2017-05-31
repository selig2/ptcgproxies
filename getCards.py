import requests, sqlite3



def saveCardImage(picUrl, saveName):
	# @ desc downloads the card image at url
	# @ param picUrl the url that contains the image
	# @ param saveName the name that you want to save the image as
	print("SAVING:", saveName)
	imageData = requests.get(picUrl).content
	with open("static/images/hiresCardImages/" + saveName, "wb") as imageFile:
		imageFile.write(imageData)


def saveAllCardImages():
	# @ desc loops over all cards from all sets and downloads the image for the car
	# @ return none
	print ("hello")
	url = "https://api.pokemontcg.io/v1/sets"
	response = requests.get(url, verify = "/etc/ssl/cert.pem")


	sets = response.json()

	totalCards = 0
	for s in sets["sets"]:
		cardsInSet = s["totalCards"]
		print(s["series"], cardsInSet, s["code"])
		totalCards += s["totalCards"]
		for i in range(1, cardsInSet + 1):
			url = "https://api.pokemontcg.io/v1/cards/" + s["code"] + "-" + str(i)
			response = requests.get(url, verify = "/etc/ssl/cert.pem")
			card = response.json()
			if("status" in card):
				print (card, s["code"], i, "FAILED")
			else:
				cardImage = card["card"]["imageUrlHiRes"]
				saveCardImage(cardImage, card["card"]["id"] + "_hires" + ".png")
				print (card, s["code"], i, "PASSED")

def insertAllCards():
	# @ desc loops over all cards and inserts them into the database where appropriate
	# @ return none
	url = "https://api.pokemontcg.io/v1/sets"
	response = requests.get(url, verify = "/etc/ssl/cert.pem")
	card_id = 0
	sets = response.json()

	conn = sqlite3.connect("pokemontcg.db")
	cur = conn.cursor()

	for s in sets["sets"]:
		cardsInSet = s["totalCards"]
		if(s["code"] == "sm2"):
			for i in range(1, cardsInSet + 1):
				url = "https://api.pokemontcg.io/v1/cards/" + s["code"] + "-" + str(i)
				response = requests.get(url, verify = "/etc/ssl/cert.pem")
				card = response.json()
				if("status" in card):
					print (card, s["code"], i, "FAILED")
				else:
					cardType = card["card"]["supertype"]
					print(cardType)
					# if(cardType == "Pokémon"):
					insertPokemonCard(card_id, card, cur)
					card_id += 1

	conn.commit()
	conn.close()

def insertPokemonCard(card_id, card, cur):
	# @ desc inserts the card and all of it's attributes into the database
	# @ param card the dictionary of info for the card
	# @ param cur the cursor for the datbase
	# assert(card["card"]["supertype"] == "Pokémon")
	card = card["card"]
	print (card)
	attributes = ["id", "name", "artist", "rarity", "series", "set", "text", "imageUrl", "imageUrlHiRes"]

	params = [card_id]
	for attr in attributes:
		if(attr in card):
			if(attr == "text"):
				params.append("_".join(card[attr]))
			else:
				params.append(card[attr])
		else:
			params.append(None)

	query = "INSERT INTO Card(card_id, api_card_id, name, artist, rarity, series, card_set, card_text, imageURL, imageURL_hires) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
	cur.execute(query, tuple(params))

	# attributes = ["subtype", "hp", "evolvesFrom", "nationalPokedexNumber"]
	# params = [card_id]
	# for attr in attributes:
	# 	if(attr in card):
	# 		params.append(card[attr])
	# 	else:
	# 		params.append(None)
	# query = "INSERT INTO Pokemon(card_id, subtype, hp, evolves_from, pokedex_number) VALUES(?, ?, ?, ?, ?)"
	# cur.execute(query, tuple(params))


	# if("attacks" in card):
	# 	for attack in card["attacks"]:
	# 		params = []
	# 		attributes = ["cost", "text", "damage", "name", "convertedEnergyCost"]
	# 		for attr in attributes:
	# 			if(attr in attack):
	# 				if(attr == "cost"):
	# 					params.append("_".join(attack[attr]))
	# 				else:
	# 					params.append(attack[attr])
	# 			else:
	# 				params.append(None)

	# 		query = "INSERT INTO Attacks(cost, attack_text, damage, name, converted_cost) VALUES (?, ?, ?, ?, ?)"
	# 		cur.execute(query, tuple(params))

	# 		query = "SELECT attack_id FROM Attacks WHERE cost = ? AND attack_text = ? and damage = ? and name = ? and converted_cost = ?"
	# 		cur.execute(query, tuple(params))
	# 		attack_id = cur.fetchone()[0]

	# 		query = "INSERT INTO hasAttack(attack_id, card_id) VALUES(?, ?)"
	# 		cur.execute(query, (attack_id, card_id))


saveAllCardImages()
# insertAllCards()