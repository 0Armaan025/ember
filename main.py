
import asyncio
import datetime
import pytube
from jokeapi import Jokes
import io
import json
from asyncio import sleep as s
from gtts import gTTS
from pyvirtualdisplay import Display
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
import os
import random
from PIL import Image, ImageDraw, ImageSequence,ImageFont
import re
import time
import chess
import pytz
import openai
import requests
from twilio.rest import Client
from discord import File, app_commands
import discord
from googletrans import Translator
from discord.ext import commands, tasks
import dotenv
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="$",intents=intents)
dotenv.load_dotenv()
token = os.getenv('token')
apikey = os.getenv('apikey')
toNumber = os.getenv('toNumber')
fromNumber = os.getenv('fromNumber')
authToken = os.getenv('authtoken')
accountSid = os.getenv('accountsid')
openai.api_key = apikey

#==================== ON READY ======================

@client.event
async def on_ready():   
    await client.change_presence(activity=discord.Game('Chess!'),status=discord.Status("idle"))
    print("The bot is ready")
    

#==================== howdy, hello? huh ======================    
@client.command(description='say hello to the bot :)',aliases=["howdy",'hiiii bro',"hi dude","hii man","hii bot","bro","wasup","sup"])
async def hello(ctx):
    choices = ["howdy","hiiiiiii","hloooooo","hola","namaste","how are you?:smile:","howdyyyyyyyyyyyyyyyyyy","heyyyyyyyyyyy"];
    choice = random.choice(choices);
    await ctx.send(f"{choice} {ctx.author.mention}")


#==========================FLIP A COIN==========================
@client.command(aliases=["flip a coin","flipcoin","flipacoin"])
async def flip(ctx):
    await ctx.send("Who wants HEADS and who wants TAILS? Please enter the names of the users separated by a space.")
    msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
    heads_user_name, tails_user_name = msg.content.split()[:2]

    headsUser = discord.utils.get(ctx.guild.members, name=heads_user_name)
    tailsUser = discord.utils.get(ctx.guild.members, name=tails_user_name)

    coin_statuses = {
        1: ("HEADS", "https://media.tenor.com/nEu74vu_sT4AAAAC/heads-coinflip.gif"),
        2: ("TAILS", "https://media.tenor.com/kK8D7hQXX5wAAAAM/coins-tails.gif")
    }
    coin_status, url = coin_statuses[random.choice([1, 2])]

    em = discord.Embed(title="COIN FLIP", description="Flipping a coin....")
    em.add_field(name=f"_Coin Says {coin_status}_", value="", inline=False)
    if coin_status == "HEADS":
        em.add_field(name=f"Yayy!! {heads_user_name} WON!", value="", inline=False)
    else:
        em.add_field(name=f"Yayy!! {tails_user_name} WON!", value="", inline=False)
    em.set_image(url=url)
    await ctx.send(embed=em)

# ==========================choose random alphabet==========================
async def choose_random_alphabet():
    alphabets = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
                 "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "x", "y", "z"]
    alphabet = random.choice(alphabets)
    return alphabet

#======================SING==============================    

@client.command(name="sing")
async def sing(ctx):
    if ctx.author.voice is None:
        await ctx.send("You are not connected to a voice channel.")
        return

    voice_channel = ctx.author.voice.channel

    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(voice_channel)
    else:

        vc = await voice_channel.connect()

    vc.play(discord.FFmpegPCMAudio('song.mp3'))

    while vc.is_playing():
        await asyncio.sleep(1)

    await vc.disconnect()


# ==========================POLL==========================

@client.command()
async def poll(ctx, question, *options):
    poll_embed = discord.Embed(title=question, color=0xFF5733)
    reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯']
    
    for i, option in enumerate(options):
        poll_embed.add_field(name=f"{reactions[i]} {option}", value="\u200b", inline=False)
    
    poll_message = await ctx.send(embed=poll_embed)
    
    for i in range(len(options)):
        await poll_message.add_reaction(reactions[i])


# ==========================REMIND==========================

@client.command()
async def reminder(ctx,time:int,*,msg):

    await ctx.send(f"Okay, I'll remind you in {60*time} seconds")

    while True:
        await s(60*time)
        await ctx.author.send(f'{msg}, {ctx.author.mention}')
        break

# ==========================TWILIO SAYS==========================

@client.command()
async def twilio_says(ctx,*,user_message):
    account_sid = accountSid
    auth_token = authToken
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=toNumber,
        from_=fromNumber,
        body=f"{user_message}"
    )
    await ctx.send("done ✅")

