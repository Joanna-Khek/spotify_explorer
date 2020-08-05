# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 23:27:09 2020

@author: Joanna Khek Cuina
"""
import json
import spotipy
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
import types
import os
from datetime import datetime, date


client_id= "CLIENT ID HERE"
client_secret = "CLIENT SECRET HERE"
username = "USERNAME HERE"
redirect_uri = "http://localhost:7777/callback/"

os.environ["SPOTIPY_CLIENT_ID"] = client_id
os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
os.environ["SPOTIPY_REDIRECT_URI"] = redirect_uri

scope = "user-read-recently-played"
token = util.prompt_for_user_token(username, scope)


# recently played
def current_user_recently_played(self, limit=50):
    return self._get('me/player/recently-played', limit=limit)

sp = spotipy.Spotify(auth=token)
sp.current_user_recently_played = types.MethodType(current_user_recently_played, sp)
data = sp.current_user_recently_played(limit=50)

def getTrackIds(data):
    ids = []
    for item in data["items"]:
        track = item["track"]
        ids.append(track["id"])
        
    return ids

track_ids = getTrackIds(data)


def getTrackFeatures(id_):
    meta = sp.track(id_)
    features = sp.audio_features(id_)
    
    # meta
    name = meta["name"]
    album = meta["album"]["name"]
    artist = meta["album"]["artists"][0]["name"]
    release_date = meta["album"]["release_date"]
    duration = meta["duration_ms"]
    popularity = meta["popularity"]
    
    # features
    danceability = features[0]["danceability"]
    energy = features[0]["energy"]
    key = features[0]["key"]
    loudness = features[0]["loudness"]
    mode = features[0]["mode"]
    speechiness = features[0]["speechiness"]
    acousticness = features[0]["acousticness"]
    instrumentalness = features[0]["instrumentalness"]
    liveness = features[0]["liveness"]
    valence = features[0]["valence"]
    tempo = features[0]["tempo"]
    time_signature = features[0]["time_signature"]
    
    track = [name, album, artist, release_date, duration, popularity, danceability, energy, key, loudness,
             mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature]
    return track

tracks = []
for ids in track_ids:
    track = getTrackFeatures(ids)
    tracks.append(track)
    
# save dataframe
final_data = pd.DataFrame(tracks, columns = ["name", "album", "artist", "release_date", "length", "popularity", 
                                             "danceability", "energy", "key", "loudness", "mode", "speechiness",
                                             "acousticness", "instrumentalness", "liveness", "valence",
                                             "tempo", "time_signature"])
final_data["scraped_on"] = date.today()
# write to file
to_csv_timestamp = datetime.today().strftime('%Y%m%d_%H%M%S')
# Define working path and filename
filename = to_csv_timestamp + '_spotify_data.csv'
final_data.to_csv(filename, index=False)
