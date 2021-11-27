import discord
from discord.ext import commands
import asyncio
from discord_components import DiscordComponents, Button
from Funcs.Timer import Timer
from Funcs.vars import delay
from Funcs.bank import get_rem_bal, change_balance

players = []


async def mm(bot, ctx, bet):
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
            await msg.edit(content=f"Время вышло! Игра начата!\n"
                                   f"Сегодня играют: {', '.join(players)}", components=[])

    timer = Timer(delay, callback)

    @bot.event
    async def on_button_click(interaction):
        if interaction.custom_id == "btnMe":
            player_n = interaction.author.name
            p_bal = await get_rem_bal(player_n)
            if player_n not in players:
                if bet < p_bal:
                    players.append(player_n)
                    await change_balance(bet, outcome={player_n: -1})
                    await interaction.respond(content=f"Вы в игре!")
                else:
                    await interaction.respond(content=f"На вашем счету недостаточно средств для игры!")
            else:
                await interaction.respond(content="Вы уже в игре!")
        else:
            pass
    return players


def get_mem_list(bot):
    mem_list = []
    for guild in bot.guilds:
        for member in guild.members:
            mem_list.append(member.name)
    out = list(set(mem_list))
    out.sort()
    return out
