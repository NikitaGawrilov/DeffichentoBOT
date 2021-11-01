import discord
from discord.ext import commands
import asyncio
from discord_components import DiscordComponents, Button
from Funcs.Timer import Timer

players = []

async def mm(bot, ctx):
    DiscordComponents(bot)
    buttons = [
        Button(label="Я в деле!", custom_id="btnMe")
    ]
    msg = await ctx.send(
        "Кто участвует?",
        components=buttons
    )

    async def callback():
        if len(players) == 0:
            await msg.edit(content="Никто не пришёл играть...", components=[])
        else:
            await msg.edit(content="Время вышло! Игра начата!", components=[])

    timer = Timer(10, callback)

    @bot.event
    async def on_button_click(interaction):
        if interaction.custom_id == "btnMe":
            player_n = interaction.author.name
            if player_n not in players:
                players.append(player_n)
                await interaction.respond(content=f"Вы в игре!")
            else:
                await interaction.respond(content="Вы уже в игре!")
        else:
            pass
    return players