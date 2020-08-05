# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 18:17:35 2020

@author: Joanna Khek Cuina
"""
import sys
import json
import spotipy
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import urllib
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
import types
import os
from datetime import datetime, date
import codecs
import requests
import urllib.request
from urllib.request import urlretrieve
from urllib.error import HTTPError
from urllib.request import urlopen


client_id= "99b86d2bfe254365903f0c334fb2cf03"
client_secret = "1294d3c8eecb4611944644862b88b992"
redirect_uri = "http://localhost:7777/callback/"
username = ""
    
os.environ["SPOTIPY_CLIENT_ID"] = client_id
os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
os.environ["SPOTIPY_REDIRECT_URI"] = redirect_uri

scope = "user-library-read user-top-read"
token = util.prompt_for_user_token(username = username,
                                   scope = scope,
                                   client_id = client_id,
                                   client_secret = client_secret,
                                   redirect_uri = redirect_uri)

sp = spotipy.Spotify(auth=token)

# creating a list of favorite artists
# URI (Uniform Resource Indicator)
def aggregate_top_artists(sp):
    top_artists_name = []
    top_artists_uri = []
    top_artists_image = []
    
    long_top_artists_name = []
    long_top_artists_uri = []
    long_top_artists_image = []
    
    ranges = ["short_term"]
    for r in ranges:
        top_artists_all_data = sp.current_user_top_artists(limit=50, time_range=r)
        top_artists_data = top_artists_all_data["items"]
        for artists_data in top_artists_data:
            top_artists_name.append(artists_data["name"])
            top_artists_uri.append(artists_data["uri"])
            top_artists_image.append(artists_data["images"][1]["url"])   
            
    short_top_artists = pd.DataFrame()
    short_top_artists["name"] = top_artists_name
    short_top_artists["uri"] = top_artists_uri
    short_top_artists["image"] = top_artists_image
            
    ranges = ["long_term"]
    for r in ranges:
        top_artists_all_data = sp.current_user_top_artists(limit=50, time_range=r)
        top_artists_data = top_artists_all_data["items"]
        for artists_data in top_artists_data:
            long_top_artists_name.append(artists_data["name"])
            long_top_artists_uri.append(artists_data["uri"])
            long_top_artists_image.append(artists_data["images"][1]["url"])
            
    long_top_artists = pd.DataFrame()
    long_top_artists["name"] = long_top_artists_name
    long_top_artists["uri"] = long_top_artists_uri
    long_top_artists["image"] = long_top_artists_image
                
    return short_top_artists, long_top_artists

                
# for each of the artists, get all tracks for each artists
def aggregate_top_tracks(sp):
    top_tracks_uri = []
    top_tracks_name = []
    top_tracks_image = []
    
    long_top_tracks_uri = []
    long_top_tracks_name = []
    long_top_tracks_image = []
    
    ranges = ["short_term"]
    for r in ranges:
        top_tracks_all_data = sp.current_user_top_tracks(limit=50, time_range=r)
        top_track_data = top_tracks_all_data["items"]
        for tracks in top_track_data:
            if tracks["name"] not in top_track_data:
                top_tracks_name.append(tracks["name"])
                top_tracks_uri.append(tracks["uri"])
                top_tracks_image.append(tracks["album"]["images"][1]["url"]) 
                
    short_top_tracks = pd.DataFrame()
    short_top_tracks["title"] = top_tracks_name
    short_top_tracks["uri"] = top_tracks_uri
    short_top_tracks["image"] = top_tracks_image
            
    ranges = ["long_term"]
    for r in ranges:
        top_tracks_all_data = sp.current_user_top_tracks(limit=50, time_range=r)
        top_track_data = top_tracks_all_data["items"]
        for tracks in top_track_data:
            if tracks["name"] not in top_track_data:
                long_top_tracks_name.append(tracks["name"])
                long_top_tracks_uri.append(tracks["uri"])
                long_top_tracks_image.append(tracks["album"]["images"][1]["url"])
                
    long_top_tracks = pd.DataFrame()
    long_top_tracks["title"] = long_top_tracks_name
    long_top_tracks["uri"] = long_top_tracks_uri
    long_top_tracks["image"] = long_top_tracks_image
                
    return short_top_tracks, long_top_tracks


# get the track id
def get_track_id(data):
    new_id = []
    for track_string in data["uri"]:
        new_id.append(track_string.split("spotify:track:")[1])
    data["track_id"] = new_id
    return data


# get track features
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
    track_id = meta["id"]
    
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
    
    track = [name, album, artist, track_id, release_date, duration, popularity, danceability, energy, key, loudness,
             mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature]
    return track


# save into dataframe
def save(tracks, name):
    track_details = []
    for ids in tracks:
        track = getTrackFeatures(ids)
        track_details.append(track)
        
    final_data = pd.DataFrame(track_details, columns = ["name", "album", "artist", "track_id", "release_date", "length", "popularity", 
                                                        "danceability", "energy", "key", "loudness", "mode", "speechiness",
                                                        "acousticness", "instrumentalness", "liveness", "valence",
                                                        "tempo", "time_signature"])
    
    #final_data.to_csv(name+".csv", index=False)
    return final_data


# get artists info (short term and long term)
short_top_artists, long_top_artists = aggregate_top_artists(sp)
short_top_artists.to_csv("short_top_artists.csv", index=False)
long_top_artists.to_csv("long_top_artists.csv", index=False)

# get tracks (short term and long term)
short_top_tracks, long_top_tracks = aggregate_top_tracks(sp)

# get the track IDs
short_top_tracks = get_track_id(short_top_tracks)
long_top_tracks = get_track_id(long_top_tracks)

# get the track features
short_track_details = save(short_top_tracks["track_id"], "short_track_details")
long_track_details = save(long_top_tracks["track_id"], "long_track_details")

# merge details and name
df_short_track = pd.merge(short_top_tracks, short_track_details, left_on="track_id", right_on="track_id", how="left")
df_long_track = pd.merge(long_top_tracks, long_track_details, left_on="track_id", right_on="track_id", how="left")
df_short_track["clean_image"]= df_short_track["image"].apply(lambda x: x.split("/")[-1])
df_long_track["clean_image"]= df_long_track["image"].apply(lambda x: x.split("/")[-1])

cols = ['title', 'uri', 'image', 'clean_image', 'track_id', 'name', 'album', 'artist',
       'release_date', 'length', 'popularity', 'danceability', 'energy', 'key',
       'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
       'liveness', 'valence', 'tempo', 'time_signature']
df_short_track = df_short_track[cols]
df_long_track = df_long_track[cols]

df_short_track.to_csv("df_short_track.csv", index=False)
df_long_track.to_csv("df_long_track.csv", index=False)

# # download artists and track image
# list_ = [short_top_artists, long_top_artists, df_short_track, df_long_track]
# for data in list_:
#     for link in data["image"]:
#         urlretrieve(link, "C:\\Users\\joann\\OneDrive\\Desktop\\My Files\\Data Science\\Projects\\Spotify\\static\\images\\"+ link.split("/")[-1] + ".png")
