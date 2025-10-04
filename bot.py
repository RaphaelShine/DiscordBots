import discord
from discord.ext import commands
import time
from datetime import datetime, timedelta, timezone

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True
intents.members = True

KST = timezone(timedelta(hours=9))
voice_clients = {}


bot = commands.Bot(command_prefix="!", intents=intents)

swearList = ["조팝나무","쌀돼지","미쿠는 노래를 좀 못 부르는 것 같아"]


@bot.event
async def on_ready(): #실행 시작
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return
    message = ctx.content
    for i in swearList:
        if inspect(message,i):
            await ctx.delete()
            await ctx.channel.send(str(ctx.author.display_name)+"의 메시지에 욕설이 보여서 죽였어~! 감지된 욕설 : "+i)
    await bot.process_commands(ctx)

def inspect(message,swear):
    ii=0
    lenswear = len(swear)
    for i in range(len(message)):
        if message[i] == swear[ii]:
            ii+=1
            if ii==lenswear:
                return True
        else:
            ii=0
    return False

@bot.command(name='안녕') #이렇게 골벵이 줄 뒤에 있는 게 명령어야
async def hallo(ctx):
    await ctx.channel.send('안녕!')
    print(ctx.author.id) #log에 author.id 알려줌

@bot.command(aliases = ['거기있니?']) 
async def respond(ctx):
    await ctx.channel.send('그럿다')
    print(ctx.channel.id) #log에 channel.id 알려줌

@bot.command(aliases = ['일로와', '이리와','다시와'])
async def join(ctx): #통화방 참가
    if ctx.author.voice:
        await ctx.channel.send("알앗어")
        channel = ctx.author.voice.channel
        vc = await channel.connect()
        voice_clients[ctx.guild.id] = vc
    else:
        await ctx.channel.send("엥 너 어디니?")

@bot.command(aliases = ['잘가', '저리가', '이제'])
async def leave(ctx): #통화방 퇴장
    if ctx.guild.id in voice_clients:
        await ctx.channel.send("잘잇어")
        await voice_clients[ctx.guild.id].disconnect()
        del voice_clients[ctx.guild.id]

@bot.command(name="초대")
async def 초대(ctx, member: discord.Member, channel_id: int):
    guild = ctx.guild
    channel = guild.get_channel(channel_id)

    if not channel:
        await ctx.channel.send("해당 채널 ID를 찾을 수 없습니다.")
        return

    # 권한 부여: 채널 보기 가능하게 설정
    overwrite = channel.overwrites_for(member)
    overwrite.view_channel = True
    print(channel_id)
    await channel.set_permissions(member, overwrite=overwrite)
    await ctx.channel.send(f"{member.mention}, 내가 불렀다 ㅋ")

#함수 추가하려면 여기다가






#이게 실제 동작 실행코드. 위에서 열심히 쓴 건 다 이 코드를 통해 실행되는 거니까 이건 꼭 마지막에다 둬.
bot.run("")  # 여기에 네 디스코드 봇 토큰 넣기
