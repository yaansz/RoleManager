# Logging
import logging
import utils.logger as logger

# Discord
import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure
import random
import copy
from typing import Union
import json

# DB
from pymongo import MongoClient

# My things
import status.status as status
import utils.embed as embed
from utils.colors import *

import os

from dotenv import dotenv_values

class Bot(commands.Bot):

    def __init__(self):        
        self.log = logging.getLogger(__name__)
        

        self.db_client = MongoClient(ENV['MONGODB'])
        self.guild_preferences_db = self.db_client['role-manager']['guild-preferences']
        self.log.debug("Guild preferences database initialized")
        
        
        # BOT CONFIG
        # some shit to make it work
        intents = discord.Intents.default()
        intents.members = True
        # Super Constructor
        super().__init__(command_prefix = lambda cli, 
                        msg: self.guild_preferences_db.find_one({"_id": msg.guild.id})['prefix'], 
                        intents=intents)
        self.log.debug("Bot basic setup initialized")

        # Extensions
        with open(os.path.dirname(os.path.abspath(__file__))  + '/database/utils.json', 'r') as f:
            extensions = json.load(f)["INITIAL_EXTENSIONS"]
        self.log.debug("Identified Extensions")
        
        self.load_extensions(extensions)
        self.log.debug("All Identified extensions have been loaded")


    def load_extensions(self, extensions):
        for extension in extensions:
            try:
                self.load_extension(extension)
                self.log.debug('Success to load extension {}'.format(extension))
            except Exception as e:
                self.log.error('Error loading extensionFailed to load extension {}\n{}: {}'.format(
                    extension, type(e).__name__, e))


    async def on_ready(self):
        self.log.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
        self.update_status.start()
        self.log.debug("Success to start the bot status update")


    @tasks.loop(seconds=10)
    async def update_status(self):
        '''
        Function to update the bot status
        '''
        #await bot.change_presence(activity=discord.Game(status[random.randint(0, len(status) - 1)]))
        result = random.choice(list(status.Status))
        
        if result == status.Status.Playing:
            await bot.change_presence(activity=discord.Game(name=random.choice(result.value)))
        elif result == status.Status.Streaming:
            await bot.change_presence(activity=discord.Streaming(name=random.choice(result.value), url="https://www.twitch.tv/yaansz"))
        elif result == status.Status.Listening:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=random.choice(result.value)))
        elif result == status.Status.Watching:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(result.value)))
        else:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=random.choice(result.value)))

    async def on_command_error(self, ctx, error):
        print(error)



if __name__ == "__main__":
    ENV = dotenv_values(os.path.dirname(os.path.abspath(__file__)) + "/.env")
    # LOG
    logger.init_log()

    logging.getLogger("discord").setLevel(logging.WARNING)
    logging.debug("Removed Discord.py logs")
    
    bot = Bot()
    bot.run(ENV['DISCORD_RM_TOKEN'])
