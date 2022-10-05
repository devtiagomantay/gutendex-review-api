from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config(object):
	# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}'
	# SQLALCHEMY_DATABASE_URI = environ['DATABASE_URL']
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:wq%.1eQd2!2@localhost:3306/database'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	DEBUG = False
	DEVELOPMENT = False


class DevelopmentConfig(Config):
	DEBUG = True
	DEVELOPMENT = True
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:wq%.1eQd2!2@localhost:3306/database'


class TestingConfig(Config):
	TESTING = True


config = {
	'dev': DevelopmentConfig,
	'test': TestingConfig,
	'default': DevelopmentConfig,
}
