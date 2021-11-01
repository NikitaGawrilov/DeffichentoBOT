from games.deck_stash import deck_vals, deck
from random import shuffle
import discord
from discord.ext import commands
import asyncio
from discord_components import DiscordComponents, Button
from Funcs.Timer import Timer
from Funcs.vars import delay

q_deck = deck.copy()
p_hands = {}
d_hand = []
ps_passed = []
outcome = {}


async def mm(bot, ctx, players):
    DiscordComponents(bot)
    buttons = [
        Button(label="Взять карты", custom_id="btnPick")
    ]
    msg = await ctx.send(
        "Господа, возьмите свои карты!",
        components=buttons
    )

    async def callback():
        for player in players:
            if player not in p_hands.keys():
                await ctx.send(f"Господин {player} не взял свои карты и тем самым отказался от игры...")

    timer = Timer(delay, callback)

    @bot.event
    async def on_button_click(interaction):
        if interaction.custom_id == "btnPick":
            player_n = interaction.author.name
            if player_n in players:
                if player_n not in p_hands:
                    p_hands[player_n] = pop(2)
                    await interaction.respond(content=f"Ваши карты, господин {player_n}:\n"
                                                      f"{get_p_cards(player_n)}")
                else:
                    await interaction.respond(content="Вы уже взяли Ваши карты!")
            else:
                await interaction.respond(content="Вы не участвуете в данной партии!")
        else:
            pass




def score(arr):
    sc = 0
    for i in range(len(arr)):
        sc = sc + deck_vals[arr[i]]
    return sc


async def hit(bot, ctx, player):
    DiscordComponents(bot)
    buttons = [
        Button(label="Ещё!", custom_id="btnHit"),
        Button(label="Пас", custom_id="btnPas"),
    ]
    msg = await ctx.send(
        f"Ещё, господин {player}?",
        components=buttons
    )

    async def callback():
        await msg.edit(content=f"Господин {player}, время вышло, считаем, что Вы пасовали...", components=[])

    timer = Timer(delay, callback)

    @bot.event
    async def on_button_click(interaction):
        player_n = interaction.author.name
        if player_n == player:
            if interaction.custom_id == "btnHit":
                await msg.edit(content=f"Господин {player} взял ещё одну карту...", components=[])
                p_hands[player_n].extend(pop())
                timer.cancel()
                await interaction.respond(content=f"Ваши карты, господин {player}:\n"
                                                  f"{get_p_cards(player)}")
            elif interaction.custom_id == "btnPas":
                await msg.edit(content=f"Господин {player} пасовал...", components=[])
                ps_passed.append(player)
                timer.cancel()
                await interaction.respond(content=f"Ваши карты, господин {player}:\n"
                                                  f"{get_p_cards(player)}")
            else:
                pass
        else:
            await interaction.respond(content=f"Эта кнопка не для вас, господин {player_n}")


async def dealer(ctx):
    global d_hand
    while score(d_hand) < 17:
        d_hand.append(q_deck.pop())
    await ctx.send(f"Диллер добирает карты себе: \n"
                   f"|{'|'.join(d_hand)}| ({score(d_hand)})")



def get_p_cards(p_name):
    return f"|{'|'.join(p_hands[p_name])}| ({score(p_hands[p_name])})"


async def compare(bot, ctx):
    while len(ps_passed) < len(p_hands.keys()):
        for player in p_hands.keys():
            if player not in ps_passed:
                if score(p_hands[player]) == 21:
                    ps_passed.append(player)
                    await ctx.send(f"У господина {player} блэк-джек!")
                    # if deck_vals[d_hand[0]] == 10: блок для вариантов выбора выигрыша
                    #     pass
                    # elif deck_vals[d_hand[0]] == 11:
                    #     pass
                elif score(p_hands[player]) > 21:
                    await ctx.send(f"У господина {player} перебор!")
                    ps_passed.append(player)
                    outcome[player] = 0
                elif score(p_hands[player]) < 21:
                    await hit(bot, ctx, player)
                    await asyncio.sleep(delay+1)
            else:
                pass
    return

def finale():
    result = []
    for player in p_hands.keys():
        p_points = score(p_hands[player])
        win_str = f"Господин {player} выигрывает!"
        lose_str = f"Господин {player} проигрывает!"
        if score(d_hand) < 21:
            if p_points == 21:
                result.append(win_str)
            elif p_points > 21:
                result.append(lose_str)
            elif p_points < 21:
                if p_points > score(d_hand):
                    result.append(win_str)
                elif p_points <= score(d_hand):
                    result.append(lose_str)
        elif score(d_hand) == 21:
            if p_points == 21:
                result.append(win_str)
            else:
                result.append(lose_str)
        elif score(d_hand) > 21:
            if p_points <= 21:
                result.append(win_str)
            else:
                result.append(lose_str)
    return "\n".join(result)

def pop(num=1):
    pop_hand =[]
    global q_deck
    if len(q_deck) < num:
        q_deck = deck.copy()
        for i in range(num):
            pop_hand.append(q_deck.pop())
    else:
        for i in range(num):
            pop_hand.append(q_deck.pop())
    return pop_hand


async def blackjack(bot, ctx, players):
    global p_hand, d_hand, q_deck
    q_deck = deck.copy()
    shuffle(q_deck)
    await mm(bot, ctx, players)
    await asyncio.sleep(delay + 1)
    if len(p_hands.keys()) != 0:
        d_hand = pop(2)
        await ctx.send(f"Диллер выкладывает свои карты: \n"
                       f"|{d_hand[0]}|?| ({deck_vals[d_hand[0]]})")
        await compare(bot, ctx)
        await dealer(ctx)
        await ctx.send(finale())
        ps_passed.clear()
        p_hands.clear()
        d_hand.clear()
        return
    else:
        await ctx.send("-----------------------------------------------------------------------------")
        return
    # cards()
    #
    # if score(p_hand) == 21 and score(d_hand) == 21:
    #     print('Зато не проиграл!')
    #     q()
    # else:
    #     while not pas:
    #         play()
    #     fin()
    #     compare()
    #     if score(p_hand) < 21 and score(d_hand) < 21:
    #         if score(p_hand) > score(d_hand):
    #             print('Вы выиграли!')
    #             q()
    #         elif score(p_hand) == score(d_hand):
    #             print('Зато не проиграл!')
    #             q()
    #         else:
    #             print('Вы проиграли...')
    #             q()


