from datetime import date
from datetime import timedelta
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from settings import *
from ytmusicapi import YTMusic
import json, random, requests, sys, time

try:
    filePath = sys.argv[1]  
except:
    print("Usage: python3 pywrapped.py takeout/yourname.json")
    quit()

# Initial config
try:
    wrFont = ImageFont.truetype("font/CircularStd-Book.otf", 46)
    wrFontBold = ImageFont.truetype("font/CircularStd-Medium.otf", 54)
except:
    print("Remember to download/add fonts to font/ directory!")
    quit()
bg = Image.open("img/bg.png")
imWidth = list(bg.size)[0]
imHeight = list(bg.size)[1]
printCoords = (100, (imHeight / 2) + 120)
artistImgCoords = (270, 270)

# Parse history and keep track of plays per artist
with open(filePath) as ytHistory:
    jsonHist = json.load(ytHistory)

mostListenedTo = {}

# Keep track of plays per song
for item in jsonHist:
    if item['header'] == 'YouTube Music':
        metadata = item['subtitles']
        metadata = metadata[0]
        artist = metadata['name']
        artist = artist.split(' - Topic')[0]
        songName = item['title'].split("Watched ")[1]
        if artist not in filteredArtists and artist in mostListenedTo:
            # This value could get huge if you listen to the same song(s) an absurd amount of times; nested dictionary might be better
            mostListenedTo[artist] += 1
        elif artist not in filteredArtists and artist not in mostListenedTo:
            mostListenedTo[artist] = 1

# Get top 5 artists and add to top five list
try:
    topfive = {}
    for k, _v in sorted(mostListenedTo.items(), key=lambda x: x[1], reverse=True)[:5]:
        currArtist = k.split(' - Topic')[0]
        if currArtist not in topfive.keys():
            topfive[currArtist] = []
except:
    print("This script assumes you have at least 5 different artists in your YouTube Music history!")
    quit()

# Get the YouTube ChannelID of top artist
topChannelId = None
for item in jsonHist:
    if item['header'] == 'YouTube Music':
        metadata = item['subtitles']
        metadata = metadata[0]
        artist = metadata['name']
        artist = artist.split(' - Topic')[0]
        if artist == list(topfive.keys())[0]:
            topChannelId = metadata['url'].split("/")[-1]
            break

# Inefficient but the values in topfive need to be filled with songs so...iterate through json again
for item in jsonHist:
    if item['header'] == 'YouTube Music':
        metadata = item['subtitles']
        metadata = metadata[0]
        artist = metadata['name']
        artist = artist.split(' - Topic')[0]
        songName = item['title'].split("Watched ")[1]
        if artist in topfive.keys():
            topfive[artist].append(songName)

# Get top songs
topsongs = []
for topartist in topfive.keys():
    topartistSongs = topfive[topartist]
    topsongs.append(max(set(topartistSongs), key=topartistSongs.count))

# Function to draw top five artists in column one and corresponding songs in column two
def draw_artists(printCoords):
    for idx, val in enumerate(topfive):
        toPrint = val
        if len(toPrint) > 15:
            toPrint = f"{toPrint[:12]}..."
        draw_text.text(printCoords, f"{idx + 1} {toPrint}", font=wrFontBold, fill=(238, 248, 87))
        printCoords = (printCoords[0], printCoords[1] + 80)

# Function to draw songs in column two
def draw_songs(printCoords):
    for idx, val in enumerate(topsongs):
        toPrint = val
        if len(toPrint) > 15:
            toPrint = f"{toPrint[:12]}..."
        draw_text.text(printCoords, f"{idx + 1} {toPrint}", font=wrFontBold, fill=(238, 248, 87))
        printCoords = (printCoords[0], printCoords[1] + 80)

# Function to probably maybe download an artist thumbnail using ytmusicapi
def get_thumbnail(artistChannelString):
    yt = YTMusic('headers.json')
    artist_results = yt.get_artist(artistChannelString)
    thumbs = artist_results['thumbnails']
    response = requests.get(thumbs[0]['url'])
    return BytesIO(response.content)

# Draw Top Artists column
draw_text = ImageDraw.Draw(bg)
artistColCoords = (list(wrFont.getsize("Top Artists"))[0], list(wrFont.getsize("Top Artists"))[1])# list(supportFontLg.getsize(firstMain))[0]
draw_text.text(printCoords, "Top Artists", font=wrFont, fill=(238, 248, 87))

# Update printCoords to account for size of Top Artists text block
printCoords = (printCoords[0], printCoords[1] + artistColCoords[1] + 40)

draw_artists(printCoords)

# Update printCoords to account for Top Songs starting position
printCoords = ((imWidth / 2) + 32, (imHeight / 2) + 120)

songColCoords = (list(wrFont.getsize("Top Songs"))[0], list(wrFont.getsize("Top Artists"))[1])
draw_text.text(printCoords, "Top Songs", font=wrFont, fill=(238, 248, 87))

# Update printCoords to account for size of Top Songs text block
printCoords = (printCoords[0], printCoords[1] + artistColCoords[1] + 40)

draw_songs(printCoords)

# Try to get and draw thumbnail in blank 540x540 box
if topChannelId:
    try:
        artistPhoto = get_thumbnail(topChannelId)
        loadedPhoto = Image.open(artistPhoto)
        artistImgCoords = (artistImgCoords[0], 540 - int(loadedPhoto.size[1] / 2))
        bg.paste(loadedPhoto, artistImgCoords)
    except:
        pass

bg.save(f"img/output_{int(time.time())}.png")