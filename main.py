import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "YOUR-CLIENT-ID"
CLIENT_SECRET = "YOUR-CLIENT-SECRET"

# ================================== Requests to billboard.com and get the data ==================================

URL = "https://www.billboard.com/charts/hot-100"
date = input("Which year do you want to travel to? type the date in this format YYYY-MM-DD: ")

response = requests.get(url=f"{URL}/{date}")
website_html = response.text

soup = BeautifulSoup(website_html, "lxml")

songs_lists = soup.find_all(name="span", class_="chart-element__information__song")
song_names = [song.getText() for song in songs_lists]

# ================================== Requests to spotify and get token.txt ==================================

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

# ================================== Search for songs ==================================

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# ================================== Create and Update a playlist ==================================

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