# ==========================CHATGPT==========================


@client.command()
async def chatgpt(ctx, *, writing=None):
    if writing == None:
        await ctx.send("You can add whatever you like, ex:- .chatgpt I was a boy somethinggs are there, or any random phrase, that you want to check if chatgpt has written")
    else:
        messages = [
            {"role": "system", "content": "You are a intelligent assistant."}]
        prompt = writing
        messages.append(
            {"role": "user", "content": prompt},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

    reply = chat.choices[0].message.content
    await ctx.send(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})

# ==========================BOOK==========================


@client.command()
async def book(ctx):
    await ctx.send("Do you want to book a table? yes or no")
    response = await client.wait_for('message', check=lambda m: m.author != client.user and m.channel == ctx.channel)

    if response.content == "yes":
        await ctx.send("For how many people do you want to the table be?")
        peopleLimit = await client.wait_for("message", check=lambda m: m.author != client.user and m.channel == ctx.channel)
        peopleLimit = int(peopleLimit.content)
        if peopleLimit > 4 or peopleLimit < 1:
            await ctx.send("The Limit is 4 and the minimum is 1")
        else:
            await ctx.send("Please enter the names of people who are eating along with you! all separated by space")
            peopleNames = await client.wait_for("message", check=lambda m: m.author != client.user and m.channel == ctx.channel)
            names = peopleNames.content.split()

            if len(names) != peopleLimit:
                await ctx.send("Please reuse .book, looks like you have not booked the table properly!")
            else:

                status = "people"
                if peopleLimit > 1:
                    status = "people"
                else:
                    status = "person"
                randomNo = random.randint(1, 10000)
                em = discord.Embed(
                    title=f"TABLE BOOKED #{randomNo}", description=f"A table has been booked for {peopleLimit} {status}\nNames are:- {str(names)}")
                await ctx.send(embed=em)
                await ctx.send(file=discord.File('pokemons/table.png'))

                orders = []

                for i in range(len(names)):
                    await ctx.send(f'what would you like to eat? {names[i]}')
                    message = await client.wait_for("message", check=lambda m: m.author != client.user and m.channel == ctx.channel)
                    orders.append(message.content)
                await ctx.send("The orders have been noted down!")
                await ctx.send("Would you like to order now? yes or no")
                response = await client.wait_for("message", check=lambda m: m.author != client.user and m.channel == ctx.channel)

                if response.content.lower() == 'yes':

                    orderCode = ""
                    times = [2, 1, 3]
                    randomNo = random.randint(1, 100000)
                    timeChosen = random.choice(times)

                    for i in range(5):
                        newCode = await choose_random_alphabet()
                        orderCode = orderCode + newCode
                    orderCode = orderCode + str(randomNo)
                    welcomeMessage = f"Welcome to the Hotel! 🍽️🍴!\n Your order will be ready in {timeChosen} minutes!\nOrder Code is ``{orderCode}``\n\n\nWe hope you enjoy the service!\n\n\n=======ORDERS======\n{orders}"
                    timeInSeconds = timeChosen*60

                    await ctx.author.send(f"Please wait {timeChosen} minutes until your order is finished being made!")
                    em = discord.Embed(
                        title=f'ORDER "{orderCode}"', description=f"{welcomeMessage}", color=0xFFFF00)
                    hotelPicture = "pokemons/hotel.png"
                    await ctx.send(file=discord.File(hotelPicture))
                    await ctx.send(embed=em)

                    await asyncio.sleep(timeInSeconds)
                    # await add_order_report(orderCode, ctx, str(orders), timeChosen)
                    await ctx.send(f"Your order is prepared! {ctx.author.mention}")

                    for i in range(len(orders)):
                        response = requests.get(
                            f"https://source.unsplash.com/500x500/?{str(orders)}", stream=True)
                        with open(f'food{i}.jpg', 'wb') as f:
                            f.write(response.content)
                            await ctx.send(file=discord.File(f'food{i}.jpg'))

                    pdf_canvas = canvas.Canvas(
                        "receipt.pdf", pagesize=landscape(letter))
                    pdf_canvas.setFont("Helvetica", 14)
                    receiptMessage = f"Deliverer:- Knock! Knock!\n{ctx.author}:Who's there?\nDeliverer: I am Armaan, from CodeBeetles Hotel, your order is ready, sir!\n{ctx.author}:Wow! That's Amazing!✨\n\n\n\n=================================================\n\n\n\nDeliverer:-hands over the order\n{ctx.author}:Thank You!\n\n==============FINANCIAL DETAILS==========\nOrder number:- {orderCode}\nTime Took:- {timeChosen} minutes\nDelivered By:- CodeBeetles Hotel\nDelivered At:- {datetime.now()}\nOrders for:- {names}\nOrders:- {orders}\n\nPrice:- $Free\n\nUse .feedback to give CodeBeetles Hotel a feedback or a tip! 😊\nThank you for ordering!\nHope to see you again!"
                    text = "==========RECIEPT===========\n"+receiptMessage
                    textobject = pdf_canvas.beginText(200, 550)
                    textobject.textLines(text)
                    pdf_canvas.drawText(textobject)
                    pdf_canvas.save()
                    receipt_pdf = File("receipt.pdf")
                    await ctx.send(file=receipt_pdf)
                    for i in range(len(orders)):
                        os.remove(f"food{i}.jpg")
                else:
                    await ctx.send("OK!")

    else:
        await ctx.send("OK!")


