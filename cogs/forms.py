import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure
from discord.ext.commands import errors

# Forms
from discord.ext.forms import Form

#DB
from pymongo import MongoClient

import random
import json
import utils.embed as embed
from utils.colors import *

import os
import logging

# ENV
from dotenv import dotenv_values
ENV = dotenv_values(os.path.dirname(os.path.abspath(__file__)) + "/../.env")

class Forms(commands.Cog):
    """
        Manager is useful to create and delete roles.
        You can link a role to a chat or just create a role with a name that you like!
    """
    def __init__(self, client):
        self.client = client

        # Some good paramters like timer and other shits
        with open(os.path.dirname(os.path.abspath(__file__)) + '/../database/utils.json', 'r') as f:
            info = json.load(f)

        # Just to log everything :D
        self.log = logging.getLogger(__name__)

        self.delete_user_message = info['utils']['delete_user_message']
        self.delete_system_message = info['utils']['delete_system_message']

        
        self.db_client = MongoClient(ENV['MONGODB'])
        self.guild_preferences_db = self.db_client[info['mongo']['database']][info['mongo']['collection']]
        self.reaction_db = self.db_client[info['mongo']['database']][info['mongo']['reaction']]


    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild_id = payload.guild_id
        channel_id = payload.channel_id
        message_id = payload.message_id

        listeners = self.reaction_db.find_one({"_id" : guild_id})["listeners"]

        print(f"PAYLOAD INFO: {payload.event_type} : USER ID: {payload.user_id} : Emoji ID: {payload.emoji.id}")

        if channel_id in [l["ch_id"] for l in listeners] and message_id in [l["msg_id"] for l in listeners]:
            print("Achei otario!")
        else:
            print("Ahchei n foi mal :(")

    @commands.command()
    async def add_reactions(self, ctx, emoji: discord.PartialEmoji, role: discord.Role):
        """
        This function will add a reaction to a Role Emoji Manager (Message) that you replied to.

        It's like say that the emoji (:happy) is (@happy) ok?
        """
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

        guild_id = message.guild.id
        channel_id = message.channel.id
        message_id = message.id

        # TODO: MELHORA ESSA QUERRY AI PO
        listeners = self.reaction_db.find_one({"_id" : guild_id})["listeners"]

        if channel_id in [l["ch_id"] for l in listeners] and message_id in [l["msg_id"] for l in listeners]:
            self.reaction_db.update({'_id': guild_id}, {'$push': {'listeners': [{"emoji" : emoji.id, "role" : role.id}]}})

        else:
            print("Ahchei n foi mal :(")

        print(message.content)

    @commands.command()
    async def init_role_react(self, ctx):
        guild_id = ctx.guild.id
        ch_id = ctx.channel.id
        msg_id = ctx.message.id 

        init = {
            "ch_id" : ch_id,
            "msg_id" : msg_id,
            "reacts" : []
        }

        self.log.debug("Update!")

        self.reaction_db.update({'_id': guild_id}, {'$push': {'listeners': init}})

# Setup
def setup(client):
    client.add_cog(Forms(client))

