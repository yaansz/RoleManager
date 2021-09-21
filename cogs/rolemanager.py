import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure

from utils.converters import CtxRoleConverter
from utils.utils import str2bool

from functools import reduce

import random
import json

import utils.embed as embed
from utils.colors import *

import os

#DB
from pymongo import MongoClient
import logging

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

        # Just to log everything :D
        self.log = logging.getLogger(__name__)

        # TODO: Loading things :P (I want to put it in a parent class, but i'm not sure at this moment)
        self.delete_user_message = info['utils']['delete_user_message']
        self.delete_system_message = info['utils']['delete_system_message']

        self.db_client = MongoClient(ENV['MONGODB'])
        self.guild_preferences_db = self.db_client[info['mongo']['database']][info['mongo']['collection']]


        self.channel_permissions = [
            "add_reactions",
            "administrator",
            "attach_files",
            "ban_members",
            "change_nickname",
            "connect",
            "create_instant_invite",
            "deafen_members",
            "embed_links",
            "external_emojis",
            "kick_members",
            "manage_channels",
            "manage_emojis",
            "manage_guild",
            "manage_messages",
            "manage_nicknames",
            "manage_permissions",
            "manage_roles",
            "manage_webhooks",
            "mention_everyone",
            "move_members",
            "mute_members",
            "priority_speaker",
            "read_message_history",
            "read_messages",
            "request_to_speak",
            "send_messages",
            "send_tts_messages",
            "speak",
            "stream",
            "use_external_emojis",
            "use_slash_commands",
            "use_voice_activation",
            "value",
            "view_audit_log",
            "view_channel",
            "view_guild_insights"
        ]


    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        '''
        Function to monitor guild channels and delete a role linked to a channel if the channel was moved to trash
        '''
        # Mudou de categoria
        if after.category == None:
            return 
        elif (before.category == None and after.category != None) or (before.category.id != after.category.id):
            
            guild = after.guild
            info = self.guild_preferences_db.find_one({"_id": guild.id})
            
            # Nome criado sempre que um chat é linkado a uma categoria!
            if before.category != None:
                role_name = before.category.name + " - " + before.name
            else:
                role_name = before.name

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
                        self.log.debug(f"Role {role_name} deleted (Channel moved to archives)!")

                        return


    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        
        target_type_channels = ["text", "category"]

        if channel.type.name.lower() not in target_type_channels:
            return
        elif channel.type.name.lower() == "text" and channel.category != None:
            option = channel.category.name + " - " + channel.name
        # I don't know why i did that shit, but i won't change
        elif channel.type.name.lower() == "text":
            option = channel.name
        else:
            option = channel.name

        for r in channel.guild.roles:
            if r.name == option:
                role = r
                
                await role.delete()
                self.log.debug(f"Role '{option}' deleted because linked channel was deleted")

                break 
        return

    @commands.command(aliases=['criar'], pass_context=True)
    @has_permissions(manage_roles = True)
    async def create(self, ctx, *, args: str = "channel"):
        """Create a new role with the given name
        """

        await ctx.message.delete(delay = self.delete_user_message)

        linked_keys = ["channel", "category"]

        role_name = self.linked_role(ctx, args) if args in linked_keys else args
    

        # Defining useful variables
        guild = ctx.guild
        author = ctx.author
        msg = ctx.message

        role_exists, role = await self.role_exists(ctx, role_name)

        if role_exists:
            embedmsg = embed.createEmbed(title="CARGO JÁ EXISTE!", 
            description= f"O cargo <@&{role.id}> já está no servidor, não precisa criar de novo!🍻",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
                ("Como pegar?", f"Apenas digite '.get' e ele será adicionado na sua conta", False)
            ],
            img="https://cdn.discordapp.com/emojis/814010519022600192.png?v=1")

            await msg.channel.send(embed=embedmsg, delete_after= self.delete_system_message)

        else:
            # New Role Created!
            new_role = await guild.create_role(name=role_name, mentionable=True)
            self.log.info( (f"New role '{new_role.name}' created in guild {guild.name} : {guild.id}").encode('ascii', 'ignore').decode('ascii') )


            # TODO: Especificar a mensagem de acordo com o cargo que foi criado!
            embedmsg = embed.createEmbed(title="Novo Cargo!", 
                description= f"O cargo <@&{new_role.id}> foi criado por <@{author.id}>",
                color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                fields=[
                    ("Como pegar?", f"Apenas digite .get no chat do cargo ou .get {new_role.name} e ele será adicionado na sua conta", False)
                ],
                img="https://cdn.discordapp.com/emojis/859150737509580800.gif?v=1")

            await msg.channel.send(embed=embedmsg)

        return


    @create.error
    async def create_error(self, ctx, error):
        
        await ctx.message.delete(delay = self.delete_user_message)
        
        if isinstance(error, CheckFailure):
            await ctx.send("**Erro:** Você não pode criar um cargo!", delete_after = self.delete_system_message)
        else:
            self.log.error(f"{error} - creation of a new role failed")
            await ctx.send(error, delete_after = self.delete_system_message)

    # TODO: Parent class too
    async def role_exists(self, ctx, role_name):
        """
            Method to check if a role exists in the current context, return a status and the role, if it exists.
        """
        conv = commands.RoleConverter()

        # If found it
        # The role already exists
        try:
            r = await conv.convert(ctx, role_name)   
            return True, r

        except commands.RoleNotFound: 
            return False, None
        
        
    # TODO: Put it in a parent class
    def linked_role(self, ctx, type: str):
        """
            This function is used to return a name to a role linked to a channel or category
        """
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

        return option;


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
            self.log.error(f"{error} - delete role failed")
            await ctx.send(error, delete_after = self.delete_system_message)

    
    async def _permission(self, ctx, role: CtxRoleConverter, mode: str, perm: str, can: bool):
        
        guild = ctx.guild
        author = ctx.author
        msg = ctx.message

    
        overwrite = discord.PermissionOverwrite()

        # Fundamental
        #  x.attr_name = s 
        # setattr(x, 'attr_name', s)
        if perm not in channel_permissions:
            self.log.debug( f"[.permission] Permission {perm} not found!")
            return
        
        setattr(overwrite, perm, can)
 
        if mode == 'category':
            category = ctx.channel.category
            await category.set_permissions(role, overwrite = overwrite)
        elif mode == 'channel':
            channel = ctx.channel
            await channel.set_permissions(role, overwrite = overwrite)
        else:
            # TODO: N ta funcionando
            await role.edit(permission = overwrite)
        
        self.log.debug( (f'Permission {perm} was changed to {can} in role {role.name} in current category').encode('ascii', 'ignore').decode('ascii') )

        fb = 'Permitido' if can else 'Proibido'

        embedmsg = embed.createEmbed(title="Permissão alterada!", 
                description= f"O cargo <@&{role.id}> foi atualizado por <@{author.id}>",
                color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                fields=[
                    (f"Permissão '{perm}'", f"Atualizada para {fb}", False)
                ],
                img="https://cdn.discordapp.com/emojis/765969524897218594.png?v=1")

        await msg.channel.send(embed=embedmsg)


        return

    @commands.command(pass_context=True)
    @has_permissions(manage_roles = True, manage_channels = True)
    async def permission(self, ctx, *, args: str = ""):
        """
        Arg List:

        ctx  -> Discord Context
        role -> CtxRoleConverter
        mode -> channel, category or role
        perm -> permission to change
        bool -> bool

        """

        await ctx.message.delete(delay = self.delete_user_message)

        splitted_args = args.split(' ')

        if len(splitted_args) < 4 or args == "":
            # Just for now
            self.log.debug("[.permission] Missing args")

            await self.permission_tutorial(ctx)

            return;

        can = str2bool(splitted_args[-1])
        perm = splitted_args[-2]
        mode = splitted_args[-3]

        role_name = ' '.join(splitted_args[:-3])

        status, role = await self.role_exists(ctx, role_name)

        await self._permission(ctx, role, mode, perm, can)


    async def permission_tutorial(self, ctx):

        embedmsg = embed.createEmbed(title="Configurações de Permissões!", 
                description= f"Verifique a lista de argumentos e permissões",
                color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                fields=[
                    (f"Argumentos", f"""role -> Role
                                        mode -> channel, category or role
                                        perm -> permission to change
                                        bool -> bool""", False),
                    (f"Permissões", "\n".join([item for item in self.channel_permissions]), False)
                ],
                img="https://cdn.discordapp.com/emojis/767241157003837460.png?v=1")

        await ctx.send(embed=embedmsg)

# Setup
def setup(client):
    client.add_cog(RoleManager(client))

