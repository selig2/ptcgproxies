from PIL import Image
import os, math
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.utils import ImageReader


def resize(infile):
	# @ desc resizes an image to be 240 x 335, the size of a pokemon card
	# @ param infile the path to the image file
	# @ return none

	newSize = (350, 489)
	im = Image.open(infile)
	im.thumbnail(newSize, Image.ANTIALIAS)
	im.save(infile, "png")


# for image in os.listdir("static/images/hiresCardImages/"):
# 	if(image[0] != "."):
# 		print image
# 		resize("static/images/hiresCardImages/" + image)
	
def chunkify(cardList):
	# @ desc takes the cards that the user has selected and splits their list into chucks of at most 9
	# @ return 
	return [cardList[i:i + 9] for i in xrange(0, len(cardList), 9)]


def createCanvas(numCards):
	# @ desc creates an empty canvas
	# @ return the empty canvas
	xDim = 240 * 3
	yDim = 335 * 3
	# print xDim, yDim, numCards
	canvas = Image.new('RGB', (xDim, yDim), (255, 255, 255)) #creates a new empty image, RGBA mode
	return canvas


def fillProxies(cardList):
	# @ desc creates the files that the user ends up printing out
	# @ param a list of card file paths
	# @ return a list of image files that the user can print out

	retPages = []

	chunks = chunkify(cardList)
	c = canvas.Canvas('proxies.pdf')
	for chunk in chunks:
		x_offset = 0
		y_offset = 0
		page = createCanvas(len(cardList))

		for i, card in enumerate(chunk):
			cardImage = Image.open(card)

			if(i % 3 == 0 and i != 0): # need to move down
				y_offset += cardImage.size[1]
				x_offset = 0

			page.paste(cardImage, (x_offset, y_offset))
			x_offset += cardImage.size[0]

		myPage = ImageReader(page)
		c.drawImage(myPage, 0, 0, 2.5*3*inch, 3.5*3*inch)
		c.showPage()
	c.save()
	return retPages
