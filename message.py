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
#요약 계산
zosa = ['은', '는', '가', '을', '를', '와', '과', '.', ',', '!', '?']
eomi = ['하', '했', '있', '없']
trashwords = ['할', '듯', '아마', '게', '아니', '난', '넌', '요약','코인']


def erase_in_words(words, word):
    if word not in trashwords:
        words.append(word)

def detail2words(message: str):

    
    '''
    # 필요없는 형식형태소를 ' '로 변환
    syllables = message.split()
    isending = False
    for i in range(0, len(syllables)):
        # 이하 어미 삭제 마무리까지
        if isending:
            if syllables[i] == ' ':
                isending = False
            syllables[i] = ' '
            continue  # 여기를 수정합니다.
        # '하'&&'했'&&'있'&&'없'에서 잘라서 어미 삭제 시작
        if syllables[i] in eomi:
            isending = True
            syllables[i] = ' '
        # 조사&&문장부호 일괄 삭제
        if syllables[i] in zosa:
            syllables[i] = ' '
    # 단어 추출
    word = ''
    words = []
    syllables.append(' ')
    for i in range(0, len(syllables)):
        if syllables[i] == ' ':
            if word != '':
                erase_in_words(words, word)  # 단어에서 거른다.
                word = ''
        else:
            word = word + syllables[i]
    
    return words
    '''

def littleshit(chat_history:dict, shigan:int):
    chatstart = 0
    # 문자열로 저장된 시간을 float로 변환, 변환 불가한 키는 필터링
    chat_times = []
    for key in chat_history.keys():
        try:
            chat_times.append(float(key))
        except ValueError:
            continue
    chat_times.sort(reverse=True)
    output = []
    while chatstart < len(chat_times) and thetime() - chat_times[chatstart] <= shigan:
        output.append(chat_times[chatstart])
        chatstart += 1
    return output


bot = commands.Bot(command_prefix='삭제 ', intents=intents)

# 코인 데이터를 저장할 JSON 파일
COIN_DATA_FILE = 'user_coins.json'

# 블랙잭 게임 상태 관리
blackjack_games = {}


def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        if card in ['J', 'Q', 'K']:
            value += 10
        elif card == 'A':
            aces += 1
            value += 11
        else:
            value += int(card)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value


def draw_card():
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return random.choice(cards)


# 코인 데이터 불러오기
def load_coin_data():
    if os.path.exists(COIN_DATA_FILE):
        with open(COIN_DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}


# 코인 데이터 저장하기
def save_coin_data(data):
    with open(COIN_DATA_FILE, 'w') as file:
        json.dump(data, file)


# 코인 데이터 불러오기
coin_data = load_coin_data()


# 유저의 코인 가져오기
def get_user_coins(user_id):
    return coin_data.get(str(user_id), 0)


# 유저의 코인 설정하기
def set_user_coins(user_id, coins):
    coin_data[str(user_id)] = coins
    save_coin_data(coin_data)


# 유저에게 코인 추가하기
def add_user_coins(user_id, coins):
    current_coins = get_user_coins(user_id)
    set_user_coins(user_id, current_coins + coins)



@bot.command(name='재시도')
async def saikonoshyotsi(ctx, after_minutes=0, before_minutes=20, ishour=0, max_messages=50):
    if ishour != 0:
        after_minutes = after_minutes*60
        before_minutes = before_minutes*60
    now = datetime.now(KST)
    after_time = now - timedelta(minutes=after_minutes)
    before_time = now - timedelta(minutes=before_minutes)
    
    async for message in ctx.history(limit=max_messages, after=before_time, before=after_time): #사라지지마 감지
        await message.delete()
            
            

@bot.command(name='dice')
async def dice(ctx, dice:str, purpose:str):
    if ctx.author.id not in dice_history:
        dice_history[ctx.author.id] = {}
    dr = []
    dd = dice.split("d")
    dd[0] = int(dd[0])
    dd[1] = int(dd[1])
    for i in range(dd[0]):
        dr.append(random.randrange(0,dd[1])+1)
    result = ''
    reresult = ''
    result_s = 0
    for i in dr:
        result += str(i)+'  |  '
        result_s += i
    result += f'  총합 {result_s}'
    if purpose in dice_history[ctx.author.id]:
        theli = dice_history[ctx.author.id][purpose]
    else:
        theli = 50
    if result_s<=round(theli):
        reresult = '성공'
    else:
        reresult = '실패'
        if result_s>=round(90):
            reresult = '극단적 실패'
    if result_s<=round(theli/2):
        reresult = '어려운 성공'
    if result_s<=round(theli/20):
        reresult = '극단적 성공'
    save_json(DICE_HISTORY_FILE, {})
    await ctx.send(purpose+'...roll\n'+f'{theli}  |  {round(theli/2)}  |  {round(theli/20)}\n'+result+'\n'+reresult)


# 명령어 ------------------------------ !확률설정
@bot.command(name='확률설정')
async def dice_fix(ctx,perpose:str,power:int):
    if ctx.author.id not in dice_history:
        dice_history[ctx.author.id] = {}
    dice_history[ctx.author.id][perpose] = power
    save_json(DICE_HISTORY_FILE,dice_history)
    await ctx.send(f"확률 설정 완료")

