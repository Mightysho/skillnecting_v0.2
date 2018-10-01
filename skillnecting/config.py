import os

class Config(object):
	"""Class for Program configuration"""
	SECRET_KEY = '5791628bb0b13ce0c676dfe280ba245'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
	GITHUB_CLIENT_ID = '24a5c3541e979bfb46d1'
	GITHUB_CLIENT_SECRET = '9b3d9c350e6a1de6e440b4eb63a3c58734db5fbe'