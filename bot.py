import discord
from discord.ext import commands
from config import settings
#import blackjack
from random import randint
import asyncio
from discord_components import DiscordComponents, Button

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
    if ctx.author.id not in players:
        players.append(ctx.author.id)
    #await ctx.send(str(players))
    #await ctx.send("")



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
    global test_is_running
    test_is_running = not test_is_running
    if test_is_running:
        DiscordComponents(bot)
        msg = await ctx.send(
            "Поймал?",
            components=[
                Button(label="Ага", custom_id="btnY"),
                Button(label="Неа", custom_id="btnN")
            ]
        )

        @bot.event
        async def on_button_click(interaction):
            if interaction.author.id == ctx.author.id:
                if interaction.custom_id == "btnY":
                    await interaction.respond(content="Чотк")
                    global test_is_running
                    test_is_running = False
                    await msg.edit(content="...", components=[])
                    return
                elif interaction.custom_id == "btnN":
                    await interaction.respond(content="Лох")
                    await msg.edit(content="...", components=[])
                    test_is_running = False
                    return
                else:
                    pass
            else:
                await interaction.respond(content="Это не тебе!")
    else:
        await ctx.send("Уже запущен")
        return

    # def check(interaction):
    #     return (interaction.custom_id == "btnY" or interaction.custom_id == "btnN") and interaction.author.id in players
    #
    # while True:
    #     interaction = await bot.wait_for("button_click", check=check)
    #     if interaction.author.id == ctx.author.id:
    #         if interaction.custom_id == "btnY":
    #             await interaction.respond(content="Чотк", type=1)
    #             interaction.responded = False
    #             return
    #         elif interaction.custom_id == "btnN":
    #             await interaction.respond(content="Лох")
    #             interaction.responded = False
    #             return
    #         else:
    #             pass
    #     else:
    #         await interaction.respond(content="Это не тебе!")
    #         interaction.responded = False

bot.run(settings['token'])