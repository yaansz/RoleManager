# This example requires the 'members' privileged intents

import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure
import random
import binascii

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

    # Starting the loop
    update_status.start()
    

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@tasks.loop(seconds=10)
async def update_status():

    status = ['Muito ocupado', 'Não pertube', 'Jogando', 'Talvez?', 'Sim', 'Não']

    await bot.change_presence(activity=discord.Game(status[random.randint(0, len(status) - 1)]))


@bot.command(aliases=['criar'], pass_context=True)
@has_permissions(manage_roles = True)
async def create(ctx, *, args: str):

    guild = ctx.guild
    author = ctx.author
    msg = ctx.message

    result = await guild.create_role(name=args)
    await ctx.send("Cargo <@&{0.id}> criado no servidor {0.guild}.".format(result))

@create.error
async def create_error(ctx, error):
    
    if isinstance(error, commands.CheckFailure):
        await ctx.send("**Erro:** Você não pode criar um cargo!")
    else:
        await ctx.send(error)


@bot.command(aliases=['cor', 'setcolor'], pass_context=True)
@has_permissions(manage_roles = True)
async def color(ctx, role: discord.Role, *, args: str):

    print(role.name)
    print(role.permissions)
   
    if is_bgcolor(args):

        args = args.lstrip('#')
        args = tuple(int(args[i:i+2], 16) for i in (0, 2, 4))
        
        rgb = args[0];
        rgb = (rgb << 8) + args[1];
        rgb = (rgb << 8) + args[2];
        
        await role.edit(colour=discord.Colour(rgb))
        await ctx.send("Cor do cargo <@&{0.id}> foi atualizada!".format(role))
    else:
        await ctx.send("**Erro:** Código inválido!")

    return None

@color.error
async def color_error(ctx, error):
    
    if isinstance(error, commands.CheckFailure):
        await ctx.send("**Erro:** Você não pode alterar um cargo!")
    else:
        await ctx.send(error)


def parse_bgcolor(bgcolor):
    if not bgcolor.startswith('#'):
        raise ValueError('A bgcolor must start with a "#"')
    return binascii.unhexlify(bgcolor[1:])

def is_bgcolor(bgcolor):
    try:
        parse_bgcolor(bgcolor)
    except Exception as e:
        return False
    else:
        return True


# TODO - deixar aquela caixa bonita lá

@bot.command(aliases=['lista', 'roles'], pass_context=True)
async def rolelist(ctx):

        
    bot_member = ctx.guild.get_member(bot.user.id)

    highest_bot_role = bot_member.roles[-1]

    lst = "**Lista de Cargos:**\n"

    for r in ctx.guild.roles:
        #list += "<@&{0.id}>".format(r) + "\n"

        print(ctx.author.guild_permissions())

        lst += ("<@&{0.id}>\n".format(r) if r.name != "@everyone" and r < highest_bot_role and not r.is_bot_managed() else "")
    

    await ctx.send(lst)

@bot.command(aliases=['canRead', 'read', 'ler'], pass_context=True)
async def canread(ctx, role: discord.Role, canRead: bool):
    category = ctx.channel.category

    if category != None:
        await category.set_permissions(role, view_channel = canRead)
        print("Foi!")


bot.run("ODY0NTU5MjM5MTg3NTI5NzQ5.YO3NiQ.maahbMxUj_p5Yyga8eXA3H9O_uY")