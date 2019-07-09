# usertxt's Discord Bot
A Discord bot

Written in Python 3.7.3

## Installation

**Install required packages**

> Note: This app is written with the discord.py rewrite, some commands will not work on other versions. More information can be found here: https://discordpy.readthedocs.io/en/rewrite/migrating.html

```
 pip install -r requirements.txt
```


## Configure

Configure the app using **config.json**

Add your bot's token to:
```
"TOKEN": "YOUR_TOKEN"
```

Fiat is set to USD by default. Set your default fiat currency with:
```
"BASE_CURRENCY: "CURRENCY"
```
>Note: Use the lowercase three letter symbol for your BASE_CURRENCY currency or the API won't fetch the information properly.

## Cogs

### Admin
The admin cog includes functions that only you or someone you set as the admin will be able to invoke. You will
need to insert your unique Discord ID into the config under DISCORD > ADMIN_ID. Here are two ways to get your 
Discord ID:

1. In Discord, go to Settings > Appearance > Enable Developer Mode. Right click on your username in any channel
and select **Copy ID**.

2. Set up the bot as you would normally without adding your ID to the config. Run the bot and attempt to use the
**clearlog** command. By invoking the command, you have added an entry into the log with your information. The
 information will appear as **username#1234[YOUR_ID]**. Open the log and copy your ID into the bot's config.
 Rerun the bot.

### CryptoTicker
CryptoTicker uses CoinGecko's API to fetch cryptocurrency prices.

**Commands:**

In the Discord chat channel your bot has joined, use the following command to prompt the bot:
```
!price <ticker> [base_currency] 
```

**Examples:**

This command will return the price of Bitcoin vs the base currency you have chosen in your config:

```
!price btc
```
> Note: You are able to use the symbol or the full name of the currency. BTC or Bitcoin.

And this command will return the price of Bitcoin vs the Australian dollar:

```
!price btc aud
```

The basecurrency command allows you to use the bot to change your default base currency:

```
!basecurrency <currency>
```

**Example:**

```
!basecurrency aud
```

### StockTicker
StockTicker uses the Alpha Vantage API to fetch stock quotes. You will need you own API key to run this cog. Get yours for free at https://www.alphavantage.co/

**Usage:**
```
!quote <ticker>
```

### TwitStream
TwitStream fetches user's tweets and relays them to your Discord channel.

You will need your own Twitter Developer account  and your own keys for this cog to work. You can apply for a Twitter dev account here: https://developer.twitter.com/

**Commands:**

The following command will fetch a tweet from the user's timeline:

```
!twit <screen_name> [count]
```

>The optional count parameter will return the user's tweet based on the order the tweet is in their timeline. None or 1 is the most recent tweet, and 2 would be the user's second most recent tweet, etc.