import tinder_api
import json
import features
import sys
import phone_auth_token
import time


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
                features.pause()
                message = "Good evening...."
                tinder_api.send_msg(match_id, message)
                log_message = "Messaged {0}:{1}".format(
                    match['person']['name'], message)
                print(log_message)

        else:
            match_id = matches['_id']
            message = "Good evening...."
            tinder_api.send_msg(match_id, message)
            log_message = "Messaged {0}:{1}".format(
                match['person']['name'], message)
            print(log_message)

    def print_details(self, rec):
        print('Liked '+rec['name'] + ' | ' + rec['bio'])

    def find_matches(self, results):
        for idx, rec in enumerate(results):
            if self.bot_alive is True:
                tinder_api.like(rec['_id'])
                self.print_details(rec)
                time.sleep(1)
            else:
                break

    def __get_recs(self):
        return tinder_api.get_recommendations(self.auth_token)

    def __get_all_matches(self):
        return tinder_api.get_updates()['matches']

    def login_facebook(self, fb_token, fb_id):
        self.auth_token = tinder_api.get_auth_token(fb_token, fb_id)
        tinder_api.update_xauth_token(self.auth_token)
        return self.auth_token

    def login_phone_number(self, number):
        self.req_code = phone_auth_token.phone_login(number)
        self.phone_number = number
        return True

    def get_phone_auth_token(self, code):
        self.auth_token = phone_auth_token.getToken(
            self.phone_number, code, self.req_code)
        tinder_api.update_xauth_token(self.auth_token)
        return self.auth_token

    def stop_bot(self):
        self.bot_alive = False

    # Start the bot
    def start_bot(self, token):
        self.auth_token = token
        recs = self.__get_recs()
        recs_status = recs['status']
        if recs_status == 200:
            self.results = recs["results"]
            self.bot_alive = True
            old_matches = self.__get_all_matches()
            self.old_matches_num = len(old_matches)
            self.find_matches(self.results)
            all_matches = self.__get_all_matches()
            new_matches = self.__get_new_matches(all_matches)
            if new_matches:
                self.__message_matches(new_matches)
            return recs_status
        else:
            return recs_status
