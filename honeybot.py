#!/usr/bin/env python3

import os
import sys
import random
try:
    import discord
    from openai import OpenAI
    from dotenv import dotenv_values
except ImportError:
    print("Please install the required packages by running 'pip install -r requirements.txt' or using apt")
    print("if you're on a Debian-based system 'apt install python3-discord python3-openai python3-dotenv'")
    exit(1)

openai_client = None
config = None

def load_secrets():
    global openai_client, config
    # Load API key and organization from .env file
    # Don't forget to add .env to your .gitignore file
    path = os.path.dirname(os.path.realpath(__file__)) + os.sep
    if not os.path.exists(path + '.env'):
        print('Please create a .env file with your OpenAI API key, organization and Discord bot token')
        sys.exit(1)
    config = dotenv_values(path + ".env")
    openai_client = OpenAI(api_key = config['OPENAI_API_KEY'], organization = config['OPENAI_ORGANIZATION'])
    if openai_client is None:
        print('Could not load valid OpenAI API key and organization from .env file')
        sys.exit(1)

def howto(question, mode='ubuntu'):
    m = 'gpt-4o'
    system = 'You are a CLI assistant. Provide only the command, no explanations or extra text.'
    prompt = f'Provide the {mode} command-line command to ' + question
    try:
        response = openai_client.chat.completions.create(model = m, messages = [{'role': 'system', 'content': system}, {'role': 'user', 'content': prompt}])
    except Exception as e:
        return f'Error: {str(e)}'
    md = response.model_dump()
    text = md['choices'][0]['message']['content']
    text = text.strip()
    if text.startswith('``'):
        lines = text.split('\n')
        if len(lines) > 1:
            text = lines[1]
    if text.startswith('`') or text.startswith('"') or text.startswith("'"):
        text = text[1:-1]
    return text

load_secrets()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# TODO: move morn to a separate file
things = [
    'chips', 'husdjur', 'demoner', 'jesus', 'popcorn', 'bullar', 'saft', 'ärtor', 'pengar', 'godis', 'kaffe', 'te', 'kebab', 'pizza', 'paket', 'mamma', 'tandkräm', 'gröt', 'AK47', 'proteinshake', 'ägg', 'pannkakor', 'fiskbullar', 'köttbullar', 'spaghetti', 'nudlar', 'flingor', 'apelsinjuice', 'ostmackor', 'havregryn', 'strumpor', 'byxor', 'solrosfrön', 'senap', 'ketchup', 'små rymdgubbar', 'tomtenissar', 'ostbågar', 'rostad majs', 'lillasyster', 'citronbitare', 'fiskpinnar', 'knäckebröd', 'julmust'
]

places = [
    'på spisen', 'i ugnen', 'i torkskåpet', 'under sängen', 'bakom soffan', 'på dagis', 'hos rektorn', 'i himlen', 'i hallen', 'i kyrkan', 'i fotöljen', 'i gondolen', 'i Sherwoodskogen', 'i kaffekoppen', 'i blodomloppet', 'i magen', 'i flaskan', 'i badrumsskåpet', 'i toaletten', 'på nätet', 'på toasitsen', 'på golvet', 'på vinden', 'på taket', 'på stolen', 'på hatthyllan', 'på varmvattenpumpen', 'på bänken', 'i båten', 'på steam', 'på ICA', 'på netflix', 'på smörgåsbordet', 'på terassen', 'i kylen', 'i Tyskland', 'i ryggsäcken', 'i postlådan', 'i magväskan', 'i kaffekoppen', 'i fickan', 'i tomtens hatt', 'i skogen', 'i micron', 'i handfatet', 'i tänderna', 'i helvetet'
]

def morn():
    return f'Morn, {random.choice(things)} finns {random.choice(places)}'

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    #print(f"Mottaget: '{message.content}' från {message.author} i kanal {message.channel.id}")
    if message.author == client.user:
        print('response: ' + message.content)
        # Ignore my own messages
        return

    # Respond to messages in the correct channel
    if message.channel.id == int(config['DISCORD_CHANNEL_ID']):
        if message.content.lower().startswith('!howto'):
            question = message.content[6:]
            print('!howto' + question)
            await message.channel.send(howto(question))

        elif message.content.lower().startswith('!powershell'):
            question = message.content[11:]
            print('!powershell' + question)
            await message.channel.send(howto(question, mode='powershell'))

        elif message.content.lower().startswith('!morn'):
            await message.channel.send(morn())

client.run(config['DISCORD_BOT_TOKEN'])