# 명령어 ------------------------------ !코인
@bot.command(name='코인')
async def check_coins(ctx):
    user_id = ctx.author.id
    coins = get_user_coins(user_id)
    await ctx.send(f"{ctx.author.mention}님의 현재 코인은 {coins}코인입니다.")


# 명령어 -------------------------------- !룰렛
@bot.command(name='룰렛')
async def roulette(ctx):
    user_id = ctx.author.id
    if get_user_coins(user_id) < 100:
        await ctx.send("코인이 부족합니다! 최소 100코인이 필요합니다.")
        return
    add_user_coins(user_id, -100)
    won_coins = random.randint(50, 200)
    add_user_coins(user_id, won_coins)
    await ctx.send(f"룰렛 결과: {won_coins}코인을 얻었습니다!")


# 명령어 ---------------------------- !숫자
@bot.command(name='숫자')
async def guess_number(ctx, guess: int):
    user_id = ctx.author.id
    if get_user_coins(user_id) < 900:
        await ctx.send("코인이 부족합니다! 최소 900코인이 필요합니다.")
        return
    if not 1 <= guess <= 10:
        await ctx.send("1에서 10 사이의 숫자를 입력해주세요.")
        return
    add_user_coins(user_id, -900)
    actual_number = random.randint(1, 10)
    if guess == actual_number:
        add_user_coins(user_id, 10000)
        await ctx.send(f"축하합니다! 숫자를 맞추셨습니다. 10000코인을 얻었습니다!")
    else:
        await ctx.send(f"틀렸습니다. 정답은 {actual_number}였습니다.")


