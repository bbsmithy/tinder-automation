from tinder_bot import TinderBot

class Test():
	"""docstring for Test"""
	def __init__(self, arg):
		super(Test, self).__init__()
		self.arg = arg
		self.email = "bean.smith77@gmail.com"
		self.password = "the power of christy"
		self.bot = TinderBot()
		self.login()

	def login(self):
		login_data = {email: self.email, password: self.password, method:'F'}
		profile = self.bot.login_bot(login_data)
		print(profile)

	def get_meta():
		print(tinder_api.get_meta())
		