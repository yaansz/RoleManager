import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure

from typing import Union

import random
import json

import utils.embed as embed
from utils.colors import *

from pathlib import Path


class HumanResources(commands.Cog):
    """
        Manager is useful to create and delete roles.
        You can link a role to a chat or just create a role with a name that you like!
    """
    def __init__(self, client):
        self.client = client

        print("File      Path:", Path(__file__).absolute())
        print("Directory Path:", Path().absolute())

        # Some good paramters like timer and other shits
        with open(str(Path().absolute()) + '/database/utils.json', 'r') as f:
            info = json.load(f)

        self.delete_user_message = info['utils']['delete_user_message']
        self.delete_system_message = info['utils']['delete_system_message']

    @commands.command(aliases=['pegar', 'add', 'add_roles'], pass_context=True)
    async def get(self, ctx, role: Union[str, discord.Role] = "channel"):
        
        await ctx.message.delete(delay = self.delete_user_message)
        
        guild = ctx.guild
        author = ctx.author
        msg = ctx.message
        option = None

        if isinstance(role, discord.Role):
            pass
        elif role.lower() == "channel":
            option = msg.channel.category.name + " - " + msg.channel.name
        elif role.lower() == "category":
            option = msg.channel.category.name
        else:
            raise ValueError("")


        found = False
        if option is not None:
            for r in guild.roles:
                if r.name == option:
                    role = r
                    found = True
                    break
        
        if option != None and not found:
            embedmsg = embed.createEmbed(title="Cargo não existe!", 
                description= f"Infelizmente, o cargo que você deseja pegar não existe, pode tentar criar com o .linked ou .create",
                color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                fields=[
                ],
                img="https://cdn.discordapp.com/emojis/814603985842733107.png?v=1")

            await ctx.message.channel.send(embed=embedmsg, delete_after= self.delete_system_message)
            
            # END
            return   
        elif role in author.roles:
            embedmsg = embed.createEmbed(title="Você já possui esse cargo!", 
                description = f"Você está tentando adicionar um cargo que já possui!",
                color = rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                fields = [
                ],
                img="https://cdn.discordapp.com/emojis/765953530204127253.png?v=1")

            await ctx.message.channel.send(embed=embedmsg, delete_after= self.delete_system_message)

            # END
            return 
        else:
            await ctx.author.add_roles(role)

            embedmsg = embed.createEmbed(title="Cargo Atualizado!", 
                description= f"O cargo <@&{role.id}> foi adicionado ao perfil <@{ctx.author.id}>",
                color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                fields=[
                    ("Como pegar?", f"Apenas digite .get no chat do cargo ou .get <@&{role.id}> e ele será adicionado na sua conta", False)
                ],
                img="https://cdn.discordapp.com/emojis/854557933421461514.gif?v=1")

            await ctx.message.channel.send(embed=embedmsg, delete_after= self.delete_system_message)

        return None


    @get.error
    async def get_error(self, ctx, error):
        
        await ctx.message.delete(delay=2)

        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            await ctx.send("**Erro:** Você não pode adicionar esse cargo!", delete_after= self.delete_system_message)
        else:
            await ctx.send(error, delete_after= self.delete_system_message)

    
    @commands.command(aliases=['remover'], pass_context=True)
    async def remove(self, ctx, role: Union[str, discord.Role] = "channel"):
        
        await ctx.message.delete(delay = self.delete_user_message)
        
        guild = ctx.guild
        author = ctx.author
        msg = ctx.message
        option = None

        if isinstance(role, discord.Role):
            pass
        elif role.lower() == "channel":
            option = msg.channel.category.name + " - " + msg.channel.name
        elif role.lower() == "category":
            option = msg.channel.category.name
        else:
            raise ValueError("")

        found = False
        if option is not None:
            for r in guild.roles:
                if r.name == option:
                    role = r
                    found = True
                    break
        
        if option != None and not found:
            embedmsg = embed.createEmbed(title="Cargo não existe!", 
                description = f"Você está tentando remover um cargo que não existe!",
                color = rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                fields = [
                ],
                img="https://cdn.discordapp.com/emojis/814603985842733107.png?v=1")

            await ctx.message.channel.send(embed=embedmsg, delete_after = self.delete_system_message)
            
            # END
            return            

        if role not in author.roles:
            embedmsg = embed.createEmbed(title="Você não possui esse cargo!", 
                description = f"Você está tentando remover um cargo que não possui!",
                color = rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                fields = [
                ],
                img="https://cdn.discordapp.com/emojis/853000725822308412.png?v=1", delete_after= self.delete_system_message)

            await ctx.message.channel.send(embed=embedmsg, delete_after = self.delete_system_message)

            # END
            return 

        await ctx.author.remove_roles(role)

        embedmsg = embed.createEmbed(title="Cargo Atualizado!", 
            description= f"O cargo <@&{role.id}> foi removido do perfil <@{ctx.author.id}>",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),

            img="https://cdn.discordapp.com/emojis/815618837109276684.png?v=1")

        await ctx.message.channel.send(embed=embedmsg, delete_after= self.delete_system_message)

        return None

    @remove.error
    async def remove_error(self, ctx, error):
        
        await ctx.message.delete(delay = self.delete_user_message)

        await ctx.send(error, delete_after= self.delete_system_message)



# Setup
def setup(client):
    client.add_cog(HumanResources(client))

