from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from tinder_bot import TinderBot

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

bot = TinderBot()


#Success Callbacks
def emit_logged_in(profile):
    emit('logged_in', profile)

def emit_recs(results):
    emit('recs', results)

def emit_phone_auth_success():
	emit('phone_auth_success')

def emit_phone_auth_failure():
	emit('phone_auth_failure')

# App page
@app.route('/')
def index():
    return render_template('index.html')


#Socket IO events
@socketio.on('connect', namespace='/test')
def connect():
    print('Client connected')

@socketio.on('disconnect', namespace='/test')
def disconnect():
    print('Client disconnected')

#Custom events
@socketio.on('get_recs', namespace='/test')
def get_recommendations():
    message = bot.start_bot(emit_recs)

@socketio.on('login', namespace='/test')
def login(data):
    profile = bot.login_facebook(data)
    emit_logged_in(profile)

@socketio.on('login_phone', namespace='/test')
def login_phone(number):
	if bot.login_phone_number(number):
		emit_phone_auth_success()
	else:
		emit_phone_auth_failure()

@socketio.on('code', namespace="/test")
def send_code(code):
	profile = bot.get_phone_auth_token(code)
	emit_logged_in(profile)
    

    

if __name__ == '__main__':
    socketio.run(app)




# Serve the page
## List of recommendations with image and name
# Start the bot
# Pass data from bot to page through sockets
# Render recommendations



