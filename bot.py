import discord
from discord.ext import commands
from config import settings
from games.blackjack import blackjack
from random import randint
import asyncio
from Funcs.matchamaking import mm, get_mem_list
from Funcs.vars import delay
from Funcs.bank import on_start_refresh, get_rem_bal


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)
players = []
test_is_running = False
game_is_running = False


@bot.event
async def on_ready():
    channel = bot.get_channel(888728463501045782)
    await channel.send("Деффиченто на связи")
    await on_start_refresh(get_mem_list(bot))


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
async def bj(ctx, bet=100):
    global game_is_running
    if not game_is_running:
        game_is_running = not game_is_running
        await ctx.send(f"-----------------------------------------------------------------------------\n"
                       f"Господин {ctx.author.name} начинает игру в блэк-джек!\n"
                       )
        global players
        players = await mm(bot, ctx)
        await asyncio.sleep(delay + 1)
        await blackjack(bot, ctx, players, bet)
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


@bot.command()
async def cash(ctx):
    emb = discord.Embed(title=f"__**Баланс:**__", color=0xac0ceb, timestamp=ctx.message.created_at)
    if ctx.author.name == ctx.guild.owner.name:
        bal = await get_rem_bal("*")
        for mem in bal.keys():
            emb.add_field(name=f"**{mem}**", value=f"> {bal[mem]}")
    else:
        name = ctx.author.name
        bal = await get_rem_bal(name)
        emb.add_field(name=f"**{name}**", value=f"> {bal}")
    await ctx.send(embed=emb)

"""
@bot.command()
async def anons(ctx):
    if ctx.author.name == ctx.guild.owner.name:
        emb = discord.Embed(title="__**ВНИМАНИЕ!!!**__", color=0xebac0c, timestamp=ctx.message.created_at)
        emb.add_field(name="**ОФИЦИАЛЬНЫЙ РЕЛИЗ DeffichentoBOT v1.0**", value="*такт хз как версии называть, предлагайте предложения, задавайте ответы*")
        emb.add_field(name="**Функционал:**", value="> Сказать \"привет\" по пендосски\n"
                                                    "> Повторить сообщение\n"
                                                    "> Джо-Джо референс\n"
                                                    "> Ответить где заряжали колоды\n"
                                                    "> Поиграть в блэк-джек\n"
                                                    "> Узнать сколько у тебя денег",
                      inline=False)
        emb.set_image(url="https://media.giphy.com/media/U8MnmuVDpK264/giphy.gif")
        await ctx.send("@everyone", embed=emb)
"""

bot.run(settings['token'])
