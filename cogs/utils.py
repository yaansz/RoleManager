import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure

from typing import Union

import random
import json

import utils.embed as embed
from utils.colors import *

import os

# ENV
from dotenv import dotenv_values
ENV = dotenv_values(os.path.dirname(os.path.abspath(__file__)) + "/../.env")

class Utils(commands.Cog):
    """
        Manager is useful to create and delete roles.
        You can link a role to a chat or just create a role with a name that you like!
    """
    def __init__(self, client):
        self.client = client

        # Some good paramters like timer and other shits
        with open(os.path.dirname(os.path.abspath(__file__))  + '/../database/utils.json', 'r') as f:
            info = json.load(f)

        self.delete_user_message = info['utils']['delete_user_message']
        self.delete_system_message = info['utils']['delete_system_message']

    @commands.command(aliases=['lista', 'roles'], pass_context=True)
    async def rolelist(self, ctx):

        await ctx.message.delete(delay= self.delete_user_message)
            
        bot_member = ctx.guild.get_member(self.client.user.id)

        highest_bot_role = bot_member.roles[-1]
        
        combine = []

        lst = ""

        string = "Lista: "
        
        #fields = [("Lista: ", "⠀⠀", False)]
        fields = []

        for r in ctx.guild.roles:
            #list += "<@&{0.id}>".format(r) + "\n"
            temp = ("<@&{0.id}>\n".format(r) if r.name != "@everyone" and r < highest_bot_role and not r.is_bot_managed() else "")

            if len(lst + temp) >= 1024:
                fields.append((string, lst, False))
                string = "⠀⠀"
                lst = ""
            else:
                lst += temp 

        if fields == []:
            fields.append((string, lst, False))


        fields.append(("Como pegar?", f"Apenas digite .get no chat do cargo ou .get <@ do cargo> e ele será adicionado na sua conta", False)
        )

        embedmsg = embed.createEmbed(title="Lista de Cargos!", 
            description= f"Veja todos os cargos que você pode pegar! :)",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=fields,
            img="https://cdn.discordapp.com/emojis/812796371638812684.png?v=1")

        await ctx.message.channel.send(embed=embedmsg)

    # PROBLEMAS PARA ATUALIZAR O CODIGO DO COLOR, EXIGE LEITURA

    @commands.command(aliases=['cor', 'setcolor'], pass_context=True)
    @has_permissions(manage_roles = True)
    async def color(self, ctx, role: discord.Role, *, args: str):

        await ctx.message.delete(delay= self.delete_user_message)
    
        if is_bgcolor(args):

            args = args.lstrip('#')
            args = tuple(int(args[i:i+2], 16) for i in (0, 2, 4))
            
            rgb = rgb_to_int(args)
            
            await role.edit(colour=discord.Colour(rgb))

            embedmsg = embed.createEmbed(title="Cor Atualizada!", 
            description= f"O cargo <@&{role.id}> teve sua cor atualizada por <@{ctx.author.id}>",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
                ("Como pegar?", f"Apenas digite .get no chat do cargo ou .get <@&{role.id}> e ele será adicionado na sua conta", False)
            ],
            img="https://cdn.discordapp.com/emojis/859495798143057940.png?v=1")

            await ctx.message.channel.send(embed=embedmsg, delete_after= self.delete_system_message)

        else:
            await ctx.send("**Erro:** Código inválido!")

        return None

    @color.error
    async def color_error(self, ctx, error):
        
        await ctx.message.delete(delay=2)

        if isinstance(error, commands.CheckFailure):
            await ctx.send("**Erro:** Você não pode alterar um cargo!", delete_after = self.delete_system_message)
        else:
            await ctx.send(error, delete_after = self.delete_system_message)
    

    @commands.command(pass_context=True)
    async def changenickname(self, ctx, *, args: str):
        """Create a new role with the given name
        """
        await member.edit(nick=args)

    @changenickname.error
    async def changenickname_error(self, ctx, error):
        
        await ctx.message.delete(delay=2)

        await ctx.send(error, delete_after = self.delete_system_message)



# Setup
def setup(client):
    client.add_cog(Utils(client))

