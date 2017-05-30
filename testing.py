from imageLib import *
from queries import *


cards = getUserProxyCards("lselig")
cardImageFiles = ["static/images/cardImages/" + card[3] + ".png" for card in cards]
print cardImageFiles
print cardImageFiles, len(cardImageFiles)
fillProxies(cardImageFiles)
