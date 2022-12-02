# pywrapped
spotify wrapped for the few youtube music users out there

## Why?

End of year FOMO every time my friends post their Spotify wrapped

## How?

I'm stubborn and like writing Python

## Installation/configuration

0. Install and configure [ytmusicapi](https://github.com/sigma67/ytmusicapi)
    1. Pay special attention to the setup; you __need headers.json__ in order to download artist photos!
1. Export the json from [Google Takeout](https://takeout.google.com) - you ONLY need YouTube/YouTube music!
    1. Save the file as __yourname__.json
    ![Google Takeout 01](/img/takeout01.JPG "This is a sample output file")
    ![Google Takeout 02](/img/takeout02.JPG "This is a sample output file")
2. Git clone this repo
3. Copy the export from step 1 into __takeout/__
    1. Relative path should be __takeout/yourname.json__ 
4. Download a cool font or two and save the .ttf file(s) in __font/__
    1. Relative path should be __font/fontname.otf__
    2. Note, I Googled and downloaded Circular into __font/CircularStd-Medium.otf__ and __font/CircularStd-Book.otf__
    2. Update the font config in __pywrapped.py__ (lines 15 and 16) if your font filenames are different!
5. __python3 pywrapped.py takeout/yourname.json__
    1. Images will output to **img/output_unixtimestamp.png**

## Standard output

![Demo output](/img/sample.png "This is a sample output file")

## Fonts links (external)

* [Google (Circular font)](https://www.google.com)

## Notes

* This is very similar to [pyinstafest](https://github.com/notaSWE/pyinstafest)
* If there are bands/artists you don't want, simply add them to the __filteredArtists__ list in __settings.py__