#======================jokes==============================    

@client.command()
async def joke(ctx):
    j = await Jokes()  # Initialise the class
    joke = await j.get_joke()  # Retrieve a random joke
    if joke["type"] == "single": # Print the joke
        await ctx.send(joke['joke'])
    else:
        print(joke["setup"])
        print(joke["delivery"])

# ==========================MAKE IMAGE==========================


@client.command()
async def make_image(ctx, *, prompt=None):
    if prompt == None:
        await ctx.send("You can add a prompt like:- .make_image boy standing outside")
    else:
        response = openai.Image.create(prompt=prompt, n=1, size="256x256",)
        await ctx.send(response["data"][0]["url"])

#==========================DESTROY==========================

@client.command()
async def destroy(ctx,user: discord.Member,*,reason = None, ):
    
    pokemons = ['pokemons/arceus.gif','pokemons/electrode.gif','pokemons/mewtwo.gif','pokemons/hehe.gif','pokemons/pikachu.gif','pokemons/destruction-1.gif','pokemons/destruction-2.gif','pokemons/destruction-3.gif','pokemons/destruction-4.gif','pokemons/destruction-5.gif','pokemons/destruction-6.gif','pokemons/destruction-7.gif'];
    pokemon = random.choice(pokemons)
    im = Image.open(pokemon)
    if reason and user != None:
        await ctx.send(f"Destroying {user.mention} for {reason}")
    frames = []
    for frame in ImageSequence.Iterator(im):
        d = ImageDraw.Draw(frame)
        fontsize=20
        font = ImageFont.truetype("arial.ttf", fontsize)
        d.text((230,100), f"I am gonna destroy\n{user.name}",font=font)
        del d

        b = io.BytesIO()
        frame.save(b, format="GIF")
        frame = Image.open(b)

        frames.append(frame)
        frames[0].save('out.gif', save_all=True, append_images=frames[1:])

    await ctx.channel.send(file=discord.File('out.gif'))    


myRandomNumberForGiveaway = 0

# ==========================PURGE==========================


@client.command()
async def purge(ctx, limit: int):
    await ctx.channel.purge(limit=limit)
    timestamp = datetime.now()
    time = timestamp.strftime(r"%I:%M %p")
    em = discord.Embed(title="Purge action",
                       description=f"Purge action taken by {ctx.author.name} at {time}")
    em.add_field(
        name=f"\n{limit} messages has been purged/deleted by {ctx.author}", value="")
    await ctx.send(embed=em)


#==========================NEW CHESS GAME==========================
@client.command()
async def new_chess_game(ctx):

        board = chess.Board()
        while not board.is_game_over():
            if board.turn == chess.WHITE:
                player = ctx.message.author
            else:
                player = "opponent"
            await ctx.send(f"{player}, it's your turn.")
            await ctx.send(board.unicode())
            move = await client.wait_for('message', check=lambda m: m.author != client.user and m.channel == ctx.channel)
            if move == ".stop":
                break
                return
            try:
                board.push_san(move.content)
            except ValueError:
                await ctx.send(f"Invalid move: {move.content}.")
                continue
            except chess.MoveError:
                await ctx.send(f"Invalid move: {move.content}.")
                continue

        result = board.result()
        if result == '1/2-1/2':
            await ctx.send("The game is a draw!")
        elif result == '1-0':
            await ctx.send(f"{ctx.message.author.mention} has won the game!")
        elif result == '0-1':
            await ctx.send(f"opponent has won the game!")
        else:
            await ctx.send("Error: Unknown game result.")

#==================== bot Info ======================    

