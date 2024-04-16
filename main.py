from dotenv import load_dotenv
import os
import base64
from requests import post,get
import json
import csv
import requests

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_access_token(client_id, client_secret):
    auth_str=f"{client_id}:{client_secret}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()

    token_url="https://accounts.spotify.com/api/token"
    headers = {
        "Authorization":f"Basic {auth_b64}",
        
    }
    data={"grant_type":"client_credentials"}
    response=requests.post(token_url, headers=headers, data=data)
    token_data = response.json()
    access_token = token_data.get("access_token")
    return access_token

def get_auth_header(token):
    return {"Authorization":"Bearer "+token}

def search_for_artist(token, artist_name):
    url="https://api.spotify.com/v1/search"
    headers=get_auth_header(token)
    query=f"?q={artist_name}&type=artist&limit=1"

    query_url=url+query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    if len(json_result)==0:
        print("No artist found with such name")
        return None
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url=f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=NP"
    headers=get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result

def get_artist_albums(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?limit=50"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['items']
    return json_result

def get_album_tracks(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['items']
    return json_result

def save_artist_albums_to_csv(artist_name, albums):
    with open(f"{artist_name}_albums.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Album Name', 'Album ID'])
        for album in albums:
            writer.writerow([album['name'], album['id']])

def save_album_tracks_to_csv(album_name, tracks):
    with open(f"{album_name}_tracks.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Track Name', 'Track ID'])
        for track in tracks:
            writer.writerow([track['name'], track['id']])


token = get_token()
result=search_for_artist(token, "Sabin Rai")
if result:
    artist_id = result['id']
    albums = get_artist_albums(token, artist_id)
    for album in albums:
        album_name = album['name']
        album_id = album['id']
        save_album_tracks_to_csv(album_name, get_album_tracks(token, album_id))
    save_artist_albums_to_csv("Sabin_Rai", albums)
        #tracks = get_album_tracks(token, album_id)
        #print("Tracks:")
        #for idx, track in enumerate(tracks):
            #print(f"{idx+1}. {track['name']}")
#artist_id=result['id']
#songs=get_songs_by_artist(token, artist_id)

#for idx,song in enumerate(songs):
    #print(f"{idx+1}. {song['name']}")