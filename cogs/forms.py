import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure
from discord.ext.commands import errors

#DB
from pymongo import MongoClient

import random
import json
import utils.embed as embed
from utils.colors import *
from utils.roleexceptions import NotReplyingError

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


    def get_role(self, payload):
        
        guild_id = payload.guild_id
        channel_id = payload.channel_id
        message_id = payload.message_id

        guild = self.client.get_guild(payload.guild_id)
        author = guild.get_member(payload.user_id)

        if author.bot:
            return None

        listeners = self.reaction_db.find_one({"_id" : guild_id})["listeners"]
        
        # check if is the case to get roles to someone
        listener = next(filter(lambda listener: listener['ch_id'] == channel_id and listener['msg_id'] == message_id, listeners), None)

        if listener is None:
            return None
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

        return role

    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """
            This function checks if a reaction has been added, if its true the function 
            will check if there's an emoji associated to an role in the message.  
        """
        if payload.event_type != "REACTION_ADD":
            return
        
        guild = self.client.get_guild(payload.guild_id)
        author = guild.get_member(payload.user_id)
        role = self.get_role(payload)
        
        if role is not None:
            await author.add_roles(role)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """
            This function checks if a reaction has been added, if its true the function 
            will check if there's an emoji associated to an role in the message.  
        """
        if payload.event_type != "REACTION_REMOVE":
            return
        
        guild = self.client.get_guild(payload.guild_id)
        author = guild.get_member(payload.user_id)
        role = self.get_role(payload)
        
        if role is not None:
            await author.remove_roles(role)



    @commands.command()
    @has_permissions(administrator = True)
    async def addr(self, ctx, emoji: Union[discord.PartialEmoji, str], role: commands.RoleConverter):
        """
        This function will add a reaction to a Role Emoji Manager (Message) that you replied to.

        It's like say that the emoji (:happy:) is (@happy) ok?
        """
        
        if ctx.message.reference is None:
            # TODO: EMBED
            await ctx.send("Você precisa estar respondendo uma mensagem para poder usar este comando", delete_after=self.delete_system_message)
            return
        
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

        guild_id = message.guild.id
        channel_id = message.channel.id
        message_id = message.id

        # TODO: MELHORA ESSA QUERRY AI PO
        listeners = self.reaction_db.find_one({"_id" : guild_id})["listeners"]    
        listener = next(filter(lambda listener: listener['ch_id'] == channel_id and listener['msg_id'] == message_id, listeners), None)
        
        if listener is None:
            embedmsg = embed.createEmbed(title="ERRO!", 
            description= f"A mensagem selecionada não foi definida para manipular cargos",
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

                # IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                await message.add_reaction(emoji)
            except Exception as e:
                embedmsg = embed.createEmbed(title="ERRO!", 
                description= f"O bot não tem acesso ao emoji, por favor, tente utilizar um unicode ou nativo do servidor.",
                color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                fields=[
                ],
                img="https://cdn.discordapp.com/emojis/838992894291345440.png?v=1")

                await message.reply(embed=embedmsg, delete_after= self.delete_system_message)
            
            # IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            listener["reactions"].append({"emoji" : send, "role" : role.id})
            self.reaction_db.update({'_id': guild_id}, {'$set': {'listeners': listeners}})


    @commands.command()
    @has_permissions(administrator = True)
    async def remr(self, ctx, thing: Union[discord.PartialEmoji, str, discord.Role]):
        
        # TODO: remr and addr are same in a lot of parts
        if ctx.message.reference is None:
            # TODO: EMBED
            await ctx.send("Você precisa estar respondendo uma mensagem para poder usar este comando", delete_after=self.delete_system_message)
            return
        
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

        guild_id = message.guild.id
        channel_id = message.channel.id
        message_id = message.id

        # TODO: MELHORA ESSA QUERRY AI PO
        listeners = self.reaction_db.find_one({"_id" : guild_id})["listeners"]    
        listener = next(filter(lambda listener: listener['ch_id'] == channel_id and listener['msg_id'] == message_id, listeners), None)
        
        if listener is None:
            embedmsg = embed.createEmbed(title="ERRO!", 
            description= f"A mensagem selecionada não foi definida para manipular cargos",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
                ("Para funcionar", f".init emoji-role", False)
            ],
            img="https://cdn.discordapp.com/emojis/838992894291345440.png?v=1")

            await message.reply(embed=embedmsg, delete_after= self.delete_system_message)
        
        else:
            
            reactions = listener["reactions"]

            if type(thing) is discord.Role:
                filtered = next(filter(lambda react: react['role'] == thing.id, reactions), None)

                if filtered is not None:
                    to_remove = self.client.get_emoji(filtered['emoji'])

            else:
                if type(thing) is not str:
                    option = thing.id
                else:
                    option = thing
                to_remove = thing
                
                filtered = next(filter(lambda react: react['emoji'] == option, reactions), None)

            # Try it
            try:

                # IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                await message.clear_reaction(to_remove)
            except Exception as e:
                print(e)
                pass
            
            # IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            listener["reactions"].remove(filtered)
            self.reaction_db.update({'_id': guild_id}, {'$set': {'listeners': listeners}})

        return

    @remr.error
    @addr.error
    async def addrem_error(self, ctx, error):

        self.log.error(f"{error}")
        await ctx.send(error, delete_after = self.delete_system_message)


    async def init_role_react(self, ctx):
        guild_id = ctx.guild.id
        ch_id = ctx.channel.id
        msg_id = ctx.message.id 

        init = {
            "ch_id" : ch_id,
            "msg_id" : msg_id,
            "reactions" : []
        }

        self.reaction_db.update({'_id': guild_id}, {'$push': {'listeners': init}})
        self.log.debug("New Role Listener started")

        embedmsg = embed.createEmbed(title="Mensagem para gerenciamento de cargos iniciada!", 
                description= f"Para adicionar cargos basta responder a mensagem com .addr <emoji> <cargo>",
                color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                fields=[
                ],
                img="https://cdn.discordapp.com/emojis/838992894291345440.png?v=1")

        await ctx.message.reply(embed=embedmsg, delete_after= self.delete_system_message)


    @commands.command()
    @has_permissions(administrator = True)
    async def init(self, ctx, *, args: str):
        if args == 'emoji-role':
            await self.init_role_react(ctx)

# Setup
def setup(client):
    client.add_cog(Forms(client))

