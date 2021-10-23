# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlists.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import sys
import json

from pprint import pprint

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def yt_api():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "C:/Users/Igor/Desktop/Playlists/GOOGLE/client_secret_1042753516680-9ht74l6b9c573g69v9jbimdbjdvv9dbj.apps.googleusercontent.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlists().list(
        part="snippet",
        maxResults=1000,
        mine=True
    )
    yt_playlists = request.execute()
    playlists = {}
    for yt_playlist_id in yt_playlists["items"]:
        # print("id: {}, title: {}".format(yt_playlist_id["id"], yt_playlist_id["snippet"]["title"]))
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=yt_playlist_id["id"],
            maxResults=1000,
        )
        yt_playlist = request.execute()

        playlist = []
        for yt_track in yt_playlist["items"]:
            playlist.append({"song": yt_track["snippet"]["title"], "artist": yt_track["snippet"]["videoOwnerChannelTitle"][:-8]})
            # print("id: {}, title: {}".format(yt_track["snippet"]["title"], yt_track["snippet"]["videoOwnerChannelTitle"][:-8]))

        playlists[yt_playlist_id["snippet"]["title"]] = playlist

    j = json.dumps(playlists, indent=4)
    print(str(j))
    
def file():
    with open("playlists.json", 'rb') as playlists_json:
        playlists = json.load(playlists_json)
        
    all_tracks = []
    for playlist_name, playlist in playlists.items():
        for track in playlist:
            all_tracks.append(track)

    seen = set()
    result = []
    for track in all_tracks:
        if frozenset(track.items()) not in seen:
            seen.add(frozenset(track.items()))
        else:
            playlists_with_dupl = []
            for playlist_name, playlist in playlists.items():
                for t in playlist:
                    if t["song"] == track["song"] and t["artist"] == track["artist"]:
                        playlists_with_dupl.append({"name":playlist_name, "playlist": playlist})
                        
            playlists_with_dupl_sorted = sorted(playlists_with_dupl, key = lambda i: (len(i['playlist'])))
            for entry in playlists_with_dupl_sorted[1:]:
                result.append('remove from {} track {}'.format(entry["name"], track))
                entry["playlist"].remove(track)
                
    for cmd in sorted(result):
        print(cmd)
        
    # pprint(playlists)
    
if __name__ == "__main__":
    file()