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
    if ec.move(m):
        pass
    else:
        await ctx.send('You made an invalid move! Please try again.')


@bot.command(name='reset', help='Resets the board')
async def reset(ctx):
    ec.reset()
    await ctx.send('Board Reset!')


@bot.command(name='turn', help='Says who\'s turn it currently is')
async def reset(ctx):
    if ec.turn is 'w':
        await ctx.send('It is white\'s turn to move.')
    else:
        await ctx.send('It is black\'s turn to move.')

bot.run(token)