
from flask_socketio import emit

def emit_logged_in(profile):
    emit('logged_in', profile)

def emit_recs(results):
    emit('recs', results)

def emit_phone_auth_success():
	emit('phone_auth_success')

def emit_phone_auth_failure():
	emit('phone_auth_failure')

def emit_like(id):
	emit('like', id)