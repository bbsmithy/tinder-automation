from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from tinder_bot import TinderBot
import event_emitter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def socketSleep(seconds):
    socketio.sleep(seconds)

bot = TinderBot(socketSleep)

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
    # bot.stop_bot()

#Custom events
@socketio.on('find_matches', namespace='/test')
def get_recommendations():
    bot.start_bot()

@socketio.on('login', namespace='/test')
def login(data):
    profile = bot.login_facebook(data)
    event_emitter.emit_logged_in(profile)
    bot.init_bot()

@socketio.on('login_phone', namespace='/test')
def login_phone(number):
	if bot.login_phone_number(number):
		event_emitter.emit_phone_auth_success()
	else:
		event_emitter.emit_phone_auth_failure()

@socketio.on('code', namespace="/test")
def send_code(code):
    profile = bot.get_phone_auth_token(code)
    event_emitter.emit_logged_in(profile)
    bot.init_bot()
    

    

if __name__ == '__main__':
    socketio.run(app)




# Serve the page
## List of recommendations with image and name
# Start the bot
# Pass data from bot to page through sockets
# Render recommendations



