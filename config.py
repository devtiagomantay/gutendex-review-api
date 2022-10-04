import os


class Config(object):
	# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}'
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	SQLALCHEMY_TRACK_MODIFICATIONS = False