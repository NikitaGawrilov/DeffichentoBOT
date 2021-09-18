import discord
from discord.ext import commands
from config import settings
#import blackjack
from countdown import cd

bot = commands.Bot(command_prefix=settings['prefix'])

players = []


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
    @bot.event
    async def on_message(msg):
        if msg.content.lower() == "где заряжали?":
            await msg.channel.send('В киоске!')
            speak()
        elif msg.content.lower() == "ругайся":
            await msg.channel.send("Ай фак ё булшит!")
            speak()
        elif msg.content.lower() == "/q":
            pass


@bot.command()
async def bj(ctx):
    players.append(ctx.author.id)
    await ctx.send(str(players))


@bot.command()
async def countdown(ctx):
    while 


bot.run(settings['token'])