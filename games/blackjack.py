from games.deck_stash import deck_vals, deck
from random import shuffle
import discord
from discord.ext import commands
import asyncio
from discord_components import DiscordComponents, Button
from Funcs.Timer import Timer

q_deck = deck.copy()
p_hands = {}
d_hand = []
ps_passed = []
delay = 10
outcome = {}


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
        if len(p_hands.keys()) == 0:
            await msg.edit(content="Никто не пришёл играть...", components=[])
        else:
            await msg.edit(content="Время вышло! Игра начата!", components=[])

    timer = Timer(delay, callback)

    @bot.event
    async def on_button_click(interaction):
        if interaction.custom_id == "btnMe":
            player_n = interaction.author.name
            if player_n not in p_hands:
                p_hands[player_n] = pop(2)
                await interaction.respond(content=f"Вы в игре\n"
                                                  f"Ваши карты, господин {player_n}:\n"
                                                  f"{get_p_cards(player_n)}")

            else:
                await interaction.respond(content="Вы уже в игре!")
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
                timer.cancel()
                ps_passed.append(player)
                await msg.edit(content=f"Господин {player} пасовал...", components=[])
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


def q():
    a = str(input('Уходишь?\n'))
    if a == 'y':
        quit()
    elif a == 'n':
        global pas
        pas = False
        global q_deck
        q_deck = deck.copy()
        print(len(q_deck))
        blackjack()
    else:
        print('По русски скажи бля')
        q()


def get_p_cards(p_name):
    return f"|{'|'.join(p_hands[p_name])}| ({score(p_hands[p_name])})"


async def compare(bot, ctx):
    while len(ps_passed) != len(p_hands.keys()):
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


async def blackjack(bot, ctx):
    global p_hand, d_hand, q_deck
    q_deck = deck.copy()
    shuffle(q_deck)

    await ctx.send(f"-----------------------------------------------------------------------------\n"
                   f"Господин {ctx.author.name} начинает игру в блэк-джек!\n"
                   f"Колоды заряжены, карты на столе разложены не в том порядке...\n"
                )

    await mm(bot, ctx)
    await asyncio.sleep(delay + 1)
    if len(p_hands.keys()) != 0:
        d_hand = pop(2)
        await ctx.send(f"Диллер выкладывает свои карты: \n"
                       f"|{d_hand[0]}|?| ({deck_vals[d_hand[0]]})")
        await compare(bot, ctx)
        await dealer(ctx)
        await ctx.send(finale())
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


