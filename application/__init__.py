from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.secret_key = '123'

app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'REm29D0rwB'
app.config['MYSQL_PASSWORD'] = '1DSGo1IFqr'
app.config['MYSQL_DB'] = 'REm29D0rwB'


from application import routes


#Visit the below website for the access to the PHP Database and enter the above credentials to login.
#  https://remotemysql.com/phpmyadmin/index.php

