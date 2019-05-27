from discord.ext import commands
import json
from os import listdir
from os.path import isfile, join
import logging

bot = commands.Bot(command_prefix='!')
COGS_DIR = 'cogs'
admin_id = 1234  # Replace 1234 with your unique discord id from ctx.message.author.id - Used for log clearing


@bot.event
async def on_ready():
    print('Bot is online')


@bot.command()
async def clearlog(ctx):
    if ctx.message.author.id == admin_id:
        with open('bot.log', 'w'):
            pass
        await ctx.send('Clearing log file')
        logging.info(f'Log file cleared by {ctx.message.author}[{ctx.message.author.id}]')
    else:
        await ctx.send('You are not authorized to clear the log file')
        logging.info(f'Attempted log file clear by {ctx.message.author}[{ctx.message.author.id}]')


if __name__ == '__main__':
    logging.basicConfig(filename='bot.log', format=f'%(asctime)s:%(levelname)s:%(message)s', datefmt='%m-%d-%Y %H:%M:%S', level=logging.INFO)
    bot.configpath = 'config.json'
    bot.config = json.load(open(bot.configpath))
    token = bot.config["DISCORD"]["TOKEN"]

    for extension in [f.replace('.py', '') for f in listdir(COGS_DIR) if isfile(join(COGS_DIR, f))]:
        try:
            bot.load_extension(COGS_DIR + '.' + extension)
            logging.info(f'Loading extension: {extension}')

        except Exception as error:
            logging.info(f'Loading {extension} returned with error: [{error}]')

    bot.run(token)
