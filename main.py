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


def search_for_nepali_artists(access_token, limit=50, offset=0):
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

def main():
    access_token = get_access_token(client_id, client_secret)
    if access_token:
        total_artists = 0
        offset = 0
        artists = []
        while total_artists < 500:  # Adjust the desired number of artists
            nepali_artists = search_for_nepali_artists(access_token, limit=50, offset=offset)
            artists.extend(nepali_artists)
            total_artists += len(nepali_artists)
            offset += 50
            if len(nepali_artists) < 50:
                break
        save_artists_to_csv(artists, access_token)
    else:
        print("Failed to obtain access token.")

if __name__ == "__main__":
    main()
