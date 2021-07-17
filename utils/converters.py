import discord
from discord.ext import commands, tasks

class CtxRoleConverter(commands.Converter):

    async def convert(self, ctx, arguments="channel"):

        guild = ctx.guild
        author = ctx.author
        msg = ctx.message

        converter = commands.RoleConverter()
        found = False
        
        if arguments.lower() == "channel":
            arguments = msg.channel.category.name + " - " + msg.channel.name
        elif arguments.lower() == "category":
            arguments = msg.channel.category.name
        
        # If found it
        # The role already exists
        r = await converter.convert(ctx, arguments)
        
        # There is the role
        return r
        