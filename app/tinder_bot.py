import json
import sys
import time

from app.phone_auth_token import phone_login, getToken
from app.fb_auth_token import get_fb_access_token, get_fb_id
from app.tinder_api import send_msg, like, get_recommendations, get_updates, get_auth_token, update_xauth_token
from app.features import pause


class TinderBot:

    def __init__(self):
        self.auth_token = ""
        self.req_code = ""
        self.phone_number = ""
        self.results = []

    def __get_new_matches(self, matches):
        new_matches_number = len(matches) - self.old_matches_num
        print("New matches: {0}".format(new_matches_number))
        if new_matches_number == 0:
            return False
        if new_matches_number == 1:
            return [matches[-new_matches_number]]
        else:
            return matches[-new_matches_number:]

    def __message_matches(self, matches):
        if isinstance(matches, list):
            for match in matches:
                match_id = match['_id']
                pause()
                message = "Good evening...."
                send_msg(match_id, message)
                print("Messaged {0}:{1}".format(
                    match['person']['name'], message))
        else:
            match_id = matches['_id']
            message = "Good evening...."
            send_msg(match_id, message)
            log_message = "Messaged {0}:{1}".format(
                match['person']['name'], message)
            print(log_message)

    def print_details(self, rec):
        print('Liked '+rec['name'] + ' | ' + rec['bio'])

    def find_matches(self, results):
        for idx, rec in enumerate(results):
            if self.bot_alive is True:
                like(rec['_id'])
                self.print_details(rec)
                time.sleep(1)
            else:
                break

    def __get_recs(self):
        return get_recommendations(self.auth_token)

    def __get_all_matches(self):
        return get_updates()['matches']

    def login_facebook(self, email, password):
        fb_token = get_fb_access_token(email, password)
        fb_id = get_fb_id(fb_token)

        return {fb_token, fb_id}

    def get_facebook_auth_token(self, fb_token, fb_id):
        self.auth_token = get_auth_token(fb_token, fb_id)
        update_xauth_token(self.auth_token)
        return self.auth_token

    def login_phone_number(self, number):
        self.req_code = phone_login(number)
        self.phone_number = number
        return self.req_code

    def get_phone_auth_token(self, code):
        self.auth_token = getToken(
            self.phone_number, code, self.req_code)
        update_xauth_token(self.auth_token)
        return self.auth_token

    def stop_bot(self):
        self.bot_alive = False

    # Start the bot
    def start_bot(self, token):
        self.auth_token = token
        recs = self.__get_recs()
        recs_status = recs['status']
        if recs_status == 200:
            results = recs["results"]
            self.bot_alive = True
            old_matches = self.__get_all_matches()
            self.old_matches_num = len(old_matches)
            self.find_matches(results)
            all_matches = self.__get_all_matches()
            new_matches = self.__get_new_matches(all_matches)
            if new_matches:
                self.__message_matches(new_matches)
            return recs_status
        else:
            return recs_status
