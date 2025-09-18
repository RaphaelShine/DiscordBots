import discord
import json
import random
import os
import time
from discord.ext import commands
from datetime import datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True
intents.members = True
CHAT_HISTORY_FILE = 'chat_history.json'
DICE_HISTORY_FILE = 'dice_history.json'


def thetime():
    return time.time()/60 # [분]



# 데이터 파일 로드/저장 함수
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return {}


def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


chat_history = load_json(CHAT_HISTORY_FILE)
dice_history = load_json(DICE_HISTORY_FILE)

bot = commands.Bot(command_prefix='메시지 ', intents=intents)

@bot.event
async def on_message(ctx):
    message = ctx.content
    iscute = False
    for i in message:
        if i == '동':
            iscute = True
        elif iscute and i == '생':
            await ctx.channel.send('너무 귀여워')
            break
        else:
            iscute = False

@bot.command(name='먹기')
async def saikonoshyotsi(ctx, after_minutes=0, before_minutes=20, ishour=0, max_messages=50):
    if ishour != 0:
        after_minutes = after_minutes*60
        before_minutes = before_minutes*60
    now = datetime.now(KST)
    after_time = now - timedelta(minutes=after_minutes)
    before_time = now - timedelta(minutes=before_minutes)
    
    async for message in ctx.history(limit=max_messages, after=before_time, before=after_time): #사라지지마 감지
        await message.delete()
            

# 봇 실행
bot.run()
