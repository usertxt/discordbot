from discord.ext import commands
import requests
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
default_fiat = config.get("user", "default_fiat")
token = config.get("user", "token")
url = config.get("app", "url")
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Bot is online')


@bot.command(pass_context=True)
async def price(ctx, ticker, fiat: str = default_fiat):
    try:
        response = requests.get(url + ticker + '&vs_currency=' + fiat)
        fetched = response.json()
        symbol = fetched[0]['symbol']
        current_price = fetched[0]['current_price']
        formatted_price = '{0:,.4f}'.format(current_price)
        await ctx.send(symbol.upper() + '/' + fiat.upper() + ': $' + str(formatted_price))
    except (IndexError, KeyError):
        await ctx.send('Unknown currency')


bot.run(token)
