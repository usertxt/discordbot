from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import requests
import logging
import json


class StockTicker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config["STOCKTICKER"]
        self.key = self.config["API_KEY"]
        self.url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='
    
    guild_ids = json.load(open("config.json"))["DISCORD"]["GUILD_IDS"]

    async def quote(self, ctx, ticker):
        response = requests.get(self.url + ticker + '&apikey=' + self.key).json()
        price = float(response['Global Quote']['05. price'])
        logging.info(f'[StockTicker Prompted]: {ctx.author}: {ticker}')
        try:
            await ctx.send(f"{ticker.upper()}: ${price:,.2f}")
            logging.info(f"[StockTicker Returned]: {ticker.upper()}: ${price:,.2f}")
        except Exception as e:
            await ctx.send(f'{e}')
            logging.info(f'[StockTicker Error]: {e}')

    @cog_ext.cog_slash(name="quote", description="Get stock quotes", guild_ids=guild_ids)
    async def slash_quote(self, ctx: SlashContext, ticker):
        await self.quote(ctx, ticker)

    @commands.command(name="quote", pass_context=True, brief="Get stock quotes")
    async def command_quote(self, ctx, ticker):
        await self.quote(ctx, ticker)


def setup(bot):
    bot.add_cog(StockTicker(bot))
