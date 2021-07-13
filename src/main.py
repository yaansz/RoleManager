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

@bot.event
async def on_guild_channel_update(before, after):
    # Mudou de categoria
    if before.category.name != after.category.name:
        print(f"Canal '{after.name}' mudou de '{before.category.name}' para {after.category.name}")
    
        # TODO - Memória para o Boninho My Friend
        ids = [851546649599279124, 864639672177262592]
        
        guild = after.guild

        role_name = before.category.name + " - " + before.name

        # Categoria que devo deletar o cargo
        if after.category.id in ids:

            print("ID encontrado")

            for r in guild.roles:
                if r.name == role_name:
                    await r.delete()
                    await after.send(f"O cargo {role_name} foi deletado!")
                    return


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


@bot.command(aliases=['deletar'], pass_context=True)
@has_permissions(manage_roles = True)
async def delete(ctx, role: discord.Role):

    await role.delete()
    await ctx.send("Cargo apagado do servidor!")

@delete.error
async def delete_error(ctx, error):
    
    if isinstance(error, commands.CheckFailure):
        await ctx.send("**Erro:** Você não pode deletar um cargo!")
    else:
        await ctx.send(error)


@bot.command(aliases=['linked'], pass_context=True)
@has_permissions(manage_roles = True, manage_channels = True)
async def linked_role(ctx, type: str = "channel"):

    guild = ctx.guild
    author = ctx.author
    msg = ctx.message
    
    if type.lower() == "channel":
        option = msg.channel.category.name + " - " + msg.channel.name
    elif type.lower() == "category":
        option = msg.channel.category.name
    else:
        raise ValueError("")

    for r in guild.roles:
        if r.name == option:
            await ctx.send("Cargo <@&{0.id}> já existe!".format(r))
            return

    new_role = await guild.create_role(name=option)
    await ctx.send("Cargo <@&{0.id}> criado.".format(new_role))


@linked_role.error
async def create_error(ctx, error):
    
    if isinstance(error, commands.CheckFailure):
        await ctx.send("**Erro:** Você não pode criar um cargo!")
    elif isinstance(error, ValueError):
        await ctx.send("**Erro:** Opção inválida! Tente Channel ou Category")
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


@bot.command(aliases=['pegar'], pass_context=True)
async def get(ctx, role: discord.Role):
    
    await ctx.author.add_roles(role)
    return None
    

@bot.command(aliases=['remover'], pass_context=True)
async def remove(ctx, role: discord.Role):
    
    await ctx.author.remove_roles(role)
    return None
    

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
@has_permissions(manage_roles = True, manage_channels = True)
async def canread(ctx, role: discord.Role, canRead: bool, channel: bool):
    category = ctx.channel.category

    if category != None:
        await category.set_permissions(role, view_channel = canRead)
        print("Foi!")

@canread.error
async def canread_error(ctx, error):
    
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send('**Erro:** Formato inválido.\nDigite ".canread <cargo> <bool: pode> <bool: é canal>"')

bot.run("ODY0NTU5MjM5MTg3NTI5NzQ5.YO3NiQ.maahbMxUj_p5Yyga8eXA3H9O_uY")