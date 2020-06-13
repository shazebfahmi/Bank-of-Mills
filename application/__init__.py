from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.secret_key = '123'
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'Q4WIoIq4gO'
app.config['MYSQL_PASSWORD'] = 'd5aCVK6L5K'
app.config['MYSQL_DB'] = 'Q4WIoIq4gO'


from application import routes