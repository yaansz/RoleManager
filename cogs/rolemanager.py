import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure

import random
import json

import utils.embed as embed
from utils.colors import *

import os

# ENV
from dotenv import dotenv_values
ENV = dotenv_values(os.path.dirname(os.path.abspath(__file__)) + "/../.env")


class RoleManager(commands.Cog):
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
    

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        '''
        Function to monitor guild channels and delete a role linked to a channel if the channel was moved to trash
        '''
        # Mudou de categoria
        if before == None or after == None:
            return 

        if before.category.name != after.category.name:
            print(f"Canal '{after.name}' mudou de '{before.category.name}' para {after.category.name}")
            
            guild = after.guild
            info = guild_preferences_db.find_one({"_id": guild.id})
            
            # Nome criado sempre que um chat é linkado a uma categoria!
            role_name = before.category.name + " - " + before.name

            # Categoria que devo deletar o cargo
            if after.category.id == info['archives']:

                for r in guild.roles:
                    if r.name == role_name:
                        await r.delete()
                        embedmsg = embed.createEmbed(title="Cargo associado excluído!", 
                            description= f"O cargo '{role_name}' associado ao canal foi excluído devido a movimentação do mesmo para os arquivos.",
                            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                            fields=[
                            ],
                            img="https://cdn.discordapp.com/emojis/753575574546415656.png?v=1")

                        # Send that shit
                        await after.send(embed=embedmsg)
                        return


    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        
        target_type_channels = ["text", "category"]

        if channel.type.name.lower() not in target_type_channels:
            return


        if channel.type.name.lower() == "text" and channel.category != None:
            option = channel.category.name + " - " + channel.name
        elif channel.type.name.lower() == "text":
            option = channel.name
        else:
            option = channel.name

        for r in channel.guild.roles:
            if r.name == option:
                role = r
                await role.delete()
                break
                 
        return

    @commands.command(aliases=['criar'], pass_context=True)
    @has_permissions(manage_roles = True)
    async def create(self, ctx, *, args: str):
        """Create a new role with the given name
        """

        # Deleting the message in n seconds after it was sent
        await ctx.message.delete(delay = self.delete_user_message)

        # Defining useful variables
        guild = ctx.guild
        author = ctx.author
        msg = ctx.message

        # New Role Created!
        result = await guild.create_role(name=args, mentionable=True)

        # Embed Message
        embedmsg = embed.createEmbed(title="Novo Cargo!", 
            description= f"O cargo <@&{result.id}> foi criado por <@{author.id}>",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
                ("Como pegar?", f"Apenas digite .get <@&{result.id}> e ele será adicionado na sua conta", False)
            ],
            img="https://cdn.discordapp.com/emojis/862024241951145984.gif?v=1")

        # Send that shit
        await msg.channel.send(embed=embedmsg, delete_after = self.delete_system_message)
        
        return


    @create.error
    async def create_error(self, ctx, error):
        
        await ctx.message.delete(delay=2)

        if isinstance(error, CheckFailure):
            await ctx.send("**Erro:** Você não pode criar um cargo!", delete_after = self.delete_system_message)
        else:
            await ctx.send(error, delete_after = self.delete_system_message)


    @commands.command(aliases=['deletar'], pass_context=True)
    @has_permissions(manage_roles = True)
    async def delete(self, ctx, *, role: commands.RoleConverter):

        await ctx.message.delete(delay= self.delete_user_message)

        await role.delete()
        await ctx.send(f"**AVISO:** Cargo '{role.name}' apagado do servidor por <@{ctx.author.id}>!")


    @delete.error
    async def delete_error(self, ctx, error):
        
        await ctx.message.delete(delay = self.delete_user_message)

        if isinstance(error, CheckFailure):
            await ctx.send("**Erro:** Você não pode deletar um cargo!", delete_after = self.delete_system_message)
        else:
            await ctx.send(error, delete_after = self.delete_system_message)


    @commands.command(aliases=['linked'], pass_context=True)
    @has_permissions(manage_roles = True, manage_channels = True)
    async def linked_role(self, ctx, type: str = "channel"):
        """
            This function creates a role linked to a channel or a category, it's very useful to ping everyone who is interested to an specific chat, like a discipline or a very interesting topic
        """

        await ctx.message.delete(delay = self.delete_user_message)

        guild = ctx.guild
        author = ctx.author
        msg = ctx.message
        
        if type.lower() == "channel" and msg.channel.category != None:
            option = msg.channel.category.name + " - " + msg.channel.name
        elif type.lower() == "channel":
            option = msg.channel.name
        elif type.lower() == "category":
            option = msg.channel.category.name
        else:
            raise ValueError("")

        conv = commands.RoleConverter()
        found = False

        # If found it
        # The role already exists
        try:
            r = await conv.convert(ctx, option)
            found = True
        except commands.RoleNotFound: 
            pass
        
        if found:
            embedmsg = embed.createEmbed(title="CARGO JÁ EXISTE!", 
            description= f"O cargo <@&{r.id}> já está no servidor, não precisa criar de novo!🍻",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
                ("Como pegar?", f"Apenas digite '.get' e ele será adicionado na sua conta", False)
            ],
            img="https://cdn.discordapp.com/emojis/814010519022600192.png?v=1")

            await msg.channel.send(embed=embedmsg, delete_after= self.delete_system_message)

        else:
            new_role = await guild.create_role(name=option, mentionable=True)

            embedmsg = embed.createEmbed(title="Novo Cargo!", 
                description= f"O cargo <@&{new_role.id}> foi criado por <@{author.id}>",
                color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                fields=[
                    ("Como pegar?", f"Apenas digite .get no chat do cargo ou .get {new_role.name} e ele será adicionado na sua conta", False)
                ],
                img="https://cdn.discordapp.com/emojis/859150737509580800.gif?v=1")

            await msg.channel.send(embed=embedmsg)


    @linked_role.error
    async def linked_role_error(self, ctx, error):
        
        await ctx.message.delete(delay = self.delete_user_message)

        if isinstance(error, CheckFailure):
            await ctx.send("**Erro:** Você não pode criar um cargo!", delete_after= self.delete_system_message)
        elif isinstance(error, ValueError):
            await ctx.send("**Erro:** Opção inválida! Tente 'Channel' ou 'Category'")
        else:
            await ctx.send(error, delete_after = self.delete_system_message)


    @commands.command(aliases=['canRead', 'read', 'ler'], pass_context=True)
    @has_permissions(manage_roles = True, manage_channels = True)
    async def canread(self, ctx, role: discord.Role, canRead: bool, type: str = "channel"):
        
        await ctx.message.delete(delay = self.delete_user_message)

        if type == "category":
            category = ctx.channel.category

            if category != None:
                await category.set_permissions(role, view_channel = canRead)
                await ctx.send("Permissão alterada!", delete_after = self.delete_system_message)
        elif type == "channel":

            await ctx.channel.set_permissions(role, view_channel = canRead)
            await ctx.send("Permissão alterada!", delete_after = self.delete_system_message)


    @canread.error
    async def canread_error(self, ctx, error):
        
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send('**Erro:** Formato inválido.\nDigite ".canread <cargo> <bool: pode> <bool: é canal>"', 
                delete_after = self.delete_system_message)



# Setup
def setup(client):
    client.add_cog(RoleManager(client))

