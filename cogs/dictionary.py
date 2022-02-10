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
        logging.info(f'[Dictionary Prompted]: {ctx.author} {search_term}')
        logging.info(f'[Dictionary Returned]: {response}')

    async def urban(self, ctx, search_term, slash_check=False):
        logging.info(f'[Urban Dictionary Prompted]: {ctx.author}: {search_term}')
        try:
            search_term_url = search_term.replace(' ', '+')
            definition = requests.get(self.api_url + search_term_url).json()
            definition = definition['list'][0]['definition']
            urban_icon = 'https://d2gatte9o95jao.cloudfront.net/assets/apple-touch-icon-1734beeaa059fbc5587bddb3001a0963670c6de8767afb6c67d88d856b0c0dad.png'

            e = discord.Embed(color=0xFFA500)
            e.set_author(name='\u200b', icon_url=urban_icon)
            if len(definition) > 1024:
                e.add_field(name=search_term, value=f'{definition[:1021].replace("[", "").replace("]","")}...')
            elif len(definition) < 1024:
                e.add_field(name=search_term, value=definition.replace("[", "").replace("]",""))
            e.add_field(name='\u200b', value=self.urban_url + search_term_url, inline=False)

            await ctx.send(embed=e)
            logging.info(f'[Urban Dictionary Returned]: Embed response for {self.api_url + search_term_url}')
        except IndexError:
            if slash_check:
                await ctx.send(f'No results for "{search_term}"', hidden=True)
            else:
                await ctx.send(f'No results for "{search_term}"')
            logging.info(f'[Urban Dictionary Error]: No results for {search_term}')

    @cog_ext.cog_slash(name="dict", description="Definitions from Merriam-Webster", guild_ids=guild_ids)
    async def slash_dict(self, ctx: SlashContext, search_term):
        await self.dict(ctx, search_term)

    @commands.command(name="dict", pass_context=True, brief="Definitions from Merriam-Webster")
    async def command_dict(self, ctx, search_term):
        await self.dict(ctx, search_term)

    @cog_ext.cog_slash(name="urban", description="Definitions from Urban Dictionary", guild_ids=guild_ids)
    async def slash_urban(self, ctx: SlashContext, search_term):
        await self.urban(ctx, search_term, slash_check=True)

    @commands.command(name="urban", pass_context=True, brief="Definitions from Urban Dictionary",
    description="Use quotes when searching for a phrase using the prefix command - Example: !urban \"search phrase\"")
    async def command_urban(self, ctx, search_term):
        await self.urban(ctx, search_term)


def setup(bot):
    bot.add_cog(Dictionary(bot))
