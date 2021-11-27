import os
import asyncio
from random import randint
from Funcs.bank import serialize, deserialize, game_totals, change_balance
from discord_components import DiscordComponents, Button
from Funcs.Timer import Timer


mem_path = os.getcwd() + "\\Funcs\\mem.json"
p_list = []
delay = 0
outcome = {}


async def enter(bot, ctx, players):
    DiscordComponents(bot)
    em = bot.get_emoji(914145290251010081)
    buttons = [
        Button(emoji=em, custom_id="btnIn")
    ]
    msg = await ctx.send(
        "Заходите, господа игроки...",
        components=buttons
    )

    async def callback():
        if len(p_list) == 0:
            await msg.edit(content="Господа, вы - сыкуны! Я забираю ваши деньги!", components=[])
        else:
            losers = []
            for player in players:
                if player not in p_list:
                    losers.append(player)
            if losers:
                await msg.edit(content=f"Вход закрыт, господа {', '.join(losers)} опоздали и проиграли!", components=[])
            else:
                await msg.edit(content=f"Вход закрыт...", components=[])


    timer = Timer(delay, callback)

    @bot.event
    async def on_button_click(interaction):
        if interaction.custom_id == "btnIn":
            player_n = interaction.author.name
            if player_n in players:
                if player_n not in p_list:
                    p_list.append(player_n)
                    await interaction.respond(content=f"Пути назад нет...")
                else:
                    await interaction.respond(content="Вы уже зашли, ждите своей участи...")
            else:
                await interaction.respond(content="Вы не участвуете в данной партии!")
        else:
            pass


async def get_is_even():
    data = await deserialize(mem_path)
    return data["is_even"]


async def flick():
    data = await deserialize(mem_path)
    data["is_even"] = not data["is_even"]
    await serialize(data, mem_path)


def reload():
    global delay, p_list
    delay = 0
    p_list.clear()
    outcome.clear()


async def finale():
    global outcome
    for player in p_list:
        if await get_is_even():
            if (int(p_list.index(player)) + 1) % 2 == 0:
                outcome[player] = 2
            else:
                outcome[player] = 0
        else:
            if (int(p_list.index(player)) + 1) % 2 != 0:
                outcome[player] = 2
            else:
                outcome[player] = 0


async def andrew_game(bot, ctx, players, bet):
    await flick()
    global delay
    delay = randint(10, 30)
    await enter(bot, ctx, players)
    await asyncio.sleep(delay + 1)
    await finale()
    if outcome.keys():
        await ctx.send(game_totals(bet, outcome))
    else:
        await ctx.send(game_totals(bet, {pl: 0 for pl in players}))
    await change_balance(bet, outcome)
    reload()


