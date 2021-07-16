import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure
import random
import copy
from typing import Union


# My things
import status.status as status
import utils.embed as embed
from utils.colors import *

import os
import pathlib
from pathlib import Path
pathlib.Path().resolve()

from dotenv import dotenv_values

ENV = dotenv_values(os.path.dirname(os.path.abspath(__file__)) + "/.env")
print("ENV: " + str(ENV))

INITIAL_EXTENSIONS = [
    'cogs.manager',
    'cogs.humanresources',
    'cogs.utils'
]

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)

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


@bot.event
async def on_guild_channel_update(before, after):
    '''
    Function to monitor guild channels and delete a role linked to a channel if the channel was moved to trash
    '''
    # Mudou de categoria
    if before == None or after == None:
        return 

    if before.category.name != after.category.name:
        print(f"Canal '{after.name}' mudou de '{before.category.name}' para {after.category.name}")
    
        # TODO - Memória para o Boninho My Friend
        ids = [851546649599279124, 864639672177262592]
        
        guild = after.guild


        # Nome criado sempre que um chat é linkado a uma categoria!
        role_name = before.category.name + " - " + before.name

        # Categoria que devo deletar o cargo
        if after.category.id in ids:

            print("ID encontrado")

            for r in guild.roles:
                if r.name == role_name:
                    await r.delete()
                    await after.send(f"O cargo {role_name} foi deletado!")
                    return


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


# Official
# bot.run("ODY0NTU5MjM5MTg3NTI5NzQ5.YO3NiQ.maahbMxUj_p5Yyga8eXA3H9O_uY")

# Test
bot.run(ENV['DISCORD_RM_TOKEN'])
