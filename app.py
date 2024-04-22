from dotenv import load_dotenv
import discord
import csv
import asyncio
import os

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID_STR = os.getenv('DISCORD_CHANNEL_ID')  # メッセージを取得したいチャンネルのID（整数）
CHANNEL_ID = int(CHANNEL_ID_STR)

LAST_MESSAGE_ID_FILE = 'last_message_id.txt'  # 最後に取得したメッセージIDを保存するファイル名

# 特権インテントの有効化
intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    # CHANNEL_ID を適切なチャネルIDに置き換える
    channel = client.get_channel(CHANNEL_ID)  
    if channel is None:
        print('チャンネルが見つかりませんでした。')
        return

    # 最後に取得したメッセージIDを読み込む
    if os.path.exists(LAST_MESSAGE_ID_FILE):
        with open(LAST_MESSAGE_ID_FILE, 'r') as file:
            last_message_id = int(file.read().strip())
    else:
        last_message_id = None

    after = discord.Object(id=last_message_id) if last_message_id else None
        
    # メッセージを保存するCSVファイルを開く
    with open('output.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "UserID", "MessageID", "Timestamp", "Content"])

        # 非同期リスト内包表記を使用してチャンネルからメッセージを取得（最後に取得したメッセージID以降）
        messages = [message async for message in channel.history(limit=1000, after=after)]
        
        for message in messages:
            writer.writerow([message.author.name, message.author.id, message.id, message.created_at, message.content])

    if messages:
        # 最新のメッセージIDをファイルに記録
        with open(LAST_MESSAGE_ID_FILE, 'w') as file:
            file.write(str(messages[0].id))

    print('CSVファイルが保存されました。')
    # Botをログアウトします
    await client.close()

# TOKENを適切なトークンに置き換える
client.run(TOKEN)
