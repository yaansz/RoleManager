import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure
import random
import copy
from typing import Union

import embed
from colors import *


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
    '''
    Function to monitor guild channels and delete a role linked to a channel if the channel was moved to trash
    '''
    # Mudou de categoria
    if before == None or after == None:
        return 

    if before.category.name != after.category.name:
        print(f"Canal '{after.name}' mudou de '{before.category.name}' para {after.category.name}")
    
        # TODO - Memória para o Boninho My Friend
        ids = [851546649599279124, 864639672177262592]
        
        guild = after.guild


        # Nome criado sempre que um chat é linkado a uma categoria!
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
    '''
    Function to update the bot status
    '''
    status = ['Muito ocupado', 'Não pertube', 'Jogando', 'Talvez?', 'Sim', 'Não', 'Boa Pergunta', 
    '😳', 'Aula do Braida boa d+ slk', '🍻', 'minha vida no lixo', 'One Piece', 'hum', 'dois', 'tres', 'cod 4',
    'Netflix', 'Disney+', 'HBO MAX', 'Cuphead', 'Undertale', 'guilty gear', 'no hard', 'prova de arq2',
    'segredo xiii', 'meia noite eu te conto', 'AAAAAAAAAAAAAAAAAA', 'dale', 'tudo mentira', 'deveras intelectus',
    'será?', 'mc poze nos anos 80', 'cringe 😡😔🤮', 'calma lá meu parceiro', 'a morte do romantismo',
    'rei do gado', 'boa noite meu consagrado']

    await bot.change_presence(activity=discord.Game(status[random.randint(0, len(status) - 1)]))


@bot.command(aliases=['criar'], pass_context=True)
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

    await msg.channel.send(embed=embedmsg)
    
    return


@create.error
async def create_error(ctx, error):
    
    await ctx.message.delete(delay=2)

    if isinstance(error, commands.CheckFailure):
        await ctx.send("**Erro:** Você não pode criar um cargo!")
    else:
        await ctx.send(error)


@bot.command(aliases=['deletar'], pass_context=True)
@has_permissions(manage_roles = True)
async def delete(ctx, role: discord.Role):

    await ctx.message.delete(delay=2)

    await role.delete()
    await ctx.send(f"**AVISO:** Cargo '{role.name}' apagado do servidor por <@{ctx.author.id}>!")

@delete.error
async def delete_error(ctx, error):
    
    await ctx.message.delete(delay=2)

    if isinstance(error, commands.CheckFailure):
        await ctx.send("**Erro:** Você não pode deletar um cargo!")
    else:
        await ctx.send(error)


@bot.command(aliases=['linked'], pass_context=True)
@has_permissions(manage_roles = True, manage_channels = True)
async def linked_role(ctx, type: str = "channel"):
    """
        This function creates a role linked to a channel or a category, it's very useful to ping everyone who is interested to an specific chat, like a discipline or a very interesting topic
    """

    await ctx.message.delete(delay=2)

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

            embedmsg = embed.createEmbed(title="CARGO JÁ EXISTE!", 
            description= f"O cargo <@&{r.id}> já está no servidor, não precisa criar de novo!🍻",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
                ("Como pegar?", f"Apenas digite .get <@&{r.id}> e ele será adicionado na sua conta", False)
            ],
            img="https://cdn.discordapp.com/emojis/814010519022600192.png?v=1")

            await msg.channel.send(embed=embedmsg)

            # Don't create again!
            return

    new_role = await guild.create_role(name=option, mentionable=True)

    embedmsg = embed.createEmbed(title="Novo Cargo!", 
        description= f"O cargo <@&{new_role.id}> foi criado por <@{author.id}>",
        color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
        fields=[
            ("Como pegar?", f"Apenas digite .get no chat do cargo ou .get <@&{new_role.id}> e ele será adicionado na sua conta", False)
        ],
        img="https://cdn.discordapp.com/emojis/859150737509580800.gif?v=1")

    await msg.channel.send(embed=embedmsg)


@linked_role.error
async def linked_role_error(ctx, error):
    
    await ctx.message.delete(delay=2)

    if isinstance(error, CheckFailure):
        await ctx.send("**Erro:** Você não pode criar um cargo!")
    elif isinstance(error, ValueError):
        await ctx.send("**Erro:** Opção inválida! Tente Channel ou Category")
    else:
        await ctx.send(error)


@bot.command(aliases=['cor', 'setcolor'], pass_context=True)
@has_permissions(manage_roles = True)
async def color(ctx, role: discord.Role, *, args: str):

    await ctx.message.delete(delay=2)
   
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

        await ctx.message.channel.send(embed=embedmsg)

    else:
        await ctx.send("**Erro:** Código inválido!")

    return None

