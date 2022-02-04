from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import requests
import json
import logging

currency_symbol_dict = {'USD': '$', 'BTC': '₿', 'ETH': 'Ξ', 'LTC': 'Ł', 'EUR': '€', 'JPY': '¥', 'RUB': '₽',
                        'AED': 'د.إ', 'BDT': '৳', 'BHD': 'BD', 'CNY': '¥', 'CZK': 'Kč', 'DKK': 'kr.', 'GBP': '£',
                        'HUF': 'Ft', 'IDR': 'Rp', 'ILS': '₪', 'INR': '₹', 'KRW': '₩', 'KWD': 'KD', 'LKR': 'රු',
                        'MMK': 'K', 'MYR': 'RM', 'NOK': 'kr', 'PHP': '₱', 'PKR': 'Rs', 'PLN': 'zł', 'SAR': 'SR',
                        'SEK': 'kr', 'THB': '฿', 'TRY': '₺', 'VEF': 'Bs.', 'VND': '₫', 'ZAR': 'R', 'XDR': 'SDR',
                        'XAG': 'XAG', 'XAU': 'XAU'}


class CryptoTicker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config["CRYPTOTICKER"]
        self.base_currency = self.config["BASE_CURRENCY"]
        self.url = self.config["URL"]
        self.coin_list = requests.get(self.config["COIN_LIST"]).json()
        self.supported_currencies = requests.get(self.config["SUPPORTED_CURRENCIES"]).json()
        self.this_extension = 'cogs.cryptoticker'

    guild_ids = json.load(open("config.json"))["DISCORD"]["GUILD_IDS"]

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'new_base':
                await ctx.send(f'```BASE_CURRENCY: {self.base_currency}\n'
                               f'command usage: basecurrency <currency>```')
                logging.info(f'[CryptoTicker Prompted]: {ctx.message.author}: basecurrency')
                logging.info('[CryptoTicker Returned]: basecurrency usage message')

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'ticker':
                await ctx.send('```command usage: price <currency> [base_currency]```')
                logging.info(f'[CryptoTicker Prompted]: {ctx.message.author}: price')
                logging.info('[CryptoTicker Returned]: price usage message')

    async def basecurrency(self, ctx, new_base):
        logging.info(f'[CryptoTicker Prompted]: {ctx.author}: basecurrency {new_base}')

        new_base = new_base.lower()
        if new_base == self.base_currency:
            await ctx.send(f'Default base currency is already set to {new_base.upper()}')
            logging.info(f'[CryptoTicker Returned]: Default base currency is already set to {new_base.upper()}')
        elif new_base in self.supported_currencies:
            try:
                self.bot.config["CRYPTOTICKER"]["BASE_CURRENCY"] = new_base
                with open(self.bot.config_path, 'w') as updated_config:
                    json.dump(self.bot.config, updated_config, indent=2, sort_keys=False, ensure_ascii=True)

                self.bot.unload_extension(self.this_extension)
                self.bot.load_extension(self.this_extension)

                await ctx.send(f'Changing default base currency to {new_base.upper()}')
                logging.info(f'[CryptoTicker Reload]: Config update - BASE_CURRENCY is now {new_base.upper()}')

            except Exception as error:
                await ctx.send(f'basecurrency command returned with error: {error}')
                logging.info(f'[CryptoTicker Error]: basecurrency command returned with error: {error}')
        else:
            await ctx.send(f'CryptoTicker Error: {new_base.upper()} is not a supported currency')
            logging.info(f'[CryptoTicker Error]: {new_base.upper()} is not a supported currency')

    async def price(self, ctx, ticker, base=None):
        if base is None:
            base = self.base_currency

        logging.info(f'[CryptoTicker Prompted]: {ctx.author}: price {ticker} {base}')

        currency_symbol = currency_symbol_dict.get(base.upper(), '$')
        ticker = ticker.lower()
        base = base.lower()

        if base in self.supported_currencies:
            try:
                for coin in self.coin_list:
                    if ticker == coin['symbol']:
                        ticker = coin['id']

                response = requests.get(self.url + ticker + '&vs_currency=' + base).json()
                symbol = response[0]['symbol']
                current_price = response[0]['current_price']
                formatted_price = f'{current_price:,.2f}'
                if formatted_price.startswith('0'):
                    formatted_price = f'{current_price:,.4f}'
                if base == 'btc':
                    formatted_price = f'{current_price:,.8f}'

                await ctx.send(f'{symbol.upper()}/{base.upper()}: {currency_symbol}{formatted_price}')
                logging.info(f'[CryptoTicker Returned]: {symbol.upper()}/{base.upper()}:'
                                f' {currency_symbol}{formatted_price}')

            except Exception as error:
                await ctx.send(f'price command returned with error: {error}')
                logging.info(f'[CryptoTicker Error]: price command returned with error: {error}')
        else:
            await ctx.send(f'CryptoTicker Error: {base.upper()} is not a supported currency')
            logging.info(f'[CryptoTicker Error]: User: {ctx.author} Error: {base}'
                            f' is not a supported currency')

    @cog_ext.cog_slash(name="basecurrency", description="Change base currency", guild_ids=guild_ids)
    async def slash_basecurrency(self, ctx: SlashContext, new_base):
        await self.basecurrency(ctx, new_base)

    @commands.command(name="basecurrency", pass_context=True, brief="Change base currency")
    async def command_basecurrency(self, ctx, new_base):
        await self.basecurrency(ctx, new_base)

    @cog_ext.cog_slash(name="price", description="Check price of selected crypto", guild_ids=guild_ids)
    async def slash_price(self, ctx: SlashContext, ticker, base=None):
        await self.price(ctx, ticker, base)

    @commands.command(name="price", pass_context=True, brief="Check price of selected crypto")
    async def command_price(self, ctx, ticker, base=None):
        await self.price(ctx, ticker, base)


def setup(bot):
    bot.add_cog(CryptoTicker(bot))
