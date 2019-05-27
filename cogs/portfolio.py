from discord.ext import commands
import requests
import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = sql.create_engine('sqlite:///portfolio.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'positions'
    id = sql.Column(sql.Integer, sql.Sequence('user_id_seq'), primary_key=True)
    name = sql.Column(sql.String(50))
    discord_id = sql.Column(sql.String(50))
    coin = sql.Column(sql.String(50))
    symbol = sql.Column(sql.String(50))
    quantity = sql.Column(sql.String(50))
    price = sql.Column(sql.String(50))

    def __repr__(self):
        return "<User(id='%s', name='%s', discord_id='%s', coin='%s', symbol='%s', quantity='%s'," \
               " price='%s')>" % (self.id, self.name, self.discord_id, self.coin, self.symbol, self.quantity, self.price)


Base.metadata.create_all(engine)


class Portfolio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_ticker = self.bot.config["CRYPTOTICKER"]
        self.url = self.config_ticker["URL"]
        self.coin_list = requests.get(self.config_ticker["COIN_LIST"]).json()
        self.supported_currencies = requests.get(self.config_ticker["SUPPORTED_CURRENCIES"]).json()

    @commands.command(pass_context=True)
    async def p(self, ctx, action, ticker=None, quantity=None, price=None):
        global current_worth, total_price, current_price, coin_symbol
        if action == 'positions':
            disc_id = str(ctx.message.author.id)

            for coin in self.coin_list:
                if ticker == coin['symbol']:
                    ticker = coin['id']

            id_query = session.query(User.discord_id, User.coin, User.symbol, User.quantity, User.price). \
                filter(User.discord_id == disc_id).\
                all()
            coin_query = session.query(User.discord_id, User.coin, User.symbol, User.quantity, User.price). \
                filter(User.discord_id == disc_id). \
                filter(User.coin == ticker)
            result1 = [r.discord_id for r in id_query]
            result2 = [r.coin for r in coin_query]

            for coin in result2:
                response = requests.get(self.url + coin).json()
                coin_symbol = response[0]['symbol']
                current_price = response[0]['current_price']
                current_worth = [float(n.quantity) * current_price for n in coin_query]
                current_worth = sum(current_worth)
                total_price = [float(n.price) for n in coin_query]
                total_price = sum(total_price)

            response = '```fix\n'
            try:
                if disc_id in result1:
                    if ticker is None:
                        response += f'All positions for {ctx.message.author.name}\n'
                    else:
                        response += f'{ticker.upper()} positions for {ctx.message.author.name}\n'
                    response += 'SYM QTY PRICE\n'
                    if ticker is None:
                        for discord_id, coin, symbol, quantity, price in id_query:
                            response += f'{symbol.upper()} {quantity}   {price}\n'
                    elif ticker in result2:
                        for discord_id, coin, symbol, quantity, price in coin_query:
                            response += f'{symbol.upper()} {quantity}   {price}\n'
                else:
                    response += 'You have no positions'
            finally:
                if ticker in result2:
                    response += f'{coin_symbol.upper()}/USD: ${current_price:,.2f}\n'
                    if current_worth < total_price:
                        loss = total_price - current_worth
                        response += f'Total cost: {total_price:,.2f} Total worth: {current_worth:,.2f} Loss: {loss:,.2f}'
                    elif current_worth > total_price:
                        profit = current_worth - total_price
                        response += f'Total cost: {total_price:,.2f} Total worth: {current_worth:,.2f} Profit: {profit:,.2f}'
            response += '```'
            await ctx.send(response)

        elif action == 'add':
            if ticker is None:
                await ctx.send('Please supply a currency')
            elif ticker in str(self.coin_list):
                for coin in self.coin_list:
                    if ticker == coin['symbol']:
                        ticker = coin['id']
                        user = User(name=ctx.message.author.name, discord_id=ctx.message.author.id, coin=coin['id'],
                                    symbol=coin['symbol'],
                                    quantity=quantity, price=price)
                        print(f'adding {user} to database')
                        session.add(user)
                        session.commit()
                        session.close()
                        await ctx.send(f'Adding {ticker} {quantity} {price} for {ctx.message.author.name}')
            else:
                await ctx.send(f'Error: {ticker.upper()} is not a supported currency')

        elif action == 'remove':
            disc_id = str(ctx.message.author.id)
            if ticker == 'all':
                session.query(User).filter(User.discord_id == disc_id).delete()
                session.commit()
                await ctx.send(f'Removing all positions for {ctx.message.author.name}')
            for coin in self.coin_list:
                if ticker == coin['symbol']:
                    ticker = coin['id']
                    session.query(User). \
                        filter(User.name == str(ctx.message.author.name)). \
                        filter(User.discord_id == disc_id). \
                        filter(User.coin == coin['id']). \
                        filter(User.symbol == coin['symbol']). \
                        filter(User.quantity == quantity). \
                        filter(User.price == price). \
                        delete()
                    session.commit()
                    await ctx.send(f'Removing {ticker} {quantity} {price} for {ctx.message.author.name}')


def setup(bot):
    bot.add_cog(Portfolio(bot))
