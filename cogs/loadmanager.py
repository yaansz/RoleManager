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


    @load.error
    async def owner_error(error, ctx):
        if isinstance(error, commands.MissingPermissions):
            ctx.send("Você não tem permissão para executar o comando!")

    @commands.command()
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
    async def reload(self, ctx, extension: str):
        
        await ctx.message.delete(delay = self.delete_user_message)
        
        self.client.reload_extension(f"cogs.{extension}")

        await ctx.message.delete(delay = self.delete_user_message)
        
        embedmsg = embed.createEmbed(title="Extensão recarregada com sucesso!", 
            description= f"A extensão '{extension}' foi recarregada!.",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
            ],
            img="https://cdn.discordapp.com/emojis/767196592490807347.png?v=1")

        # Send that shit
        await ctx.send(embed=embedmsg, delete_after = self.delete_system_message)

    
    @commands.command()
    async def reloadall(self, ctx):
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
        

        await ctx.message.delete(delay = self.delete_user_message)
        

        embedmsg = embed.createEmbed(title="As extensões foram carregadas!", 
            description= f"A extensão '{extension}' foi carregada!.",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
                ("Falhas?", lst if lst != "" else "Não!" , True)
            ],
            img="https://cdn.discordapp.com/emojis/767196592490807347.png?v=1")

        # Send that shit
        await ctx.send(embed=embedmsg, delete_after = self.delete_system_message)

# Setup
def setup(client):
    client.add_cog(LoadManager(client))

