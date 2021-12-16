from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
import json
from os import listdir
from os.path import isfile, join
import logging

bot = commands.Bot(command_prefix='$')
COGS_DIR = 'cogs'
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

@bot.event
async def on_ready():
    print('Bot is online')
    logging.info('Bot is online')

if __name__ == '__main__':
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    handler = logging.FileHandler('bot.log', 'a', 'utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s', '%m-%d-%Y %H:%M:%S'))
    root_logger.addHandler(handler)

    bot.config_path = 'config.json'
    bot.config = json.load(open(bot.config_path))
    token = bot.config["DISCORD"]["TOKEN"]

    for extension in [f.replace('.py', '') for f in listdir(COGS_DIR) if isfile(join(COGS_DIR, f))]:
        try:
            bot.load_extension(COGS_DIR + '.' + extension)
            logging.info(f'Loading extension: {extension}')

        except Exception as error:
            logging.info(f'Loading {extension} returned with error: [{error}]')

    bot.run(token)
