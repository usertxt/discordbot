from discord.ext import commands
import discord
import asyncio
import requests
import logging


class Dictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = 'https://www.urbandictionary.com/define.php?term='
        self.api_url = 'http://api.urbandictionary.com/v0/define?term='

    @commands.command(pass_context=True)
    async def urban(self, ctx):
        search_term = ctx.message.content[7:].replace(' ', '+')
        response = self.url + search_term
        await ctx.send(response)
        logging.info(f'[Dictionary Prompted]: {ctx.message.author}: {ctx.message.content[7:]}')
        logging.info(f'[Dictionary Returned]: {response}')

    @commands.command(pass_context=True)
    async def dict(self, ctx):
        search_term_url = ctx.message.content[6:].replace(' ', '+')
        search_term = ctx.message.content[6:]
        definition = requests.get(self.api_url + search_term_url).json()
        definition = definition['list'][0]['definition']
        logging.info(f'[Dictionary Prompted]: {ctx.message.author}: {search_term}')

        async with ctx.typing():
            await asyncio.sleep(1)
            try:
                e = discord.Embed()
                if len(definition) > 1024:
                    e.add_field(name=search_term, value=f'{definition[:1021]}...')
                elif len(definition) < 1024:
                    e.add_field(name=search_term, value=definition)
                e.set_thumbnail(url='https://d2gatte9o95jao.cloudfront.net/assets/apple-touch-icon-1734beeaa059fbc5587bddb3001a0963670c6de8767afb6c67d88d856b0c0dad.png')
                e.add_field(name='\u200b', value=self.url + search_term_url)

                await ctx.send(embed=e)
                await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
                logging.info(f'[Dictionary Returned]: Embed response for {self.api_url + search_term_url}')
            except IndexError:
                await ctx.send(f'No results for {search_term}')
                await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
                logging.info(f'[Dictionary Error]: No results for {search_term}')


def setup(bot):
    bot.add_cog(Dictionary(bot))
