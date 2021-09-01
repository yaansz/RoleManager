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

from typing import Union

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
        """
            This function checks if a reaction has been added, if its true the function 
            will check if there's an emoji associated to an role in the message.  
        """
        if payload.event_type != "REACTION_ADD":
            return
        
        guild_id = payload.guild_id
        channel_id = payload.channel_id
        message_id = payload.message_id

        guild = self.client.get_guild(payload.guild_id)
        author = guild.get_member(payload.user_id)

        if author.bot:
            return

        listeners = self.reaction_db.find_one({"_id" : guild_id})["listeners"]
        
        # check if is the case to get roles to someone
        listener = next(filter(lambda listener: listener['ch_id'] == channel_id and listener['msg_id'] == message_id, listeners), None)

        if listener is None:
            return
        else:
            emoji = payload.emoji
            
            # unicode or custom?
            if emoji.is_custom_emoji():
                send = emoji.id
            else:
                send = emoji.name

            reacts = listener["reactions"]
            # the emoji is associated to a role?
            react = next(filter(lambda react: react['emoji'] == send, reacts), None)

            if react is not None:
                role = guild.get_role(react['role'])
                await author.add_roles(role)


    @commands.command()
    async def addr(self, ctx, emoji: Union[discord.PartialEmoji, str], role: discord.Role):
        """
        This function will add a reaction to a Role Emoji Manager (Message) that you replied to.

        It's like say that the emoji (:happy) is (@happy) ok?
        """
        # TODO: check  if it exists
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

        guild_id = message.guild.id
        channel_id = message.channel.id
        message_id = message.id

        # TODO: MELHORA ESSA QUERRY AI PO
        listeners = self.reaction_db.find_one({"_id" : guild_id})["listeners"]    
        listener = next(filter(lambda listener: listener['ch_id'] == channel_id and listener['msg_id'] == message_id, listeners), None)
        
        if listener is None:
            embedmsg = embed.createEmbed(title="ERRO!", 
            description= f"A mensagem selecionada não foi definida para pegar cargos",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
                ("Para funcionar", f".init emoji-role", False)
            ],
            img="https://cdn.discordapp.com/emojis/838992894291345440.png?v=1")

            await message.reply(embed=embedmsg, delete_after= self.delete_system_message)
        
        else:
            if type(emoji) is not str:
                processed_emoji = emoji
                send = emoji.id
            else:
                processed_emoji = emoji
                send = emoji
            
            # Try it
            try:
                await message.add_reaction(emoji)
            except Exception as e:
                embedmsg = embed.createEmbed(title="ERRO!", 
                description= f"O bot não tem acesso ao emoji, por favor, tente utilizar um unicode ou nativo do servidor.",
                color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                fields=[
                ],
                img="https://cdn.discordapp.com/emojis/838992894291345440.png?v=1")

                await message.reply(embed=embedmsg, delete_after= self.delete_system_message)
            
            listener["reactions"].append({"emoji" : send, "role" : role.id})
            self.reaction_db.update({'_id': guild_id}, {'$set': {'listeners': listeners}})

            
            # embedmsg = embed.createEmbed(title="Adicionado com sucesso!", 
            # description= f"Agora a reação {emoji} foi definida para o cargo <@&{role.id}>",
            # color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            # fields=[
            # ],
            # img="https://cdn.discordapp.com/emojis/838992894291345440.png?v=1")




    def init_role_react(self, ctx):
        guild_id = ctx.guild.id
        ch_id = ctx.channel.id
        msg_id = ctx.message.id 

        init = {
            "ch_id" : ch_id,
            "msg_id" : msg_id,
            "reactions" : []
        }

        self.log.debug("Update!")

        self.reaction_db.update({'_id': guild_id}, {'$push': {'listeners': init}})


    @commands.command()
    async def init(self, ctx, *, args: str):
        if args == 'emoji-role':
            self.init_role_react(ctx)

# Setup
def setup(client):
    client.add_cog(Forms(client))

