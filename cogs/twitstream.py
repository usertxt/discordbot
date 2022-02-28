from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from twitter import *
import asyncio
import logging
import random
import re
import json


class TwitStream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config["TWITSTREAM"]
        self.consumer_key = self.config["CONSUMER_KEY"]
        self.consumer_secret = self.config["CONSUMER_SECRET"]
        self.token_key = self.config["TOKEN_KEY"]
        self.token_secret = self.config["TOKEN_SECRET"]

        self.t = Twitter(auth=OAuth(self.token_key, self.token_secret, self.consumer_key, self.consumer_secret))

    guild_ids = json.load(open("config.json"))["DISCORD"]["GUILD_IDS"]

    async def twit(self, ctx, screen_name, count=None):
        if count is None:
            count = 1

        if count == "rand":
            count = random.randint(1, 149)

        if int(count) < 150:
            num = int(count) - 1
            data = self.t.statuses.user_timeline(screen_name=screen_name, count=count, tweet_mode="extended")
            twit_id = data[num]['id']
            corrected_screen_name = data[num]['user']['screen_name']

            if 'retweeted_status' in data[num]:
                rt_screen_name = data[num]['retweeted_status']['user']['screen_name']
                twit_id = data[num]['retweeted_status']['id']
                await ctx.send(f'{corrected_screen_name} retweeted: https://twitter.com/{rt_screen_name}/status/{twit_id}')
                logging.info(f'[TwitStream Returned]: {corrected_screen_name} retweeted: https://twitter.com/{rt_screen_name}/status/{twit_id}')
            else:
                await ctx.send(f'https://twitter.com/{corrected_screen_name}/status/{twit_id}')
                logging.info(f'[TwitStream Returned]: https://twitter.com/{corrected_screen_name}/status/{twit_id}')
            

            while data[num]['full_text'].endswith('...'):
                num -= 1
                twit_id = data[num]['id']
                await ctx.send(f'https://twitter.com/{corrected_screen_name}/status/{twit_id}')
                logging.info(f'[TwitStream Returned]: https://twitter.com/{corrected_screen_name}/status/{twit_id}')

            if "https://t.co" in data[num]['full_text'] and data[num]['entities'].get('media') is None:
                url = re.search("(?P<url>https?://[^\s]+)", data[num]['full_text']).group("url")
                await asyncio.sleep(3)
                await ctx.send(url)
        else:
            await ctx.send('[TwitStream Error]: Too many tweets requested')

    @cog_ext.cog_slash(name="twit", description="Get tweets by Twitter username", guild_ids=guild_ids)
    async def slash_twit(self, ctx: SlashContext, screen_name, count=None):
        await self.twit(ctx, screen_name, count)

    @commands.command(name="twit", pass_context=True, brief="Get tweets by Twitter username")
    async def command_twit(self, ctx, screen_name, count=None):
        await self.twit(ctx, screen_name, count)


def setup(bot):
    bot.add_cog(TwitStream(bot))
