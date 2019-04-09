import discord
from discord.ext import commands
import requests
import json

token = ''

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print('Bot is ready')

@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command(pass_context=True)
async def price(ctx, ticker):
    response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=' + ticker)
    price = response.json()
    symbol = price[0]['symbol']
    current_price = price[0]['current_price']
    formatted_price = '{0:,.4f}'.format(current_price)
    await ctx.send(symbol.upper() + '/USD: $' + str(formatted_price))

bot.run(token)
