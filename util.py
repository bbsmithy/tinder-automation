from datetime import datetime, timezone

def get_time():
	local_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%Z');
	return local_time+'Z'

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))