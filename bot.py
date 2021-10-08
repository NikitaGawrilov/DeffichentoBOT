import discord
from discord.ext import commands
from config import settings
from games.blackjack import blackjack
from random import randint
import asyncio
from discord_components import DiscordComponents, Button
from Funcs.Timer import Timer

bot = commands.Bot(command_prefix=settings['prefix'])
players = []
test_is_running = False

@bot.command()
async def hi(ctx):
    await ctx.send("Hi!")


@bot.command(pass_context=True) #разрешаем передавать агрументы
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
        elif msg.content.lower() == "ругайся":
            await ctx.channel.send("Ай фак ё булшит!")
        elif msg.content.lower() == "/q":
            await ctx.send("Попиздели и хватит!")
            return


@bot.command()
async def bj(ctx):
    await blackjack(bot, ctx)



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
                await ctx.channel.send("Блять, заново...")
                i = int(arg)
            else:
                await ctx.channel.send(i)
                i = i - 7
        elif msg.content.lower() == '/q':
            await ctx.send('Харош')
            return
        else:
            pass

@bot.command()
async def test(ctx):
    r = ["gjgjgjg", "dsksdokfdsof", "fjsdfijsd"]
    await ctx.send("\n".join(r))



bot.run(settings['token'])