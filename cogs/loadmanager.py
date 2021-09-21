import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure

#DB
from pymongo import MongoClient

import random
import json

import utils.embed as embed
from utils.colors import *

import os

# ENV
from dotenv import dotenv_values
ENV = dotenv_values(os.path.dirname(os.path.abspath(__file__)) + "/../.env")

def isOwner(ctx):
    return ctx.author.id == 366342872892440586


class LoadManager(commands.Cog):
    """
        Manager is useful to create and delete roles.
        You can link a role to a chat or just create a role with a name that you like!
    """
    def __init__(self, client):
        self.client = client

        # Some good paramters like timer and other shits
        with open(os.path.dirname(os.path.abspath(__file__)) + '/../database/utils.json', 'r') as f:
            info = json.load(f)

        self.delete_user_message = info['utils']['delete_user_message']
        self.delete_system_message = info['utils']['delete_system_message']

        
        self.db_client = MongoClient(ENV['MONGODB'])
        self.guild_preferences_db = self.db_client[info['mongo']['database']][info['mongo']['collection']]

       
    @commands.command()
    @commands.check(isOwner)
    async def load(self, ctx, extension: str):
        
        await ctx.message.delete(delay = self.delete_user_message)

        self.client.load_extension(f"cogs.{extension}")
        
        embedmsg = embed.createEmbed(title="Extensão carregada com sucesso!", 
            description= f"A extensão '{extension}' foi carregada!.",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
            ],
            img="https://cdn.discordapp.com/emojis/767196592490807347.png?v=1")

        # Send that shit
        await ctx.send(embed=embedmsg, delete_after = self.delete_system_message)


    @commands.command()
    @commands.check(isOwner)
    async def unload(self, ctx, extension: str):

        await ctx.message.delete(delay = self.delete_user_message)
        
        self.client.unload_extension(f"cogs.{extension}")
        
        embedmsg = embed.createEmbed(title="Extensão descarregada com sucesso!", 
            description= f"A extensão '{extension}' foi descarregada!.",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
            ],
            img="https://cdn.discordapp.com/emojis/766457934905081887.png?v=1")

        # Send that shit
        await ctx.send(embed=embedmsg, delete_after = self.delete_system_message)

        
    
    @commands.command()
    @commands.check(isOwner)
    async def reload(self, ctx, extension: str):

        await ctx.message.delete(delay = self.delete_user_message)

        self.client.reload_extension(f"cogs.{extension}")
        
        embedmsg = embed.createEmbed(title="Extensão recarregada com sucesso!", 
            description= f"A extensão '{extension}' foi recarregada!.",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
            ],
            img="https://cdn.discordapp.com/emojis/767196592490807347.png?v=1")

        # Send that shit
        await ctx.send(embed=embedmsg, delete_after = self.delete_system_message)

    
    @commands.command()
    @commands.check(isOwner)
    async def reloadall(self, ctx):
        
        await ctx.message.delete(delay = self.delete_user_message)

        with open(os.path.dirname(os.path.abspath(__file__))  + '/../database/utils.json', 'r') as f:
            extensions = json.load(f)["INITIAL_EXTENSIONS"]

        lst = ""

        # Extensions
        for extension in extensions:
            try:
                self.client.reload_extension(extension)
            except Exception as e:
                lst += 'Falha ao recarregar {}\n{}: {}\n'.format(
                    extension, type(e).__name__, e)
        
        
        embedmsg = embed.createEmbed(title="As extensões foram carregadas!", 
            description= f"As extensões foram recarregada!.",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
                ("Falhas?", lst if lst != "" else "Não!" , True)
            ],
            img="https://cdn.discordapp.com/emojis/767196592490807347.png?v=1")

        # Send that shit
        await ctx.send(embed=embedmsg, delete_after = self.delete_system_message)

    @load.error
    @unload.error
    @reloadall.error
    async def owner_error(self, ctx, error):
        
        await ctx.message.delete(delay = self.delete_user_message)
        
        if isinstance(error, CheckFailure):
            
            embedmsg = embed.createEmbed(title="Você não pode executar esse comando!", 
            description= f"Comando exclusivo para os desenvolvedores do bot",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
            ],
            img="https://cdn.discordapp.com/emojis/844662458622935092.png?v=1")

            await ctx.send(embed=embedmsg, delete_after = self.delete_system_message)
        else:
    
            await ctx.send(error, delete_after= self.delete_system_message)


# Setup
def setup(client):
    client.add_cog(LoadManager(client))

