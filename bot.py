import discord
from discord.ext import commands
from config import settings
from games.blackjack import blackjack
from random import randint
import asyncio
from discord_components import DiscordComponents, Button
from Funcs.Timer import Timer
from Funcs import matchamaking
from Funcs.vars import delay

bot = commands.Bot(command_prefix=settings['prefix'])
players = []
test_is_running = False
game_is_running = False

@bot.command()
async def hi(ctx):
    await ctx.send("Hi!")


@bot.command()
async def povtor(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def jojo(ctx):
    url = 'https://i.ytimg.com/vi/rvd366w_EhU/maxresdefault.jpg'
    emb = discord.Embed(color=0xc43cd4, title = "あのディオのクソ口")
    emb.set_image(url=url)
    await ctx.send(embed=emb)

@bot.command()
async def speak(ctx):
    await ctx.send("Режим переговоров активирован")
    while True:
        msg = await bot.wait_for('message')
        if msg.content.lower() == "где заряжали?":
            await ctx.send('В киоске!')
            return


@bot.command()
async def bj(ctx):
    global game_is_running
    if not game_is_running:
        game_is_running = not game_is_running
        await ctx.send(f"-----------------------------------------------------------------------------\n"
                       f"Господин {ctx.author.name} начинает игру в блэк-джек!\n"
                       )
        global players
        players = await matchamaking.mm(bot, ctx)
        await asyncio.sleep(delay + 1)
        await blackjack(bot, ctx, players)
        game_is_running = not game_is_running
        players.clear()
    else:
        await ctx.send(f"Дождитесь завершения запущенной игры, господин {ctx.author.name}!")


@bot.command()
async def zxc(ctx, arg):
    i = int(arg)
    while i > 0:
        try:
            msg = await bot.wait_for('message', timeout=0.3)
        except asyncio.TimeoutError:
            msg = ''
        if msg == '':
            if randint(0, 20) == 20:
                await ctx.channel.send("Заново...")
                i = int(arg)
            else:
                await ctx.channel.send(i)
                i = i - 7
        elif msg.content.lower() == '/q':
            await ctx.send('Харош')
            return
        else:
            pass

# @bot.command()
# async def test(ctx):
#     r = ["gjgjgjg", "dsksdokfdsof", "fjsdfijsd"]
#     await ctx.send("\n".join(r))



bot.run(settings['token'])