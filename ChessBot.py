# bot.py
import os
import random

from discord.ext import commands
from dotenv import load_dotenv
from Chess import EmojiChess

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
ec = EmojiChess()


@bot.command(name='show', help='Show chess board')
async def show(ctx):
    await ctx.send(ec.emoji_string())


@bot.command(name='move', help='Performs a move')
async def roll(ctx, m):
    ec.move(m)
    await ctx.send(ec.turn)


@bot.command(name='reset', help='Resets the board')
async def reset(ctx):
    ec.reset()
    await ctx.send('Board Reset!')

bot.run(token)