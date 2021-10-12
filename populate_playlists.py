import sys
import os
from lxml import etree

for filename in os.listdir(sys.argv[1]):
    if not filename.endswith(".html"):
        continue
    file = open(filename, 'r', encoding="utf8")
    tree = etree.HTML(file.read())
    songs = tree.xpath("/html[@class='inactive-player no-focus-outline']/body/ytmusic-app/ytmusic-app-layout[@id='layout']/div[@id='content']/ytmusic-browse-response[@id='browse-page']/ytmusic-section-list-renderer[@class='style-scope ytmusic-browse-response']/div[@id='contents']/ytmusic-playlist-shelf-renderer[@class='style-scope ytmusic-section-list-renderer']/div[@id='contents']/ytmusic-responsive-list-item-renderer[@class='style-scope ytmusic-playlist-shelf-renderer']/div[@class='flex-columns style-scope ytmusic-responsive-list-item-renderer']/div[@class='title-column style-scope ytmusic-responsive-list-item-renderer']/yt-formatted-string[@class='title style-scope ytmusic-responsive-list-item-renderer complex-string']/a[@class='yt-simple-endpoint style-scope yt-formatted-string']")
    artists = tree.xpath("/html[@class='inactive-player no-focus-outline']/body/ytmusic-app/ytmusic-app-layout[@id='layout']/div[@id='content']/ytmusic-browse-response[@id='browse-page']/ytmusic-section-list-renderer[@class='style-scope ytmusic-browse-response']/div[@id='contents']/ytmusic-playlist-shelf-renderer[@class='style-scope ytmusic-section-list-renderer']/div[@id='contents']/ytmusic-responsive-list-item-renderer[@class='style-scope ytmusic-playlist-shelf-renderer']/div[@class='flex-columns style-scope ytmusic-responsive-list-item-renderer']/div[@class='secondary-flex-columns style-scope ytmusic-responsive-list-item-renderer']/yt-formatted-string[@class='flex-column style-scope ytmusic-responsive-list-item-renderer complex-string'][1]")
    write_file = open(filename[:-5], 'w', encoding="utf8")
    for i in range(0, len(songs) - 1):
        print(songs[i].text, file=write_file)
        print(artists[i].get('title'), file=write_file)