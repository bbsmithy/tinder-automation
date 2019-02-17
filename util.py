from datetime import datetime, timezone

def get_time():
	local_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%Z');
	return local_time+'Z'