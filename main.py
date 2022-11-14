import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from bs4 import BeautifulSoup


Client_ID = "d2ca5a2a90ba40e19bb9c54aa69a4990"
Client_Secret = "05eb7c211d04488389611a8089b7b9a0"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

year = input("What year would you like to travel?, type the date in this format YYYY-MM-DD: ")
URL = "https://www.billboard.com/charts/hot-100/"

response = requests.get(URL + year)
soup = BeautifulSoup(response.text, "html.parser")

title = soup.find_all(name="h3", class_="a-no-trucate", id="title-of-a-story")
title_list = [song.getText().strip() for song in title]

# Searching Spotify for songs by title

song_uris = []
year = year.split("-")[0]
for song in title_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating a new private playlist in Spotify

playlist = sp.user_playlist_create(user=user_id, name=f"{year} Billboard 100", public=False)
print(playlist)

# Adding songs found into the new playlist

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
