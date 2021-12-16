from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.client import SlashCommand
from twitter import *
import asyncio
import logging
import random
import re


class TwitStream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config["TWITSTREAM"]
        self.consumer_key = self.config["CONSUMER_KEY"]
        self.consumer_secret = self.config["CONSUMER_SECRET"]
        self.token_key = self.config["TOKEN_KEY"]
        self.token_secret = self.config["TOKEN_SECRET"]

        self.t = Twitter(auth=OAuth(self.token_key, self.token_secret, self.consumer_key, self.consumer_secret))

    @cog_ext.cog_slash(name="twit")
    async def _twit(self, ctx: SlashContext, screen_name, count=None):
        if count is None:
            count = 1

        if count == "rand":
            count = random.randint(0, 50)

        if int(count) > 150:
            await ctx.send('[TwitStream Error]: Too many tweets requested')
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
        else:
            num = int(count) - 1
            data = self.t.statuses.user_timeline(screen_name=screen_name, count=count, tweet_mode="extended")
            twit_id = data[num]['id']

            await ctx.send(f'https://twitter.com/{screen_name}/status/{twit_id}')
            logging.info(f'[TwitStream Returned]: https://twitter.com/{screen_name}/status/{twit_id}')

            while data[num]['full_text'].endswith('...'):
                num -= 1
                twit_id = data[num]['id']
                await ctx.send(f'https://twitter.com/{screen_name}/status/{twit_id}')
                logging.info(f'[TwitStream Returned]: https://twitter.com/{screen_name}/status/{twit_id}')

            if "https://t.co" in data[num]['full_text'] and data[num]['entities'].get('media') is None:
                url = re.search("(?P<url>https?://[^\s]+)", data[num]['full_text']).group("url")
                await asyncio.sleep(3)
                await ctx.send(url)

    @commands.command(pass_context=True)
    async def twit(self, ctx, screen_name, count=None):
        logging.info(f'[TwitStream Prompted]: {ctx.message.author}: twit {screen_name} {count}')
        if count is None:
            count = 1

        if count == "rand":
            count = random.randint(0, 50)
            logging.info(count)

        if int(count) > 150:
            async with ctx.typing():
                await asyncio.sleep(1)
                await ctx.send('[TwitStream Error]: Too many tweets requested')
                await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
        else:
            num = int(count) - 1
            data = self.t.statuses.user_timeline(screen_name=screen_name, count=count, tweet_mode="extended")
            twit_id = data[num]['id']

            async with ctx.typing():
                await asyncio.sleep(1)
                await ctx.send(f'https://twitter.com/{screen_name}/status/{twit_id}')
                logging.info(f'[TwitStream Returned]: https://twitter.com/{screen_name}/status/{twit_id}')
                await ctx.message.add_reaction('\N{THUMBS UP SIGN}')

            while data[num]['full_text'].endswith('...'):
                num -= 1
                twit_id = data[num]['id']

                async with ctx.typing():
                    await asyncio.sleep(3)
                    await ctx.send(f'https://twitter.com/{screen_name}/status/{twit_id}')
                    logging.info(f'[TwitStream Returned]: https://twitter.com/{screen_name}/status/{twit_id}')

            if "https://t.co" in data[num]['full_text'] and data[num]['entities'].get('media') is None:
                url = re.search("(?P<url>https?://[^\s]+)", data[num]['full_text']).group("url")
                async with ctx.typing():
                    await asyncio.sleep(3)
                    await ctx.send(url)


def setup(bot):
    bot.add_cog(TwitStream(bot))