@color.error
async def color_error(ctx, error):
    
    await ctx.message.delete(delay=2)

    if isinstance(error, commands.CheckFailure):
        await ctx.send("**Erro:** Você não pode alterar um cargo!")
    else:
        await ctx.send(error)


@bot.command(aliases=['pegar', 'add', 'add_roles'], pass_context=True)
async def get(ctx, role: Union[str, discord.Role] = "channel"):
    
    await ctx.message.delete(delay=2)
    
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
            description= f"Infelizmente, o cargo que você deseja criar não existe, pode tentar criar com o .linked ou .create",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
            ],
            img="https://cdn.discordapp.com/emojis/814603985842733107.png?v=1")

        await ctx.message.channel.send(embed=embedmsg)
            
    else:

        await ctx.author.add_roles(role)

        embedmsg = embed.createEmbed(title="Cargo Atualizado!", 
            description= f"O cargo <@&{role.id}> foi adicionado ao perfil <@{ctx.author.id}>",
            color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
            fields=[
                ("Como pegar?", f"Apenas digite .get no chat do cargo ou .get <@&{role.id}> e ele será adicionado na sua conta", False)
            ],
            img="https://cdn.discordapp.com/emojis/854557933421461514.gif?v=1")

        await ctx.message.channel.send(embed=embedmsg)

    return None

#@get.error
async def get_error(ctx, error):
    
    await ctx.message.delete(delay=2)

    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("**Erro:** Você não pode adicionar esse cargo!")
    else:
        await ctx.send(error)


@bot.command(aliases=['remover'], pass_context=True)
async def remove(ctx, role: discord.Role):
    
    await ctx.message.delete(delay=2)

    await ctx.author.remove_roles(role)

    embedmsg = embed.createEmbed(title="Cargo Atualizado!", 
        description= f"O cargo <@&{role.id}> foi removido do perfil <@{ctx.author.id}>",
        color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),

        img="https://cdn.discordapp.com/emojis/815618837109276684.png?v=1")

    await ctx.message.channel.send(embed=embedmsg)

    return None

@remove.error
async def remove_error(ctx, error):
    
    await ctx.message.delete(delay=2)

    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("**Erro:** Você não pode remover esse cargo!")
    else:
        await ctx.send(error)


# TODO - deixar aquela caixa bonita lá

@bot.command(aliases=['lista', 'roles'], pass_context=True)
async def rolelist(ctx):

    await ctx.message.delete(delay=2)
        
    bot_member = ctx.guild.get_member(bot.user.id)

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


# REWRITE THAT SHIT

@bot.command(aliases=['canRead', 'read', 'ler'], pass_context=True)
@has_permissions(manage_roles = True, manage_channels = True)
async def canread(ctx, role: discord.Role, canRead: bool, type: str = "channel"):
    
    await ctx.message.delete(delay=2)

    if type == "category":
        category = ctx.channel.category

        if category != None:
            await category.set_permissions(role, view_channel = canRead)
            await ctx.send("Permissão alterada!")
    elif type == "channel":

        await ctx.channel.set_permissions(role, view_channel = canRead)
        await ctx.send("Permissão alterada!")


@canread.error
async def canread_error(ctx, error):
    
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send('**Erro:** Formato inválido.\nDigite ".canread <cargo> <bool: pode> <bool: é canal>"')

@bot.command(aliases=['ajuda'], pass_context=True)
async def commands(ctx):
    
    lst = ""
    lst += "`.create <role name>` - Comando para criar um cargo.\n"
    lst += "`.delete <@ mention role>` - Comando para deletar um cargo.\n"
    lst += "`.linked <default:channel or category>` - Comando para criar um cargo vinculado a um canal ou categoria\n"
    lst += "`.color <@ mention role> <color code hex>` - Comando para mudar a cor de um cargo.\n" 
    lst += "`.get <@ mention role>` - Comando para pegar um cargo.\n"
    lst += "`.remove <@ mention role>` - Comando para remover um cargo.\n"
    lst += "`.rolelist` - Comando para listar os cargos disponíveis.\n"
    lst += "`.canread <@ mention role> <True/False>` - Comando para permitir ou não a leitura de um chat (TODO)\n"
    
    embedmsg = embed.createEmbed(title="Lista de Comandos!", 
        description= f"Veja todos os comandos disponíveis!",
        color=rgb_to_int((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
        fields=[
            ("Lista: ", lst, False),
            
            ],
        img="https://cdn.discordapp.com/emojis/812796371638812684.png?v=1")

    await ctx.message.channel.send(embed=embedmsg)

bot.run("ODY0NTU5MjM5MTg3NTI5NzQ5.YO3NiQ.maahbMxUj_p5Yyga8eXA3H9O_uY")