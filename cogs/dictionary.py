from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import discord
import requests
import logging
import json


class Dictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.urban_url = 'https://www.urbandictionary.com/define.php?term='
        self.dict_url = 'https://www.merriam-webster.com/dictionary/'
        self.api_url = 'http://api.urbandictionary.com/v0/define?term='

    guild_ids = json.load(open("config.json"))["DISCORD"]["GUILD_IDS"]

    async def dict(self, ctx, search_term):
        search_term = search_term.replace(' ', '+')
        response = self.dict_url + search_term
        await ctx.send(response)
        logging.info(f'[Dictionary Prompted]: {search_term}')
        logging.info(f'[Dictionary Returned]: {response}')

    async def urban(self, ctx, search_term):
        search_term_url = search_term.replace(' ', '+')
        definition = requests.get(self.api_url + search_term_url).json()
        definition = definition['list'][0]['definition']
        logging.info(f'[Dictionary Prompted]: {search_term}')

        try:
            e = discord.Embed()
            if len(definition) > 1024:
                e.add_field(name=search_term, value=f'{definition[:1021]}...')
            elif len(definition) < 1024:
                e.add_field(name=search_term, value=definition)
            e.set_thumbnail(url='https://d2gatte9o95jao.cloudfront.net/assets/apple-touch-icon-1734beeaa059fbc5587bddb3001a0963670c6de8767afb6c67d88d856b0c0dad.png')
            e.add_field(name='\u200b', value=self.urban_url + search_term_url)

            await ctx.send(embed=e)
            logging.info(f'[Dictionary Returned]: Embed response for {self.api_url + search_term_url}')
        except IndexError:
            await ctx.send(f'No results for {search_term}')
            logging.info(f'[Dictionary Error]: No results for {search_term}')

    @cog_ext.cog_slash(name="dict", description="Definitions from Merriam-Webster", guild_ids=guild_ids)
    async def slash_dict(self, ctx: SlashContext, search_term):
        await self.dict(ctx, search_term)

    @commands.command(name="dict", pass_context=True)
    async def command_dict(self, ctx, search_term):
        await self.dict(ctx, search_term)

    @cog_ext.cog_slash(name="urban", description="Definitions from Urban Dictionary", guild_ids=guild_ids)
    async def slash_urban(self, ctx: SlashContext, search_term):
        await self.urban(ctx, search_term)

    @commands.command(name="urban", pass_context=True)
    async def command_urban(self, ctx, search_term):
        await self.urban(ctx, search_term)


def setup(bot):
    bot.add_cog(Dictionary(bot))
