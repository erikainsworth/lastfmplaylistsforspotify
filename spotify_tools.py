import sys
import os
import itertools
import tekore as tk
import spt_authorize

import pylistenbrainz

def authorize():
	try:
		conf = tk.config_from_file(config_file, return_refresh=True)
		token = tk.refresh_pkce_token(conf[0], conf[3])
		tk.config_to_file(config_file, conf[:3] + (token.refresh_token,))
	except:
		client_secret = 'your_client_secret'
		redirect_uri = 'https://example.com/callback'   # Or your redirect uri
		conf = (client_id, client_secret, redirect_uri)		
		token = tk.prompt_for_pkce_token(client_id, redirect_uri, scope=tk.scope.every)
		tk.config_to_file(config_file, conf + (token.refresh_token,))
	return tk.Spotify(token)

def get_user():
	return spotify.current_user()	
	
def get_saved_albums():
	albums = spotify.all_items(spotify.saved_albums())
	return albums

def get_album_track_uris(album):
	uri_list = [item.uri for item in spotify.all_items(album.tracks)]
	return uri_list	
	
def get_playlist(name):
	playlist_gen = spotify.all_items(spotify.playlists(user.id))
	for pl in playlist_gen:
		if pl.name == name:
			return pl.id
	# playlist doesn't exist, so create
	return create_play_list(name)	

def create_play_list(name):
	pl = spotify.playlist_create(user.id, name, public=False, description='just testing')
	return pl.id
	
def add_to_playlist(playlist_id, uris):
	spotify.playlist_add(playlist_id, uris, position=None)

def clear_playlist(playlist_id):
	spotify.playlist_clear(playlist_id)

def create_all_songs_playlist():
	playlist_id = get_playlist('all songs')	
	albums = get_saved_albums()
	
	clear_playlist(playlist_id)
	for a in albums:
		uri_list = get_album_track_uris(a.album)
		print(uri_list)
		add_to_playlist(playlist_id, uri_list)
	
def store_user_library():
	saved_albums_file = os.path.sep.join([os.path.dirname(__file__), 'saved_albums.txt'])
	album_gen = get_saved_albums()
	#with open(saved_albums_file, 'w') as album_file:
#		album_file.writelines(a.album.id + '\n' for a in album_gen)
		
	saved_playlist_file = os.path.sep.join([os.path.dirname(__file__), 'saved_playlists`.txt'])
	playlist_gen = spotify.all_items(spotify.playlists(user.id))
	for pl in playlist_gen:
		playlist_items = spotify.all_items(spotify.playlist_items(pl.id))
		print(list(itertools.islice(playlist_items, 1)))
		
	#with open(saved_playlist_file, 'w') as playlist_file:
	#	playlist_file.writelines(pl.name + '\n' for pl in playlist_gen)
	
	# TODO 
	# store tracks in playlists as json
	# make configurable,, i.e. provide input to specify which items should be save (albums, tracks, playlists)
	
	

def set_user_library():
	pass
	
	#TODO
	# follow artists: https://tekore.readthedocs.io/en/stable/examples/artist_follower.html
		
		
def get_lb_listens(name):
	listens = lb_client.get_listens(username=name)
	for listen in listens:
		print("Track name:", listen.track_name)
		print("Artist name:", listen.artist_name)
		
def get_lb_recordings(name):
	listens = lb_client.get_user_recordings(username=name)
	for listen in listens:
		print(listen)

if __name__ == '__main__':
	spotify = spt_authorize.authorize()
	user = get_user()
	print(dir(user))
	#store_user_library()
	
	#lb_client = pylistenbrainz.ListenBrainz()
	#get_lb_recordings('erik.ainsworth@gmail.com')

	
# TODO:
# Create Most played tracks based on lastFM
# Create Least played tracks based on lastFM
# Create recommended tracks based on lastFM
# create loved tracks based on ListenBrainz
# Migrate library to other user
