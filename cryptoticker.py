from discord.ext import commands
import requests
import configparser

configfile = 'config.ini'
config = configparser.ConfigParser()
config.read(configfile)
default_fiat = config.get('user', 'default_fiat')
url = config.get('app', 'url')

module = ['cryptoticker']


class CryptoTicker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def setfiat(self, ctx, newfiat):
        for cryptoticker in module:
            try:
                config['user']['default_fiat'] = newfiat
                with open(configfile, 'w+') as updatedconfigfile:
                    config.write(updatedconfigfile)

                self.bot.unload_extension(cryptoticker)
                self.bot.load_extension(cryptoticker)

                await ctx.send('Changing default fiat currency to ' + newfiat.upper())
                print('[Reloading CryptoTicker Plugin] Config update: default_fiat is now ' + newfiat.upper())

            except Exception as error:
                await ctx.send(f'setfiat command returned an error: {error}')
                print(f'setfiat command returned with error: {error}')

    @commands.command(pass_context=True)
    async def price(self, ctx, ticker, fiat: str = default_fiat):
        try:
            response = requests.get(url + ticker + '&vs_currency=' + fiat)
            fetched = response.json()
            symbol = fetched[0]['symbol']
            current_price = fetched[0]['current_price']
            formatted_price = '{0:,.4f}'.format(current_price)
            await ctx.send(symbol.upper() + '/' + fiat.upper() + ': $' + str(formatted_price))

        except Exception as error:
            await ctx.send(f'Unknown currency or error: {error}')
            print(f'price command returned with error: {error}')


def setup(bot):
    bot.add_cog(CryptoTicker(bot))
