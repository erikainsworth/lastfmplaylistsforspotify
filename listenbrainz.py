import pylistenbrainz

def get_listens(name):
	listens = lb_client.get_listens(username=name)
	for listen in listens:
		print("Track name:", listen.track_name)
		print("Artist name:", listen.artist_name)
		
def get_recordings(name):
	listens = lb_client.get_user_recordings(username=name)
	for listen in listens:
		print(listen)