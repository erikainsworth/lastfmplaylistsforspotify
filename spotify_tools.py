import tekore as tk
import sys
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
	

if __name__ == '__main__':
	if len(sys.argv) > 1:
		client_id = sys.argv[1]
	config_file = 'tekore.cfg'
	spotify = authorize()	
	
	user = get_user()
#	playlist_id = get_playlist('all songs')	
#	albums = get_saved_albums()
#	
#	clear_playlist(playlist_id)
#	for a in albums:
#		uri_list = get_album_track_uris(a.album)
#		print(uri_list)
#		add_to_playlist(playlist_id, uri_list)
	
# TODO:
# Create Most played tracks based on lastFM
# Create Least played tracks based on lastFM
# Create recommended tracks based on lastFM
# create loved tracks based on ListenBrainz
# Migrate library to other user
