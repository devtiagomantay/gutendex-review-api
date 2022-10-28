import os
import unittest
from project import main
from pathlib import Path

TEST_DB = 'test.db'
app = main.app
db = main.db


class BasicTest(unittest.TestCase):
	def setUp(self):
		app.config['BASEDIR'] = str(Path(os.getcwd()).parents[0])
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
												os.path.join(app.config['BASEDIR'], TEST_DB)
		self.app = app.test_client()
		db.drop_all()
		db.create_all()

		self.assertEqual(app.debug, False)

		# TODO: add mock data

	def tearDown(self):
		os.remove(app.config['BASEDIR'] + '/test.db')
		pass

	def test_search_name_endpoint(self):
		response = self.app.get('/books/search/name/name', follow_redirects=True)
		self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
	unittest.main()
