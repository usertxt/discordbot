# usertxt's Discord Bot
A Discord bot

Written in Python 3.7.2

## Installation

**Install required packages**

> Note: This app is written with the discord.py rewrite, some commands will not work on other versions. More information can be found here: https://discordpy.readthedocs.io/en/rewrite/migrating.html

```
 pip3 install -r requirements.txt
```


## Configure

Configure the app using **config.json**

Add your bot's token to:
```
"TOKEN": "YOUR_TOKEN"
```

Fiat is set to USD by default. Set your default fiat currency with:
```
"DEFAULT_FIAT": "CURRENCY"
```
>Note: Use the lowercase three letter symbol for your DEFAULT_FIAT currency or the API won't fetch the information properly.

## Cogs

### CryptoTicker
This extension uses CoinGecko's API to fetch cryptocurrency prices.

**Commands:**

In the Discord chat channel your bot has joined, use the following command to prompt the bot:
```
!price <currency> [fiat] 
```

**Examples:**

This command will return the price of Bitcoin vs the default currency you have chosen in your config:
> Note: You are able to use the symbol or the full name of the currency. BTC or Bitcoin.
```
!price btc
```

And this command will return the price of Bitcoin vs the Australian dollar:

```
!price btc aud
```

The setfiat command allows you to use the bot to change your default fiat currency:

```
!setfiat <fiat>
```

**Example:**

```
!setfiat aud
```
