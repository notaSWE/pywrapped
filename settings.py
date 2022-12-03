from PIL import Image, ImageFont

FONT_ONE = "font/CircularStd-Book.otf"
FONT_TWO = "font/CircularStd-Medium.otf"

try:
    wrFont = ImageFont.truetype(FONT_ONE, 46)
    wrFontBold = ImageFont.truetype(FONT_TWO, 54)
except:
    print("Remember to download/add fonts to font/ directory!")
    quit()

bg = Image.open("img/bg.png")
imWidth = list(bg.size)[0]
imHeight = list(bg.size)[1]
printCoords = (100, (imHeight / 2) + 120)
artistImgCoords = (270, 270)

# Filtered artists
filteredArtists = ['Original Soundtrack']