
from flask_socketio import emit

def emit_logged_in(profile):
	emit('logged_in', profile, namespace='/test')

def emit_recs(results):
	emit('recs', results, namespace='/test')
	print(results)

def emit_phone_auth_success():
	emit('phone_auth_success', namespace='/test')

def emit_phone_auth_failure():
	emit('phone_auth_failure', namespace='/test')

def emit_like(id):
	emit('like', id, namespace='/test')