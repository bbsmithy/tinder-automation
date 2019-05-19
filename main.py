import urllib3
import argparse
from app.tinder_bot import TinderBot
from app.fb_auth_token import get_fb_access_token, get_fb_id
from app.config import CONFIG

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
parser = argparse.ArgumentParser(description="Flip a switch by setting a flag")
parser.add_argument(
    '-m', type=str, help="Input for mobile number for mobile authentication option")
parser.add_argument(
    '-p', type=str, help="Input for Facebook password for Facebook authentication option")
parser.add_argument(
    '-e', type=str,  help="Input for Facebook email for Facebook authentication option")

args = parser.parse_args()

bot = TinderBot()


def initialize_bot_facebook(email, password):
    fb_token = get_fb_access_token(email, password)
    fb_id = get_fb_id(fb_token)
    tinder_token = bot.login_facebook(fb_token, fb_id)
    return bot.start_bot(tinder_token)


def initialize_bot_mobile(phone_number):
    bot.login_phone_number(phone_number)
    code = input("Enter code sent to your number:")
    token = bot.get_phone_auth_token(code)
    f = open("token.txt", "w")
    f.write(token)
    f.close()
    return bot.start_bot(token)


def read_token():
    try:
        f = open("token.txt", "r")
        return f.read()
    except:
        return False


def mobile_login(phone_number):
    saved_token = read_token()
    if saved_token:
        status = bot.start_bot(saved_token)
        if status != 200:
            return initialize_bot_mobile(phone_number)
    else:
        return initialize_bot_mobile(phone_number)


def facebook_login(email, password):
    saved_token = read_token()
    if saved_token:
        status = bot.start_bot(saved_token)
        if status != 200:
            initialize_bot_facebook(email, password)
    else:
        initialize_bot_facebook(email, password)


if __name__ == '__main__':
    if args.m:
        mobile_login(args.m)
    elif args.e and args.p:
        facebook_login(args.e, args.p)
    else:
        print("Please provide arguments or config file")
        print("-m: Mobile number for mobile authentication")
        print("-p: Facebook password for Facebook authentication")
        print("-e: Facebook email for Facebook authentication")
