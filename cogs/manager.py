import discord
from discord.ext import commands

import .utils.embed as embed

class Manager(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['criar'], pass_context=True)
    @has_permissions(manage_roles = True)
    async def create(ctx, *, args: str):
        """Create a new role with the given name
        """

        # Deleting the message in n seconds after it was sent
        await ctx.message.delete(delay=2)

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
        await msg.channel.send(embed=embedmsg, delete_after = time_to_delete)
        
        return

    @create.error
    async def create_error(ctx, error):
        
        await ctx.message.delete(delay=2)

        if isinstance(error, commands.CheckFailure):
            await ctx.send("**Erro:** Você não pode criar um cargo!")
        else:
            await ctx.send(error)

# Setup
def setup(client):
    client.add_cog(Manager(client))

