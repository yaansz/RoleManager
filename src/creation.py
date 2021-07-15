import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure

# Embed + Colors + Random -> Pack to Send Messages
import embed
from colors import *
import random

# Timer
from auxiliar import time_to_delete

@commands.command(aliases=['criar'], pass_context=True)
@has_permissions(manage_roles = True)
async def create(ctx, *, args: str):
    """Create a new role with the given name
    """
    await ctx.message.delete(delay=2)

    guild = ctx.guild
    author = ctx.author
    msg = ctx.message

    result = await guild.create_role(name=args, mentionable=True)

    embedmsg = embed.createEmbed(title="Novo Cargo!", 
        description= f"O cargo <@&{result.id}> foi criado por <@{author.id}>",
        color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
        fields=[
            ("Como pegar?", f"Apenas digite .get <@&{result.id}> e ele será adicionado na sua conta", False)
        ],
        img="https://cdn.discordapp.com/emojis/862024241951145984.gif?v=1")

    await msg.channel.send(embed=embedmsg, delete_after = time_to_delete)
    
    return


@create.error
async def create_error(ctx, error):
    
    await ctx.message.delete(delay=2)

    if isinstance(error, commands.CheckFailure):
        await ctx.send("**Erro:** Você não pode criar um cargo!")
    else:
        await ctx.send(error)
