from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# MySQLデータベース接続設定
USER = 'discord'
PASSWORD = 'tc2024'
HOST = 'localhost'  # またはリモートアドレス
DATABASE = 'discord-bot'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DATABASE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
