#!/usr/bin/env python3

import os
import sys
import random
import subprocess
try:
    import discord
    from openai import AsyncOpenAI
    from dotenv import dotenv_values
except ImportError:
    print("Please install the required packages by running 'pip install -r requirements.txt' or using apt")
    print("if you're on a Debian-based system 'apt install python3-discord python3-openai python3-dotenv'")
    exit(1)

class HoneyBot:
    def __init__(self):
        self.openai_client = None
        self.config = None
        self.load_secrets()

        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.client = discord.Client(intents=self.intents)
        self.client.event(self.on_ready)
        self.client.event(self.on_message)

    def load_secrets(self):
        # Load API key and organization from .env file
        path = os.path.dirname(os.path.realpath(__file__)) + os.sep
        if not os.path.exists(path + '.env'):
            print('Please create a .env file with your OpenAI API key, organization and Discord bot token')
            sys.exit(1)
        self.config = dotenv_values(path + ".env")
        self.openai_client = AsyncOpenAI(api_key=self.config['OPENAI_API_KEY'], organization=self.config['OPENAI_ORGANIZATION'])
        if self.openai_client is None:
            print('Could not load valid OpenAI API key and organization from .env file')
            sys.exit(1)

    async def howto(self, question, mode='ubuntu'):
        m = 'gpt-4o'
        system = 'You are a CLI assistant. Provide only the command, no explanations or extra text.'
        prompt = f'Provide the {mode} command-line command to ' + question
        try:
            response = await self.openai_client.chat.completions.create(model=m, messages=[{'role': 'system', 'content': system}, {'role': 'user', 'content': prompt}])
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

    def morn(self):
        things = [
            'chips', 'husdjur', 'demoner', 'jesus', 'popcorn', 'bullar', 'saft', 'ärtor', 'pengar', 'godis', 'kaffe', 'te', 'kebab', 'pizza', 'paket', 'mamma', 'tandkräm', 'gröt', 'AK47', 'proteinshake', 'ägg', 'pannkakor', 'fiskbullar', 'köttbullar', 'spaghetti', 'nudlar', 'flingor', 'apelsinjuice', 'ostmackor', 'havregryn', 'strumpor', 'byxor', 'solrosfrön', 'senap', 'ketchup', 'små rymdgubbar', 'tomtenissar', 'ostbågar', 'rostad majs', 'lillasyster', 'citronbitare', 'fiskpinnar', 'knäckebröd', 'julmust'
        ]
        places = [
            'på spisen', 'i ugnen', 'i torkskåpet', 'under sängen', 'bakom soffan', 'på dagis', 'hos rektorn', 'i himlen', 'i hallen', 'i kyrkan', 'i fotöljen', 'i gondolen', 'i Sherwoodskogen', 'i kaffekoppen', 'i blodomloppet', 'i magen', 'i flaskan', 'i badrumsskåpet', 'i toaletten', 'på nätet', 'på toasitsen', 'på golvet', 'på vinden', 'på taket', 'på stolen', 'på hatthyllan', 'på varmvattenpumpen', 'på bänken', 'i båten', 'på steam', 'på ICA', 'på netflix', 'på smörgåsbordet', 'på terassen', 'i kylen', 'i Tyskland', 'i ryggsäcken', 'i postlådan', 'i magväskan', 'i kaffekoppen', 'i fickan', 'i tomtens hatt', 'i skogen', 'i micron', 'i handfatet', 'i tänderna', 'i helvetet'
        ]
        return f'Morn, {random.choice(things)} finns {random.choice(places)}'

    def commands(self):
        return [
            '!howto <question> - Get a Ubuntu command-line for a specific task',
            '!powershell <question> - Get a PowerShell command-line for a specific task',
            '!morn - Get a random "Morn" message',
            '!vecka - Get the current week number',
            '!insult - Insult the named user',
            '!compliment - Compliment the named user'
        ]

    async def vecka_nu(self):
        cmd = ["curl", "-s", "https://vecka.nu/", "-H", "user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output, _ = subprocess.Popen(["html2markdown"], stdin=process.stdout, stdout=subprocess.PIPE).communicate()
        return output.decode("utf-8").strip()

    async def insult(self, username):
        username = username.strip()
        if len(username) < 1:
            username = None
        m = 'gpt-4o'
        system = 'You are a sarcastic but lighthearted assistant. Generate a humorous insult that is witty but not offensive.'
        prompt = f'Generate a funny and witty insult that is lighthearted and playful.'
        if username:
            prompt = f'Generate a funny and witty insult directed at {username} that is lighthearted and playful.'
        try:
            response = await self.openai_client.chat.completions.create(model=m, messages=[{'role': 'system', 'content': system}, {'role': 'user', 'content': prompt}])
        except Exception as e:
            return f'Error: {str(e)}'
        md = response.model_dump()
        text = md['choices'][0]['message']['content']
        return text.strip()

    async def compliment(self, username):
        if len(username) < 1:
            username = None
        m = 'gpt-4o'
        system = 'You are a positive and encouraging assistant. Generate a genuine and uplifting compliment that is warm and friendly.'
        prompt = 'Generate a sincere and uplifting compliment that makes someone feel valued and appreciated.'
        if username:
            prompt = f'Generate a sincere and uplifting compliment directed at {username} that makes them feel valued and appreciated.'
        try:
            response = await self.openai_client.chat.completions.create(model=m, messages=[{'role': 'system', 'content': system}, {'role': 'user', 'content': prompt}])
        except Exception as e:
            return f'Error: {str(e)}'
        md = response.model_dump()
        text = md['choices'][0]['message']['content']
        return text.strip()

    async def on_ready(self):
        print(f'Logged in as {self.client.user}')

    async def on_message(self, message):
        if message.author == self.client.user:
            return
        lower = message.content.lower()
        if message.channel.id == int(self.config['DISCORD_CHANNEL_ID']):
            if lower.startswith('!howto'):
                question = message.content[6:]
                await message.channel.send(await self.howto(question))
            elif lower.startswith('!powershell'):
                question = message.content[11:]
                await message.channel.send(await self.howto(question, mode='powershell'))
            elif lower.startswith('!morn'):
                await message.channel.send(self.morn())
            elif lower.startswith('!vecka'):
                await message.channel.send(await self.vecka_nu())
            elif lower.startswith('!insult'):
                await message.channel.send(await self.insult(message.content[7:]))
            elif lower.startswith('!compliment'):
                await message.channel.send(await self.compliment(message.content[11:]))
            elif lower.startswith('!commands'):
                for line in self.commands():
                    await message.channel.send(line)

    def run(self):
        self.client.run(self.config['DISCORD_BOT_TOKEN'])

# main
bot = HoneyBot()
bot.run()
