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

import os

import logging

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

        # Just to log everything :D
        self.log = logging.getLogger(__name__)

        self.delete_user_message = info['utils']['delete_user_message']
        self.delete_system_message = info['utils']['delete_system_message']

        
        self.db_client = MongoClient(ENV['MONGODB'])
        self.guild_preferences_db = self.db_client[info['mongo']['database']][info['mongo']['collection']]
        self.reaction_db = self.db_client[info['mongo']['database']][info['mongo']['reaction']]


    @commands.command(pass_context=True)
    @has_permissions(administrator = True)
    async def reset(self, ctx, msg = ""):
        
        await ctx.message.delete(delay = self.delete_user_message)

        if type(msg) is not str:
            msg = msg.content
        
        hardreset = "--hard" in msg
        feedback = "Preferências do bot foram restauradas aos valores padrões!"

        try:
            self.guild_preferences_db.delete_one({"_id": ctx.guild.id})

            if hardreset:
                # TODO: Deletar todas as mensagens de reação no --hard
                self.reaction_db.delete_one({"_id": ctx.guild.id})
                feedback += " Reações também foram deletadas"
                
        except:
            pass
        await self.on_guild_join(ctx.guild, hardreset)
        await ctx.reply(feedback)


    @commands.Cog.listener()
    async def on_message(self, msg):
        
        if msg.content.startswith("reset rolemanager"):
            
            ctx = await self.client.get_context(msg)

            if ctx.author.guild_permissions.administrator:
                await self.reset(ctx, msg)
            else:
                await ctx.reply("Você não tem permissão!", delete_after= self.delete_system_message)


    @commands.Cog.listener()
    async def on_guild_join(self, guild, hard = True):
    
        info = {
            "_id": guild.id,
            "prefix": '.', 
            "lang": "pt-br",
            "archives": None
        }


        self.log.info( f"New Guild: {info}")

        g_id = self.guild_preferences_db.insert_one(info).inserted_id
        
        if hard:
            react_info = {
                "_id": guild.id,
                "listeners": []
            }
            g_id = self.reaction_db.insert_one(react_info).inserted_id

        return


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        

        self.log.info( f"Guild {guild.name} : {guild.id} is no longer available.")

        self.guild_preferences_db.delete_one({"_id": guild.id})
        self.reaction_db.delete_one({"_id": guild.id})

        return

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        return


    @commands.command(pass_context=True)
    @has_permissions(administrator = True)
    async def prefix(self, ctx, prefix: str):
        """Create a new role with the given name
        """ 

        await ctx.message.delete(delay = self.delete_user_message)

        self.guild_preferences_db.update_one({'_id': ctx.guild.id}, 
        {'$set': {'prefix': prefix}})

        embedmsg = embed.createEmbed(title="Prefixo atualizado!", 
                    description= f"O novo prefixo do servidor agora é '{prefix}'",
                    color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                    fields=[
                    ],
                    img="https://cdn.discordapp.com/emojis/808769255952089099.png?v=1")

        await ctx.send(embed=embedmsg)

        self.log.info( f"Prefix of {ctx.guild.name} : {ctx.guild.id} was updated to {prefix}")

        return

    
    @commands.command(pass_context=True)
    @has_permissions(administrator = True)
    async def archives(self, ctx):
        
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
    

    @archives.error
    @prefix.error
    @reset.error
    async def guild_errors(self, ctx, error):
        
        await ctx.message.delete(delay = self.delete_user_message)

        if isinstance(error, CheckFailure):
            
            embedmsg = embed.createEmbed(title="Você não pode executar esse comando!", 
            description= f"Apenas administradores podem usar esse comando!",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
            ],
            img="https://cdn.discordapp.com/emojis/844662458622935092.png?v=1")

            await ctx.send(embed=embedmsg, delete_after = self.delete_system_message)
        
        elif isinstance(error, errors.MissingRequiredArgument):

            info = self.guild_preferences_db.find_one({"_id": ctx.guild.id}) 

            embedmsg = embed.createEmbed(title="Você não passou argumentos suficientes!", 
            description= f"Utilize '{info['prefix']}prefix 'Prefixo'' para setar um novo prefixo para o servidor.",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
            ],
            img="https://cdn.discordapp.com/emojis/852737778722275359.gif?v=1")

            await ctx.send(embed=embedmsg, delete_after = self.delete_system_message)


        else:
    
            await ctx.send(error, delete_after= self.delete_system_message)



    @commands.command()
    async def preferences(self, ctx):
        
        await ctx.message.delete(delay = self.delete_user_message)

        info = self.guild_preferences_db.find_one({"_id": ctx.guild.id})

        guild = ctx.guild
        author = ctx.author
        msg = ctx.message
        try:
            archives = await commands.CategoryChannelConverter().convert(ctx, str(info['archives']))
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

