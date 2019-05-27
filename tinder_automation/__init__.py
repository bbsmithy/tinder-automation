import urllib3
import argparse
from .tinder_bot import TinderBot


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TinderAutomation:

    def __init__(self):
        self.bot = TinderBot()

    def __initialize_bot_facebook(self, email, password):
        result = self.bot.login_facebook(email, password)
        if(result is False):
            print('Could not login using email and password')
        else:
            tinder_token = self.bot.get_facebook_auth_token(
                result['fb_token'], result['fb_id'])
            self.__write_token(tinder_token)
            return self.bot.start_bot(tinder_token)

    def __initialize_bot_mobile(self, phone_number):
        self.bot.login_phone_number(phone_number)
        code = input("Enter code sent to your number:")
        token = self.bot.get_phone_auth_token(code)
        self.__write_token(token)
        return self.bot.start_bot(token)

    def __write_token(self, token):
        f = open("token.txt", "w")
        f.write(token)
        f.close()

    def __read_token(self):
        try:
            f = open("token.txt", "r")
            return f.read()
        except:
            return False

    def __mobile_login(self, phone_number):
        saved_token = self.__read_token()
        if saved_token:
            status = self.bot.start_bot(saved_token)
            if status != 200:
                return self.__initialize_bot_mobile(phone_number)
        else:
            return self.__initialize_bot_mobile(phone_number)

    def __facebook_login(self, email, password):
        saved_token = self.__read_token()
        if saved_token:
            status = self.bot.start_bot(saved_token)
            if status != 200:
                self.__initialize_bot_facebook(email, password)
        else:
            self.__initialize_bot_facebook(email, password)

    def start(self, config):
        if('login_method' in config):
            if(config['login_method'] is 'facebook'):
                if('email' in config and 'password' in config):
                    self.__facebook_login(
                        config['email'], config['password'])
                else:
                    print(
                        "Please provide facebook email and password fields in config object to login")
            elif(config['login_method'] is 'mobile'):
                self.__mobile_login(config['number'])
        else:
            print(
                "Please provide login_method, e.g 'login_method':('mobile' or 'facebook')")
