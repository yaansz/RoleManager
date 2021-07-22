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

        
        self.db_client = MongoClient(ENV['MONGODB'])
        self.guild_preferences_db = self.db_client[info['mongo']['database']][info['mongo']['collection']]
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        
        if msg.content == "reset rolemanager":
            try:
                self.guild_preferences_db.delete_one({"_id": msg.guild.id})
            except:
                pass
            await self.on_guild_join(msg.guild)
            await msg.reply("Preferências do bot foram restauradas aos valores padrões!")
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
    
        info = {

            "_id": guild.id,
            "prefix": '.', 
            "lang": "pt-br",
            "archives": None
        }

        g_id = self.guild_preferences_db.insert_one(info).inserted_id

        return


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        
        self.guild_preferences_db.delete_one({"_id": guild.id})

        return

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        return


    @commands.command(pass_context=True)
    @has_permissions(manage_roles = True)
    async def setprefix(self, ctx, prefix: str):
        """Create a new role with the given name
        """

        self.guild_preferences_db.update_one({'_id': ctx.guild.id}, 
        {'$set': {'prefix': prefix}})

        embedmsg = embed.createEmbed(title="Prefixo atualizado!", 
                    description= f"O novo prefixo do servidor agora é '{prefix}'",
                    color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                    fields=[
                    ],
                    img="https://cdn.discordapp.com/emojis/808769255952089099.png?v=1")

        await ctx.message.channel.send(embed=embedmsg)

        return

    
    @commands.command(pass_context=True)
    @has_permissions(manage_roles = True)
    async def test(self, ctx):
        """Create a new role with the given name
        """

        await ctx.message.delete(delay = self.delete_user_message)

        embedmsg = embed.createEmbed(title="Testando!", 
                    description= f"Alo Alo Alo 4",
                    color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                    fields=[
                    ],
                    img="https://cdn.discordapp.com/emojis/808769255952089099.png?v=1")

        await ctx.message.channel.send(embed=embedmsg)

        return

    
    @commands.command(pass_context=True)
    @has_permissions(manage_channels = True)
    async def setarchives(self, ctx):
        
        await ctx.message.delete(delay = self.delete_user_message)

        self.guild_preferences_db.update_one({'_id': ctx.guild.id}, 
        {'$set': {'archives': ctx.channel.category.id}})

        guild = ctx.guild
        author = ctx.author
        msg = ctx.message

        embedmsg = embed.createEmbed(title="Categoria de arquivos atualizada!", 
            description= f"Os arquivos foram definidos na categoria '{ctx.channel.category.name}' por <@{ctx.author.id}>",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
            ],
            img="https://cdn.discordapp.com/emojis/443814368858341426.png?v=1")

        # Send that shit
        await msg.channel.send(embed=embedmsg)

        return

    @commands.command()
    async def preferences(self, ctx):

        info = self.guild_preferences_db.find_one({"_id": ctx.guild.id})

        guild = ctx.guild
        author = ctx.author
        msg = ctx.message

        try:
            archives = await commands.CategoryChannelConverter().convert(ctx, info['archives'])
            archives = archives.name
        except:
            archives = "Não definido"

        embedmsg = embed.createEmbed(title="Preferências do servidor", 
            description= f"Veja as opções definidas para o servidor",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
                ("Idioma", f"{info['lang']}", True),
                ("Prefixo", f"{info['prefix']}", True),
                ("Categoria Arquivos", f"{archives}", True)
            ],
            img="https://cdn.discordapp.com/emojis/443814368858341426.png?v=1")

        # Send that shit
        await msg.channel.send(embed=embedmsg)
    
        return

# Setup
def setup(client):
    client.add_cog(GuildManager(client))

