from datetime import date
from datetime import timedelta
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from settings import *
from ytmusicapi import YTMusic
import json, random, requests, sys, time

try:
    # Load Google Takeout file as json
    filePath = sys.argv[1]
    with open(filePath) as ytHistory:
        jsonHist = json.load(ytHistory)
except:
    print("Usage: python3 pywrapped.py takeout/yourname.json")
    quit()

# Function to draw a column (Top Artists, Top Songs)
def draw_column(printCoords, colToDraw):
    for idx, val in enumerate(colToDraw):
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

# Function to keep track of plays per song
def parse_songs(pathToLoadedJson):
    outDict = {}
    for item in pathToLoadedJson:
        if item['header'] == 'YouTube Music':
            metadata = item['subtitles']
            metadata = metadata[0]
            artist = metadata['name']
            artist = artist.split(' - Topic')[0]
            songName = item['title'].split("Watched ")[1]
            if artist not in filteredArtists and artist in outDict:
                outDict[artist].append(str(songName))
            elif artist not in filteredArtists and artist not in outDict:
                outDict[artist] = [songName]
    return top_five(outDict)

# Get top 5 artists and add to topfive list
def top_five(mostListenedToDict):
    topfiveDict = {}
    for k, v in sorted(mostListenedToDict.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
        currArtist = k.split(' - Topic')[0]
        topfiveDict[currArtist] = max(set(list(v)), key=v.count)
    return topfiveDict

mostListenedTo = parse_songs(jsonHist)
topfive = list(mostListenedTo.keys())
topsongs = list(mostListenedTo.values())

# Get the YouTube Music ChannelID of top artist
topChannelId = None
for item in jsonHist:
    if item['header'] == 'YouTube Music':
        metadata = item['subtitles']
        metadata = metadata[0]
        artist = metadata['name']
        artist = artist.split(' - Topic')[0]
        if artist == topfive[0]:
            topChannelId = metadata['url'].split("/")[-1]
            break

# Draw Top Artists column
draw_text = ImageDraw.Draw(bg)
artistColCoords = (list(wrFont.getsize("Top Artists"))[0], list(wrFont.getsize("Top Artists"))[1])
draw_text.text(printCoords, "Top Artists", font=wrFont, fill=(238, 248, 87))

# Update printCoords to account for size of Top Artists text block
printCoords = (printCoords[0], printCoords[1] + artistColCoords[1] + 40)

draw_column(printCoords, topfive)

# Update printCoords to account for Top Songs start position
printCoords = ((imWidth / 2) + 32, (imHeight / 2) + 120)

songColCoords = (list(wrFont.getsize("Top Songs"))[0], list(wrFont.getsize("Top Artists"))[1])
draw_text.text(printCoords, "Top Songs", font=wrFont, fill=(238, 248, 87))

# Update printCoords to account for size of Top Songs text block
printCoords = (printCoords[0], printCoords[1] + artistColCoords[1] + 40)

draw_column(printCoords, topsongs)

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