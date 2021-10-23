import os
import sys
import json
import re

from pprint import pprint

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

playlists_json_file = 'playlists.json'

def load():
    """
    Load all playlists data using Youtube Data API for a authenticated user (using Client ID secrets file)
    and save it into a JSON file
    """
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    api_service_name = 'youtube'
    api_version = 'v3'
    client_secrets_file = 'C:/Users/Igor/Desktop/Playlists/GOOGLE/client_secret_1042753516680-9ht74l6b9c573g69v9jbimdbjdvv9dbj.apps.googleusercontent.com.json'

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, ['https://www.googleapis.com/auth/youtube.readonly'])
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlists().list(
        part='snippet',
        maxResults=1000,
        mine=True
    )
    yt_playlists = request.execute()
    playlists = {}
    for yt_playlist_id in yt_playlists['items']:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=yt_playlist_id['id'],
            maxResults=1000,
        )
        yt_playlist = request.execute()

        playlist = []
        for yt_track in yt_playlist['items']:
            playlist.append({'title': yt_track['snippet']['title'], 'artist': yt_track['snippet']['videoOwnerChannelTitle'][:-8]})

        playlists[yt_playlist_id['snippet']['title']] = playlist

    playlists_json = json.dumps(playlists, indent=4)
    with open(playlists_json_file, 'w') as file:
        print(str(playlists_json), file=file)
    
def manage():
    """
    Read playlists data from JSON file, and then
    print instructions for user to remove track duplicates across different playlists.
    The playlist with the least count of tracks retains the track, other duplicates are removed.
    """
    with open(playlists_json_file, 'rb') as playlists_json:
        playlists = json.load(playlists_json)

#    Remove text in parentheses from track titles since some of the tracks may contain "(radio edit)" or similar
#    for playlist_name, playlist in playlists.items():
#        for track in playlist:
#            track['title'] = re.sub(r"\(.*\)", "", track['title']).strip()
        
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
                for track_compare in playlist:
                    if track_compare['title'] == track['title'] and track_compare['artist'] == track['artist']:
                        playlists_with_dupl.append({'name':playlist_name, 'playlist': playlist})
                        
            playlists_with_dupl_sorted = sorted(playlists_with_dupl, key = lambda i: (len(i['playlist'])))
            for entry in playlists_with_dupl_sorted[1:]:
                result.append('remove from {} track {}'.format(entry['name'], track))
                entry['playlist'].remove(track)
                
    for cmd in sorted(result):
        print(cmd)
    
if __name__ == '__main__':
    """
    'load' - Load playlists from Youtube Data API
    Any other arguments - manage playlists
    """
    if len(sys.argv) > 1 and sys.argv[1] == 'load':
        load()
    else:
        manage()