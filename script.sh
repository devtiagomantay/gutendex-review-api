#!/bin/sh
sudo apt install python3 virtualenv docker docker-compose git pymysql
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
sudo docker-compose -f docker-compose.yaml up -d
export DATABASE_URL="mysql+pymysql://root:@localhost:3306/database"
flask db init
flask db migrate
flask run