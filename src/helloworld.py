import requests
from bs4 import BeautifulSoup
import re
import json
from secrets import spotify_token, spotify_user_id

def getAndParseURL(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return(soup)


full_lineup_results = getAndParseURL("https://www.okeechobeefest.com/lineup/")
artists = full_lineup_results.find_all(href=re.compile("#modal-lineup-artist"))

# artist_set to be used later to double-check if span texts are actually artists
artist_set = set()
for artist in artists:
    artist_set.add(''.join(artist.findAll(text=True)))

# loops from 1 -> 3
for x in range(1,4):
    print("")
    print("Day " + str(x) + " Results:")
    day_x_results = getAndParseURL("https://www.okeechobeefest.com/lineup/set-times/day-" + str(x) + "/")
    day_x_artists = day_x_results.find_all('span')

    day_x_set = set()
    for artist in day_x_artists:
        if artist.text in artist_set:
            day_x_set.add((artist.text).replace('(Live)', ''))

    # Creating a playlist for each day of 1-3 Okeechobee
    request_body = json.dumps({
        "name": "Okeechobee Festival Day " + str(x),
        "description": "Okeechobee Day " + str(x) +" Playlist",
        "public": True
    })

    query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
    response = requests.post(
        query,
        data=request_body,
        headers={
            "Content-Type":"application/json",
            "Authorization":"Bearer {}".format(spotify_token)
        }
    )
    response_json = response.json()
    playlist_id = response_json["id"]
    print("playlist id:" +str(playlist_id))

    for artist in day_x_set:
        # get the artist id to get the artists top tracks
        query = "https://api.spotify.com/v1/search?q={}&type=artist&limit=1".format(artist)
        artist_response = requests.get(
            query,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(spotify_token)
            }
        )

        res = artist_response.json()
        try:
            artist_id = res["artists"]["items"][0]["id"]
        except IndexError:
            artist_id = "skip_artist"

        if artist_id == "skip_artist" or artist_id == "25oLRSUjJk4YHNUsQXk7Ut":
            continue
        
        print("artist id: " + str(artist_id))

        #artists top tracks
        query = "https://api.spotify.com/v1/artists/{}/top-tracks?country=US".format(artist_id)
        top_tracks_response = requests.get(
            query,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(spotify_token)
            }
        )

        res = top_tracks_response.json()
        get_this_many_tracks = 3
        if len(res["tracks"]) < 3:
            get_this_many_tracks = len(res["tracks"])
        
        for y in range(get_this_many_tracks):
            print(res["tracks"][y]["uri"])
            song_uri = res["tracks"][y]["uri"]
            query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(playlist_id, song_uri)
            request_data = json.dumps(res["tracks"][y]["uri"])
            response = requests.post(
                query,
                headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
                }
            )





    

    