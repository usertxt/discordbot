from discord.ext import commands
import json
from os import listdir
from os.path import isfile, join

bot = commands.Bot(command_prefix='!')
COGS_DIR = 'cogs'


@bot.event
async def on_ready():
    print('Bot is online')

if __name__ == '__main__':
    bot.configpath = 'config.json'
    bot.config = json.load(open(bot.configpath))
    token = bot.config["DISCORD"]["TOKEN"]

    for extension in [f.replace('.py', '') for f in listdir(COGS_DIR) if isfile(join(COGS_DIR, f))]:
        try:
            bot.load_extension(COGS_DIR + '.' + extension)
            print(f'Loading extension: {extension}')

        except Exception as error:
            print(f'Loading {extension} returned with error: [{error}]')

    bot.run(token)
