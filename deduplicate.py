import sys
import os

def file_to_playlist(file):
    playlist=[]
    count=0
    song=""
    artist=""
    for line in file:
        if len(line.strip()) == 0:
            continue
            
        if int(count % 2) == 0:
            song = line.strip()
        else:
            artist = line.strip()
            playlist.append({"song": song, "artist": artist})
        count += 1
    return playlist

playlists={}
for filename in os.listdir(sys.argv[1]):
    file = open(filename, 'r', encoding="utf8")
    playlists[filename] = file_to_playlist(file)
    
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