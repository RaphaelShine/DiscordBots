import discord
import json
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

bot = commands.Bot(command_prefix='아 ', intents=intents)

@bot.command(name='으슬으슬')
async def saikonoshyotsi(ctx, after_minutes=0, before_minutes=10, ishour=0, max_messages=50):
    if ishour != 0:
        after_minutes = after_minutes*60
        before_minutes = before_minutes*60
    now = datetime.now(KST)
    after_time = now - timedelta(minutes=after_minutes)
    before_time = now - timedelta(minutes=before_minutes)
    
    async for message in ctx.history(limit=max_messages, after=before_time, before=after_time):
        if message.author.id == ctx.author.id:
            await message.delete()


@bot.command(name='안녕')
async def hallo(ctx):
    await ctx.send(str(ctx.author.id))




# 봇 실행
bot.run()