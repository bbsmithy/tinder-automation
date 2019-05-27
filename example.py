from tinder_automation import TinderAutomation

ta = TinderAutomation()
ta.start({"login_method": "facebook", "email": "xxx", "password": "xxx"})


# login facebook, login mobile (CLI only)
# program runs every 24 hours on cron tab (Lamda cron job)
#
