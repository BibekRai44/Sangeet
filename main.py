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


def search_for_nepali_artist(access_token, limit=50, offset=0):
    search_url="https://api.spotify.com/v1/search"
    headers={
        "Authorization":f"Bearer {access_token}"
    }
    parmas={
        "q":"country:Nepal",
        "type":"artist",
        "limit":limit,
        "offset":offset
    }

    response=requests.get(search_url, headers=headers, params=parmas)
    nepali_artists=response.json().get("artists", {}).get("items", [])
    return nepali_artists

def get_artist_followers(artist_id, access_token):
    followers_url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(followers_url, headers=headers)
    followers_count = response.json().get("followers", {}).get("total", "")
    return followers_count

def save_artists_to_csv(artists, access_token):
    with open("nepali_artists_info.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Artist Name", "Genres", "Popularity", "Followers Count"])
        for artist in artists:
            artist_name = artist["name"]
            genres = ", ".join(artist.get("genres", []))
            popularity = artist.get("popularity", "")
            artist_id = artist["id"]
            followers_count = get_artist_followers(artist_id, access_token)
            writer.writerow([artist_name, genres, popularity, followers_count])

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