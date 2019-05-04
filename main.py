from tinder_bot import TinderBot
import urllib3
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
parser = argparse.ArgumentParser(description="Flip a switch by setting a flag")
parser.add_argument(
    '-m', type=str, help="Input for mobile number for mobile authentication option")
parser.add_argument(
    '-p', type=str, help="Input for Facebook password for Facebook authentication option")
parser.add_argument(
    '-e', type=str,  help="Input for Facebook email for Facebook authentication option")

args = parser.parse_args()


# Command line arguments
# -m: Mobile number login
# -e: Email facebook login
# -ps: Password facebook login
# -help: Gets help

# -config: config file json file (if found ignore all other commands)
# {'login_type': 'facebook', 'email': 'bean.smith77@gmail.com', 'password': 'some_passy_word', 'number': '0838100085'}

# Example way to run
# python3 tinder-automation -m

bot = TinderBot()


def initialize_bot_mobile(phone_number):
    bot.login_phone_number(phone_number)
    code = input("Enter code sent to your number:")
    token = bot.get_phone_auth_token(code)
    f = open("token.txt", "w")
    f.write(token)
    f.close()
    bot.start_bot(token)


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
            initialize_bot_mobile(phone_number)
    else:
        initialize_bot_mobile(phone_number)


def facebook_login():
    print('Rewrite facebook login using flags please Brian...please do it now please...did you hear me?')


if __name__ == '__main__':
    if args.m:
        mobile_login(args.m)
    elif args.e and args.p:
        print("Facebook login")
        print(args.e)
        print(args.p)
    else:
        print("Please provide arguments or config file")
        print("-m: Mobile number for mobile authentication")
        print("-p: Facebook password for Facebook authentication")
        print("-e: Facebook email for Facebook authentication")