# 명령어 - !요약
@bot.command(name='요약')
async def summerise(ctx, shigan: int, triger=3):
    ctx.guild.members

    words = {}
    summeries = []

    for i in littleshit(chat_history, shigan):
        messages = chat_history.get(str(i), [])[0]
        if not messages:
            await ctx.send('있을 수 없는 일. 이걸 본다면 도망쳐라.')
            continue

        # 도배 처리
        #
        # 수 세기
        for word in detail2words(messages[1]):
            if len(word) > 20:
                word = word[:20] + '...'
            if messages[0] not in words.keys():
                words[messages[0]] = {}
            words[messages[0]][word] = words[messages[0]].get(word,0) + 1

    # 작문 words[id] = {word:count,word:count}
    for id, organ in words.items():
        user = ctx.guild.get_member(int(id))
        if user:
            summeries.append(f"\n{user.nick}\n")
        print(id,organ)
        for word in organ.keys():
            if  organ[word] >= triger:
                summeries.append(f" {word} : {organ[word]}번   ")

    summery = ''.join(summeries)
    await ctx.send(f"{shigan}분간의 메시지에 대한 요약입니다.{summery}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # 채팅 기록 저장
    timestamp = thetime()  # 실제 시간을 반환하는 함수 호출
    if str(timestamp) not in chat_history:
        chat_history[str(timestamp)] = []  # JSON 직렬화를 위해 문자열로 저장
    chat_history[str(timestamp)].append([str(message.author.id), str(message.content)])
    save_json(CHAT_HISTORY_FILE, chat_history)

    # 코인 지급
    coins_earned = random.randint(0, 20)
    add_user_coins(message.author.id, coins_earned)
    await message.author.send(f"당신은 {coins_earned}코인을 획득했습니다.")

    await bot.process_commands(message)



# 명령어 -------------------------- !블랙잭
@bot.command(name='블랙잭')
async def blackjack(ctx):
    user_id = ctx.author.id
    if get_user_coins(user_id) < 2500:
        await ctx.send("코인이 부족합니다! 최소 2500코인이 필요합니다.")
        return

    # 게임 초기화
    player_hand = [draw_card(), draw_card()]
    dealer_hand = [draw_card(), draw_card()]
    blackjack_games[user_id] = {
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
        'finished': False
    }

    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    if player_value == 21:
        add_user_coins(user_id, 10000)  # 블랙잭 보너스 절반
        await ctx.send(
            f"{ctx.author.mention}님이 블랙잭을 달성했습니다! {player_hand} 딜러의 카드: {dealer_hand}. 10000코인을 얻었습니다."
        )
        blackjack_games[user_id]['finished'] = True
    else:
        add_user_coins(user_id, -2500)
        await ctx.send(
            f"{ctx.author.mention}님의 카드: {player_hand} (점수: {player_value}), 딜러의 보이는 카드: {dealer_hand[0]}. '히트' 또는 '스탠드'를 선택해주세요."
        )


@bot.command(name='히트')
async def hit(ctx):
    user_id = ctx.author.id
    if user_id not in blackjack_games or blackjack_games[user_id]['finished']:
        await ctx.send("진행 중인 블랙잭 게임이 없습니다.")
        return

    game = blackjack_games[user_id]
    game['player_hand'].append(draw_card())
    player_value = calculate_hand_value(game['player_hand'])

    if player_value > 21:
        await ctx.send(
            f"{ctx.author.mention}님이 버스트되었습니다! 카드: {game['player_hand']} (점수: {player_value})."
        )
        game['finished'] = True
    else:
        await ctx.send(
            f"{ctx.author.mention}님의 현재 카드: {game['player_hand']} (점수: {player_value}). '히트' 또는 '스탠드'를 선택해주세요."
        )


@bot.command(name='스탠드')
async def stand(ctx):
    user_id = ctx.author.id
    if user_id not in blackjack_games or blackjack_games[user_id]['finished']:
        await ctx.send("진행 중인 블랙잭 게임이 없습니다.")
        return

    game = blackjack_games[user_id]
    player_value = calculate_hand_value(game['player_hand'])
    dealer_value = calculate_hand_value(game['dealer_hand'])

    while dealer_value < 17:
        game['dealer_hand'].append(draw_card())
        dealer_value = calculate_hand_value(game['dealer_hand'])

    if dealer_value > 21 or player_value > dealer_value:
        add_user_coins(user_id, 5000)  # 승리 코인 절반
        await ctx.send(
            f"승리! {ctx.author.mention}님의 카드: {game['player_hand']} (점수: {player_value}), 딜러의 카드: {game['dealer_hand']} (점수: {dealer_value}). 5000코인을 얻었습니다."
        )
    elif player_value == dealer_value:
        add_user_coins(user_id, 2500)  # 무승부 코인 절반 반환
        await ctx.send(
            f"무승부입니다! {ctx.author.mention}님의 카드: {game['player_hand']} (점수: {player_value}), 딜러의 카드: {game['dealer_hand']} (점수: {dealer_value}). 2500코인을 돌려받았습니다."
        )
    else:
        await ctx.send(
            f"패배했습니다... {ctx.author.mention}님의 카드: {game['player_hand']} (점수: {player_value}), 딜러의 카드: {game['dealer_hand']} (점수: {dealer_value})."
        )

    game['finished'] = True


# 명령어 -------------- !랭킹
@bot.command(name='랭킹')
async def ranking(ctx):
    sorted_users = sorted(coin_data.items(), key=lambda x: x[1], reverse=True)
    ranking_message = "코인 랭킹:\n"
    for rank, (user_id, coins) in enumerate(sorted_users[:10], start=1):
        user = ctx.guild.get_member(int(user_id))
        
        if user:
            ranking_message += f"{rank}. {user.nick} - {coins}코인\n"
    await ctx.send(ranking_message)


# 명령어 -------------------- !주기
@bot.command(name='주기')
async def give_coins(ctx, member: discord.Member, amount: int):
    giver_id = ctx.author.id
    receiver_id = member.id

    if amount <= 0:
        await ctx.send("양수의 코인만 줄 수 있습니다.")
        return

    if get_user_coins(giver_id) < amount:
        await ctx.send("코인이 부족합니다!")
        return

    add_user_coins(giver_id, -amount)
    add_user_coins(receiver_id, amount)
    await ctx.send(
        f"{ctx.author.mention}님이 {member.mention}님에게 {amount}코인을 주었습니다.")


# 명령어 -------------------- !혁명
@bot.command(name='혁명')
async def revolution(ctx, member: discord.Member):
    attacker_id = ctx.author.id
    defender_id = member.id

    if get_user_coins(attacker_id) < 50:
        await ctx.send("혁명을 시도하기 위한 코인이 부족합니다! 최소 50코인이 필요합니다.")
        return

    add_user_coins(attacker_id, -50)
    success_chance = random.randint(1, 1000)

    if success_chance == 1:  # 0.1% 확률로 성공
        attacker_coins = get_user_coins(attacker_id)
        defender_coins = get_user_coins(defender_id)
        set_user_coins(attacker_id, defender_coins)
        set_user_coins(defender_id, attacker_coins)
        await ctx.send(
            f"혁명이 성공했습니다! {ctx.author.mention}님과 {member.mention}님의 코인이 교환되었습니다."
        )
    else:
        await ctx.send("혁명이 실패했습니다. 코인은 교환되지 않았습니다.")


# 명령어 - !명령어
@bot.command(name='명령어')
async def commands_list(ctx):
    commands = ("!코인 - 현재 내 코인을 확인합니다.\n"
                "!룰렛 - 100코인을 소모하여 50에서 200의 랜덤 코인을 얻습니다.\n"
                "!숫자 (숫자) - 1에서 10까지의 랜덤 숫자를 맞추면 10000코인을 얻습니다.\n"
                "!블랙잭 - 블랙잭 게임을 합니다.\n"
                "!랭킹 - 서버 내의 코인 순위를 보여줍니다.\n"
                "!주기 @이름 (금액) - 지정한 유저에게 코인을 줍니다.\n"
                "!혁명 @이름 - 혁명을 시도하여 서로의 코인을 바꿉니다.\n"
                "!명령어 - 모든 명령어를 알려줍니다.\n")
    await ctx.send(commands)

# 봇 실행
bot.run()
