import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure
import random
import copy
from typing import Union

# DB
from pymongo import MongoClient

# My things
import status.status as status
import utils.embed as embed
from utils.colors import *

import os

from dotenv import dotenv_values

# MONGO

client = MongoClient('mongodb://localhost:27017/')
guild_preferences_db = client['role-manager']['guild-preferences']

# ENV + INIT 

ENV = dotenv_values(os.path.dirname(os.path.abspath(__file__)) + "/.env")

INITIAL_EXTENSIONS = [
    'cogs.rolemanager',
    'cogs.humanresources',
    'cogs.utils',
    'cogs.guildmanager'
]

# BOT CONFIG

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = lambda cli, msg: guild_preferences_db.find_one({"_id": msg.guild.id})['prefix'], intents=intents)

# Extensions
for extension in INITIAL_EXTENSIONS:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print('Failed to load extension {}\n{}: {}'.format(
            extension, type(e).__name__, e))

# COMMANDS BELLOW 


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

    # Starting the loop
    update_status.start()


@tasks.loop(seconds=10)
async def update_status():
    '''
    Function to update the bot status
    '''
    #await bot.change_presence(activity=discord.Game(status[random.randint(0, len(status) - 1)]))
    result = random.choice(list(status.Status))
    
    if result == status.Status.Playing:
        await bot.change_presence(activity=discord.Game(name=random.choice(result.value)))
    elif result == status.Status.Streaming:
        await bot.change_presence(activity=discord.Streaming(name=random.choice(result.value), url="https://www.twitch.tv/yaansz"))
    elif result == status.Status.Listening:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=random.choice(result.value)))
    elif result == status.Status.Watching:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(result.value)))
    else:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=random.choice(result.value)))


@bot.event
async def on_command_error(ctx, error):
    print(error)



# TODO - deixar aquela caixa bonita lá

# REWRITE THAT SHIT


@bot.command(aliases=['ajuda'], pass_context=True)
async def commands(ctx):
    
    lst = ""
    lst += "`.create <role name>` - Comando para criar um cargo.\n"
    lst += "`.delete <default: current chat or @ mention role>` - Comando para deletar um cargo.\n"
    lst += "`.linked <default:channel or category>` - Comando para criar um cargo vinculado a um canal ou categoria\n"
    lst += "`.color <@ mention role> <color code hex>` - Comando para mudar a cor de um cargo.\n" 
    lst += "`.get <default: current chat or @ mention role>` - Comando para pegar um cargo.\n"
    lst += "`.remove <@ mention role>` - Comando para remover um cargo.\n"
    lst += "`.rolelist` - Comando para listar os cargos disponíveis.\n"
    lst += "`.canread <@ mention role> <True/False> <default: Channel or Category>` - Comando para permitir ou não a leitura de um chat\n"

    embedmsg = embed.createEmbed(title="Lista de Comandos!", 
        description= f"Veja todos os comandos disponíveis!",
        color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
        fields=[
            ("Lista: ", lst, False),
            
            ],
        img="https://cdn.discordapp.com/emojis/812796371638812684.png?v=1")

    await ctx.message.channel.send(embed=embedmsg)


# Test
bot.run(ENV['DISCORD_RM_TOKEN'])
