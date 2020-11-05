import tekore as tk

def authorize():
	try:
		conf = tk.config_from_file(config_file, return_refresh=True)
		token = tk.refresh_pkce_token(conf[0], conf[3])
		tk.config_to_file(config_file, conf[:3] + (token.refresh_token,))
	except:
		client_id = '10fed7a2f3b745b59d976d602bce0a02'
		client_secret = 'your_client_secret'
		redirect_uri = 'https://example.com/callback'   # Or your redirect uri
		conf = (client_id, client_secret, redirect_uri)		
		token = tk.prompt_for_pkce_token(client_id, redirect_uri, scope=tk.scope.every)
		tk.config_to_file(config_file, conf + (token.refresh_token,))
	return tk.Spotify(token)

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
	
def get_user():
	return spotify.current_user()
	
def add_to_playlist(playlist_id, uris):
	spotify.playlist_add(playlist_id, uris, position=None)

def create_play_list(name):
	pl = spotify.playlist_create(user.id, name, public=False, description='just testing')
	return pl.id
	
# echtwaar = id: 6ymLpUDv4ct4KznBvMQFxG
config_file = 'tekore.cfg'
spotify = authorize()
user = get_user()
playlist_id = get_playlist('all songs')
albums = get_saved_albums()
for a in albums:
	uri_list = get_album_track_uris(a.album)
	print(uri_list)
	add_to_playlist(playlist_id, uri_list)