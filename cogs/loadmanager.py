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
    async def load(self, ctx, extension: str):
        
        await ctx.message.delete(delay = self.delete_user_message)
        
        self.client.load_extension(f"cogs.{extension}")

    @commands.command()
    async def unload(self, ctx, extension: str):
        
        await ctx.message.delete(delay = self.delete_user_message)

        
        self.client.unload_extension(f"cogs.{extension}")
    
    @commands.command()
    async def reload(self, ctx, extension: str):
        
        await ctx.message.delete(delay = self.delete_user_message)
        
        self.client.reload_extension(f"cogs.{extension}")

    
    @commands.command()
    async def reloadall(self, ctx):
        with open(os.path.dirname(os.path.abspath(__file__))  + '/../database/utils.json', 'r') as f:
            extensions = json.load(f)["INITIAL_EXTENSIONS"]

        # Extensions
        for extension in extensions:
            try:
                self.client.reload_extension(extension)
            except Exception as e:
                print('Failed to load extension {}\n{}: {}'.format(
                    extension, type(e).__name__, e))

# Setup
def setup(client):
    client.add_cog(LoadManager(client))