@client.command()
async def botinfo(ctx):
    embed = discord.Embed(title="Bot Information", description="This bot was created by Armaan and Ayush.", color=0x00ff00)
    embed.set_thumbnail(url=client.user.avatar)
    embed.add_field(name="Bot Name", value=client.user.name, inline=True)
    embed.add_field(name="Bot ID", value=client.user.id, inline=True)
    embed.add_field(name="Bot Prefix", value=client.command_prefix, inline=True)
    embed.add_field(name="Server Count", value=len(client.guilds), inline=True)
    embed.add_field(name="User Count", value=len(client.users), inline=True)
    embed.add_field(name="Library", value="Discord.py", inline=True)
    embed.add_field(name="Discord.py Version", value=discord.__version__, inline=True)
    embed.set_footer(text="Bot created using Discord.py")
    await ctx.send(embed=embed)    



#==========================WHO IS==========================
@client.command()
async def whois(ctx,*,user: discord.Member = None):
    await open_store_house(user)
    data = await get_store_house_data()

    experience = data[str(user.id)]['experience']
    level = data[str(user.id)]['level']

    if user.nick == True:
        username = user.nick
    else:
        username = user.name;    
    em = discord.Embed(title = f"Who is {username}");
    joined_at = user.joined_at.strftime("%b %d, %Y, %T")
    joined_di = user.created_at.strftime("%b %d, %Y, %T")
    em.add_field(name=f"{username} joined {ctx.message.guild.name} at ",value=f"{joined_at}");
    em.add_field(name=f"{username} joined discord at ",value=f"{joined_di}",inline=False);
    em.add_field(name=f"{username}'s Level:-",value=f"{level}",inline=False)
    em.add_field(name=f"{username}'s Experience:-",value=f"{experience}",inline=False)

    pfp = user.avatar
    em.set_image(url=pfp)
    await ctx.send(embed = em);



#==========================youtube links access==========================
@client.command(name="youtubeAccess")
async def youtubeaccess(ctx):

    data = await get_store_house_data()

    if 'youtube' in data:
        status = data['youtube']['access']
    else:
        data['youtube'] = {}
        data['youtube']['access'] = "true"
        status = data['youtube']['acess']

    if status == "true":
        await ctx.send("Status:- Youtube links are allowed")
    else:
        await ctx.send("Status:- Youtube links are disallowed")

    await ctx.send("Would you like to change this? yes (yes for allowed) or no (no for disallowed)?")
    newsStatus = await client.wait_for('message', check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)

    
    if newsStatus.content == "yes":
            print("it's yes");
            data['youtube']['access'] = "true"
            await ctx.send("Settings updated successfully!")
    else:
            print("it's no");
            data['youtube']['access'] = "false"
            await ctx.send("Settings updated successfully!")      

    with open('ember/storehouse.json', 'w') as f:
        json.dump(data, f)                     



#======================PLAY (PARTIALLY WORKS :SOB:)==============================    

@client.command()
async def play(ctx, url):

    if ctx.message.content == ".stopmusicnow":
        await vc.disconnect()

    else:
        if ctx.author.voice is None:
            await ctx.send("You are not connected to a voice channel.")
            return

        voice_channel = ctx.author.voice.channel

        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(voice_channel)
        else:
            vc = await voice_channel.connect()

        try:
            video = pytube.YouTube(url)
            audio_url = video.streams.filter(only_audio=True).first().url
        except:
            await ctx.send("Sorry, I couldn't download the audio from that video.")
            return

        audio_source = discord.FFmpegPCMAudio(audio_url)
        vc.play(audio_source, after=lambda e: print(
            'Player error: %s' % e) if e else None)

        while vc.is_playing():
            await asyncio.sleep(1)

        await vc.disconnect()
        

#==========================MESSAGE LISTENER==========================

