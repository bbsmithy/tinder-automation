import tinder_api
import fb_auth_token
import json
import features
import sys
import util
import phone_auth_token
import event_emitter



class TinderBot:

    def __init__(self, sleepFunction):
        self.auth_token = ""
        self.req_code = ""
        self.phone_number = ""
        self.results = []
        self.socketSleep = sleepFunction

    def get_meta(self):
        return tinder_api.get_meta()
        
    def message_matches(self, matches):
        for match in matches:
            match_id = match["_id"]
            features.pause()
            message = "Good evening...."
            tinder_api.send_msg(match_id, message)
            print("Messaged "+match["name"]+": "+message)


    def print_stats(self, matches, results):
        matches_count = len(matches)
        success_rate = len(matches) // len(results) * 100
        print("Matched with: " + matches_count + " people");
        print("Success rate: " + success_rate + "%");


    def check_for_matches(self, check_since_time):
        updates = tinder_api.get_matches(check_since_time)
        return updates['matches']


    def find_matches(self, results):
        starting_time = util.get_time()
        for idx, rec in enumerate(results):
            tinder_api.like(rec['_id'])
            print('Liked '+rec['name'])
            event_emitter.emit_like(rec['_id'])
            if idx % 5 == 0:
                matches = tinder_api.get_updates(starting_time)
                print(matches)
            self.socketSleep(2)
       


    def get_recs(self):
        return tinder_api.get_recommendations(self.auth_token)



    #Handle authentication for bot
    def login_phone_number(self, number):
        self.req_code = phone_auth_token.phone_login(number)
        self.phone_number = number
        return True

    def get_phone_auth_token(self, code):
        self.auth_token = phone_auth_token.getToken(self.phone_number, code, self.req_code)
        tinder_api.update_xauth_token(self.auth_token)
        return tinder_api.get_self()


    def login_facebook(self, data):
        fb_access_token = fb_auth_token.get_fb_access_token(data["email"], data["password"])
        fb_user_id = fb_auth_token.get_fb_id(fb_access_token)
        self.auth_token = tinder_api.get_auth_token(fb_access_token, fb_user_id)
        return tinder_api.get_self()

    #Start the bot
    def start_bot(self):
        self.find_matches(self.results)
       

    def init_bot(self):
        recs = self.get_recs()
        if recs['status']==200:  
            self.results = recs["results"] 
            event_emitter.emit_recs(self.results)
        else:
            print(recs)

    #get results -> send to client
    #foreach result
        #like index -> send index to client -> remove from results ss -> show love heart for second -> remove from list cs
    #check for matches -> send matches to client -> display matches client side with option to send all
    #type message and send to server -> run message matches ss
    #