from discord.ext import commands
import requests
import asyncio
import logging


class StockTicker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config["STOCKTICKER"]
        self.key = self.config["API_KEY"]
        self.url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='

    @commands.command(pass_context=True)
    async def ticker(self, ctx, stock_ticker):
        response = requests.get(self.url + stock_ticker + '&apikey=' + self.key).json()
        logging.info(f'[StockTicker Prompted]: {ctx.message.author}: {stock_ticker}')
        try:
            async with ctx.typing():
                await asyncio.sleep(1)
                await ctx.send(f"{stock_ticker.upper()}: ${response['Global Quote']['05. price']}")
                logging.info(f"[StockTicker Returned]: {stock_ticker.upper()}: ${response['Global Quote']['05. price']}")
                await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
        except Exception:
            async with ctx.typing():
                await asyncio.sleep(1)
                await ctx.send(f'Ticker not found')
                logging.info('[StockTicker Error]: Ticker not found')
                await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')


def setup(bot):
    bot.add_cog(StockTicker(bot))
