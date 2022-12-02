import json

# Tests ./headers.json; read the docs
# https://ytmusicapi.readthedocs.io/en/stable/setup.html

from ytmusicapi import YTMusic
yt = YTMusic('headers.json')
search_results = yt.search('The Midnight Nocturnal')
for item in search_results:
	if 'duration' in item.keys() and item['duration']:
		print(json.dumps(item))
