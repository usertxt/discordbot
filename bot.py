from discord.ext import commands
import configparser

configfile = 'config.ini'
config = configparser.ConfigParser()
config.read(configfile)
token = config.get('user', 'token')
url = config.get('app', 'url')

bot = commands.Bot(command_prefix='!')
extensions = ['cryptoticker']


@bot.event
async def on_ready():
    print('Bot is online')

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f'Loading extension {extension}')

        except Exception as error:
            print(f'{extension} cannot be loaded. [{error}]')

    bot.run(token)
