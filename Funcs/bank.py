import os
import json

path = os.getcwd() + "\\bank.json"


def game_totals(bet, outcome):
    totals = ["__**Результаты игры**__"]
    bots_income = 0
    for player_n in outcome.keys():
        sum = int(bet) * outcome[player_n]
        bots_income += -sum
        totals.append(f"Господин {player_n}: {sum}")
    totals.append(f"Господин Деффиченто: {bots_income}")
    return f"\n".join(totals)


async def change_balance(bet, outcome):
    bot_income = 0
    bank = await deserialize()
    for player in bank.keys():
        if player in outcome.keys():
            sum = int(bet) * outcome[player]
            bot_income += -sum
            bank[player] += sum
            bank["DeffichentoBOT"] += bot_income
    await serialize(bank)


async def serialize(data):
    with open(path, "w") as write_file:
        json.dump(data, write_file)


async def deserialize():
    with open(path, "r") as read_file:
        data = json.load(read_file)
    return data


async def on_start_refresh(mem_list):
    cur_bank = await deserialize()
    for member in mem_list:
        if member not in cur_bank:
            cur_bank[member] = 10000
        else:
            pass
    await serialize(cur_bank)


async def get_rem_bal(name):
    bank = await deserialize()
    if name == "*":
        return bank
    else:
        return bank[name]
