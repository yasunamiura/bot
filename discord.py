from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from discord.ext import commands
import discord
import os

# FlaskアプリとSQLAlchemyの設定
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://your_mysql_username:your_mysql_password@localhost/your_database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# データベースモデルの定義
class DiscordMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    message_id = db.Column(db.BigInteger, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)

# discord.pyクライアントの設定
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID_STR = os.getenv('DISCORD_CHANNEL_ID')  # メッセージを取得したいチャンネルのID（整数）
CHANNEL_ID = int(CHANNEL_ID_STR)

intents = discord.Intents.default()
intents.messages = True
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        print('チャンネルが見つかりませんでした。')
        return

    # データベーステーブルが存在しなければ作成
    with app.app_context():
        db.create_all()

    # メッセージの履歴を取得し、データベースに保存
    messages = await channel.history(limit=1000).flatten()
    with app.app_context():
        for message in messages:
            nickname = message.author.display_name
            new_message = DiscordMessage(
                username=message.author.name,
                nickname=nickname,
                user_id=message.author.id,
                message_id=message.id,
                timestamp=message.created_at,
                content=message.content
            )
            db.session.add(new_message)

        db.session.commit()
    print('メッセージがデータベースに保存されました。')
    await client.close()

client.run(TOKEN)
