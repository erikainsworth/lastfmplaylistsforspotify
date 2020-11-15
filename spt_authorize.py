import tekore as tk

config_file = 'tekore.cfg'
def authorize():
	
	try:
		conf = tk.config_from_file(config_file, return_refresh=True)
		token = tk.refresh_pkce_token(conf[0], conf[3])
		tk.config_to_file(config_file, conf[:3] + (token.refresh_token,))
	except:
		client_id = input('please enter app client_id')
		client_secret = 'your_client_secret'
		redirect_uri = 'https://example.com/callback'   # Or your redirect uri
		conf = (client_id, client_secret, redirect_uri)		
		token = tk.prompt_for_pkce_token(client_id, redirect_uri, scope=tk.scope.every)
		tk.config_to_file(config_file, conf + (token.refresh_token,))
	return tk.Spotify(token)
	
	
