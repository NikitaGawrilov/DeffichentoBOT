from games.deck_stash import deck_vals, deck
from random import shuffle
import asyncio
from discord_components import DiscordComponents, Button
from Funcs.Timer import Timer
from Funcs.vars import delay
from Funcs.bank import game_totals, change_balance

q_deck = deck.copy()
p_hands = {}
d_hand = []
ps_passed = []
outcome = {}
kostyl = 1  # Да, именно он!


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
        global kostyl
        kostyl = 1
        await msg.edit(content="Время вышло!", components=[])
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
                    global kostyl
                    kostyl = 1
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
        ps_passed.append(player)

    timer = Timer(delay, callback)

    @bot.event
    async def on_button_click(interaction):
        player_n = interaction.author.name
        if player_n == player:
            global kostyl
            if interaction.custom_id == "btnHit":
                p_hands[player_n].extend(pop(1))
                await msg.edit(content=f"Господин {player_n} взял ещё одну карту...", components=[])
                await interaction.respond(content=f"Ваши карты, господин {player_n}:\n {get_p_cards(player_n)}")
                timer.cancel()
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
                    await ctx.send(f"У господина {player} блэк-джек!")
                    ps_passed.append(player)
                    if deck_vals[d_hand[0]] == 10:
                        await ctx.send(f"У диллера также есть вероятность блэк-джека, поэтому выигрыш господина {player} определится в конце партии...")
                    elif deck_vals[d_hand[0]] == 11:
                        await bj_outcome_choice(bot, ctx, player)
                        await asyncio.sleep(delay + 1)
                    else:
                        outcome[player] = 1.5
                elif score(p_hands[player]) > 21:
                    await ctx.send(f"У господина {player} перебор!")
                    ps_passed.append(player)
                    outcome[player] = -1
                elif score(p_hands[player]) < 21:
                    global kostyl
                    await hit(bot, ctx, player)
                    kostyl = 1
                    await asyncio.sleep(delay+1)
            else:
                pass
    return


async def bj_outcome_choice(bot, ctx, player):
    DiscordComponents(bot)
    buttons = [
        Button(label="Забрать выигрыш 1 к 1", custom_id="btnTake"),
        Button(label="Ждать до конца игры", custom_id="btnWait"),
    ]
    msg = await ctx.send(
        f"Господин {player}, у диллера также может быть блэк-джек.\n"
        f"Вы можете забрать сейчас выигрыш 1 к 1 или дождаться конца игры и получить выигрыш 3 к 2, "
        f"однако, если в конце игры у диллера также окажется блэк-джек, вы проиграете!\n"
        f"Что выбираете?",
        components=buttons
    )

    async def callback():
        await msg.edit(content=f"Господин {player}, время вышло! Судьба вашего выигрыша определится в конце игры...", components=[])

    timer = Timer(delay, callback)

    @bot.event
    async def on_button_click(interaction):
        player_n = interaction.author.name
        if player_n == player:
            if interaction.custom_id == "btnTake":
                await ctx.send(f"Господин {player} забирает выигрыш 1 к 1!")
                outcome[player] = 1
                timer.cancel()
            elif interaction.custom_id == "btnWait":
                await ctx.send(f"Господин {player} предпочёл дождаться конца игры...")
                timer.cancel()
            else:
                pass
        else:
            await interaction.respond(content=f"Эта кнопка не для вас, господин {player_n}")


def finale():
    global outcome
    for player in p_hands.keys():
        if player not in outcome.keys():
            p_points = score(p_hands[player])
            if score(d_hand) < 21:
                if p_points == 21:
                    outcome[player] = 1.5
                elif p_points > 21:
                    outcome[player] = -1
                elif p_points < 21:
                    if p_points > score(d_hand):
                        outcome[player] = 1.5
                    elif p_points <= score(d_hand):
                        outcome[player] = -1
            elif score(d_hand) == 21:
                if p_points == 21:
                    outcome[player] = 0.5
                else:
                    outcome[player] = -1
            elif score(d_hand) > 21:
                if p_points <= 21:
                    outcome[player] = 1.5
                else:
                    outcome[player] = -1


def pop(num=1):
    global kostyl
    if kostyl == 1:
        kostyl += 1
        pop_hand = []
        global q_deck
        if len(q_deck) < num:
            q_deck = deck.copy()
            for i in range(num):
                pop_hand.append(q_deck.pop())
        else:
            for i in range(num):
                pop_hand.append(q_deck.pop())
        return pop_hand
    else:
        pass

async def reload(ctx):
    global ps_passed, p_hands, d_hand, q_deck
    ps_passed.clear()
    p_hands.clear()
    d_hand.clear()
    q_deck.clear()
    outcome.clear()
    await ctx.send("-----------------------------------------------------------------------------")


async def blackjack(bot, ctx, players, bet):
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
        finale()
        await ctx.send(game_totals(bet, outcome))
        await change_balance(bet, outcome)
        await reload(ctx)
        return
    else:
        await reload(ctx)
        return


