import unittest
from app.tinder_bot import TinderBot

bot = TinderBot()

TEST_CONFIG = {
    "email": 'bean.smith77@gmail.com',
    'password': 'thepowerofchristy'
}


class TestMain(unittest.TestCase):

    def test_facebook_login(self):
        fb_token, fb_id = bot.login_facebook(
            TEST_CONFIG['email'], TEST_CONFIG['password'])
        print("Facebook token: {0}".format(fb_token))
        print("Facebook id: {0}".format(fb_id))
        self.assertFalse('error' in fb_token)
        self.assertFalse('error' in fb_id)


if __name__ == "__main__":
    unittest.main()