@client.listen('on_message')
async def message_listener(message):    
    global current_player
    data = await get_store_house_data()

    
    if client.user.mentioned_in(message):
        await message.channel.send("Hey bud, please don't ping me, LEMME PLAY chesssss, please? :face_holding_back_tears:")

   


    youtube_regex = r"(https?:\/\/(?:www\.)?youtube\.com\/\S+|https?:\/\/(?:www\.)?youtu\.be\/\S+)"
    if re.search(youtube_regex, message.content):

        if data['youtube']['access'] == "true":
            print('done')
        else:
            await message.delete();    

    if message.author.bot:
        return
    
    author_id = message.author.id
    current_time = time.time()
    
    channel = client.get_channel(int(message.channel.id))
    channel_name = str(channel.name)



    if message.author == client.user:
        return
    
    with open('ember/storehouse.json', 'r') as f:
        storehouse = json.load(f)

    if str(message.author.id) in storehouse:
        storehouse[str(message.author.id)]['experience'] += 1
    else:
        storehouse[str(message.author.id)]={}
        storehouse[str(message.author.id)]["level"]=0
        storehouse[str(message.author.id)]["experience"]=0
        storehouse[str(message.author.id)]["points"]=0
        storehouse[str(message.author.id)]["warnings"]=0
        storehouse[str(message.author.id)]["money"] = 0   
        storehouse[str(message.author.id)]['experience'] = 10

    exp = storehouse[str(message.author.id)]['experience']
    if exp in [10, 50, 150, 200, 250, 300, 350,400,450,500,650,700,750,900,1000,1200,1500,2000,3000,3500,5000,7000,8000,10000]:
        level = (exp // 50) + 1
        level = int(level)
        storehouse[str(message.author.id)]['level'] = level
        channel = client.get_channel(1101689511987138600)
        await channel.send(f"Congratulations {message.author.mention}! You leveled up to level {level}!")

    
    with open('ember/storehouse.json', 'w') as f:
        json.dump(storehouse, f)



    return
#==================== How are you? ====================== 
@client.command(name="How_are_you?")
async def howryou(ctx):
    await ctx.send("I am great :smile:, how is it going for you? :wave:")
    message = await client.wait_for('message',check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)

    if "good" in message.content:
        await ctx.send("ohh nice, glad to hear!")
    elif "bad" in message.content:
        await ctx.send("Ohh :(, what happened? feel free to share with me :)")
    else:
        await ctx.send("ohh -_-")        


#======================QUOTE==============================    

@client.command()
async def quote(ctx):
    category = 'happiness'
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    response = requests.get(api_url, headers={'X-Api-Key': 'f4uZV12fKgUGzJ38lmZzEg==CMrSupDNex2iMh2Y'})
    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)
        quote = data[0]['quote']
        await ctx.send(f"Quote:- {quote}")
    else:
        print("Error:", response.status_code, response.text)           

#==================== Translate ====================== 

@client.command()
async def translate(ctx, lang, *, text):
    translator = Translator(user_agent='Mozilla/5.0')
    translation = translator.translate(text, dest=lang)
    await ctx.send(f'Translation: {translation.text}')
    
    tts = gTTS(text=translation.text, lang=lang)
    file = io.BytesIO()
    tts.write_to_fp(file)
    file.seek(0)
    await ctx.send(file=discord.File(file, filename='translation.mp3'))

#======================TRIVIA==============================    

@client.command()
async def trivia(ctx):
        response = requests.get('https://opentdb.com/api.php?amount=1')
        question = response.json()['results'][0]

        embed = discord.Embed(title=question['category'], description=question['question'])
        for i, option in enumerate(question['incorrect_answers'] + [question['correct_answer']]):
            embed.add_field(name=f"Option {i+1}", value=option, inline=False)

        await ctx.send(embed=embed)

        # Wait for user response
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        msg = await client.wait_for('message', check=check, timeout=30)

        # Check if answer is correct
        if msg.content.lower() == question['correct_answer'].lower():
            await ctx.send(f"Correct! The answer was {question['correct_answer']}.")
        else:
            await ctx.send(f"Sorry, the correct answer was {question['correct_answer']}.")
    

#======================PING==============================    

@client.command()
async def ping(ctx):
    await ctx.send('Pong! Latency: {}ms'.format(round(client.latency * 1000)))

#======================WEATHER==============================    

@client.command()
async def weather(ctx, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=c5ee11a084d86fc7c3fa219524dae85a&units=metric'
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        data = response.json()
        description = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        await ctx.send(f"Current weather in {city}: {description.capitalize()}. Temperature is {temp}°C but feels like {feels_like}°C. Humidity is {humidity}% and wind speed is {wind_speed} m/s.")
    else:
        await ctx.send(f"Couldn't get weather data for {city}. Please try again.")
    

#======================OPEN STORE HOUSE==============================   

async def open_store_house(user):
    users = await get_store_house_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)]={}
        users[str(user.id)]["level"]=0
        users[str(user.id)]["experience"]=0
        users[str(user.id)]["points"]=0
        users[str(user.id)]["warnings"]=0
        users[str(user.id)]["money"] = 0   

    with open("ember/storehouse.json","w") as f:
        json.dump(users,f)   
    return True             

#======================GET STORE HOUSE DATA==============================    

async def get_store_house_data():
    with open("ember/storehouse.json","r") as f:
        data = json.load(f)

    return data   

client.run(token)    