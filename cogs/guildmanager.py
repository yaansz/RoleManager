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


class GuildManager(commands.Cog):
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

        
        self.db_client = MongoClient('mongodb://localhost:27017/')
        self.guild_preferences_db = self.db_client['role-manager']['guild-preferences']
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
    
        info = {

            "_id": guild.id,
            "prefix": '.', 
            "lang": "pt-br",
            "trash": None
        }

        g_id = self.guild_preferences_db.insert_one(info).inserted_id

        return


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        
        self.guild_preferences_db.delete_one({"_id": guild.id})

        return


    @commands.command(pass_context=True)
    @has_permissions(manage_roles = True)
    async def setprefix(self, ctx, prefix: str):
        """Create a new role with the given name
        """

        self.guild_preferences_db.update_one({'_id': ctx.guild.id}, 
        {'$set': {'prefix': prefix}})

        return
    

    


# Setup
def setup(client):
    client.add_cog(GuildManager(client))

