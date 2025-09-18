import discord
from discord.ext import commands
import yt_dlp
import asyncio
import time
from datetime import datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="ଳ", intents=intents)

voice_clients = {}


@bot.event
async def on_ready(): #실행 시작
    print(f"Logged in as {bot.user}")

@bot.command(aliases = ['거기있니?']) #이렇게 골벵이 줄 뒤에 있는 게 명령어야
async def respond(ctx): #이게 노예로 부리는 방법
    await ctx.send('그럿다')
    print(ctx.channel.id)

@bot.command(aliases = ['따라해']) #이렇게 골벵이 줄 뒤에 있는 게 명령어야
async def repeat(ctx): #이게 노예로 부리는 방법
    ch = bot.get_channel(1276840449906180096)
    ment = ctx.message.content
    ment = ment[5:]
    print(ment)
    await ch.send(ment)


@bot.command(aliases = ['일로와', '이리와','다시와'])
async def join(ctx): #통화방 참가
    if ctx.author.voice:
        await ctx.send("알앗어")
        channel = ctx.author.voice.channel
        vc = await channel.connect()
        voice_clients[ctx.guild.id] = vc
    else:
        await ctx.send("엥 너 어디니?")

@bot.command(aliases = ['잘가', '저리가', '이제'])
async def leave(ctx): #통화방 퇴장
    if ctx.guild.id in voice_clients:
        await ctx.send("잘잇어")
        await voice_clients[ctx.guild.id].disconnect()
        del voice_clients[ctx.guild.id]

@bot.command(name='불러줘')
async def play(ctx, url): #노래 요청
    if ctx.guild.id not in voice_clients:
        await ctx.invoke(join)
    await ctx.send("좋아")

    vc = voice_clients[ctx.guild.id]

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'song.mp3',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    vc.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: print())



#여기는 노래 재생 되면 추가 조작 기능. 아직 한번도 시도 못함. 일단 재생부터 돼야함.
@bot.command(aliases = ['skip', 's'])
async def Skip(ctx):
    try:
        bot.voice_clients[0].stop()
    except:
        await ctx.send("Skip Error")
 
@bot.command(aliases = ['pause'])
async def Pause(ctx):
    try:
        bot.voice_clients[0].pause()
    except:
        await ctx.send("Pause Error")
 
@bot.command(aliases = ['resume'])
async def Resume(ctx):
    try:
        bot.voice_clients[0].resume()
    except:
        await ctx.send("Resume Error")

#함수 추가하려면 여기다가




@bot.command(name="초대")
async def 초대(ctx, member: discord.Member, channel_id: int):
    guild = ctx.guild
    channel = guild.get_channel(channel_id)

    if not channel:
        await ctx.send("해당 채널 ID를 찾을 수 없습니다.")
        return

    # 권한 부여: 채널 보기 가능하게 설정
    overwrite = channel.overwrites_for(member)
    overwrite.view_channel = True
    print(channel_id)
    await channel.set_permissions(member, overwrite=overwrite)
    await ctx.send(f"{member.mention}, 내가 불렀다 ㅋ")

@bot.command(name="스레드정화")
async def 삭제스레드(ctx):
    if ctx.author.id != 800291345197432862:
        await ctx.send("무슨 소릴 하는 거야? 으으")
        return
    # 이 명령어가 스레드 내에서 호출되었는지 확인
    if isinstance(ctx.channel, discord.Thread):
        await ctx.send("^^7")
        await ctx.channel.delete()
    else:
        await ctx.send("여긴 스레드가 아니야")

@bot.command(name='해파리요원출동!')
async def messageCopy(ctx, after_minutes=0, before_minutes=60, ishour=0, max_messages=50):
    if ctx.author.id != 800291345197432862:
        await ctx.send("저 요원 아닌데요.")
        return
    await ctx.send('^^7')
    if ishour != 0:
        after_minutes = after_minutes*60
        before_minutes = before_minutes*60
    now = datetime.now(KST)
    after_time = now - timedelta(minutes=after_minutes)
    before_time = now - timedelta(minutes=before_minutes)
    
    messagePoket = []
    async for message in ctx.history(limit=max_messages, after=before_time, before=after_time):
        messagePoket.append([str(message.author),str(message.created_at),str(message.content)])
    result=''
    for msgA_C in messagePoket:
        result+=msgA_C[0]+'\n'+msgA_C[1]+'\n'+msgA_C[2]+'\n'
    await ctx.send(result)

@bot.command(name='수습해!')
async def saikonoshyotsi(ctx, after_minutes=0, before_minutes=20, ishour=0, max_messages=50):
    if ctx.author.id != 800291345197432862:
        await ctx.send("ㅔ? 뭘? ㅇㅠㅇ?")
        return
    if ishour != 0:
        after_minutes = after_minutes*60
        before_minutes = before_minutes*60
    now = datetime.now(KST)
    after_time = now - timedelta(minutes=after_minutes)
    before_time = now - timedelta(minutes=before_minutes)
    
    async for message in ctx.history(limit=max_messages, after=before_time, before=after_time): #사라지지마 감지
        await message.delete()

#이게 실제 동작 실행코드. 위에서 열심히 쓴 건 다 이 코드를 통해 실행되는 거니까 이건 꼭 마지막에다 둬.
bot.run()  # 여기에 네 디스코드 봇 토큰 넣기