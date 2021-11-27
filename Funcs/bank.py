import os
import json

bank_path = os.getcwd() + "\\Funcs\\bank.json"


def game_totals(bet, outcome):
    totals = ["__**Результаты игры**__"]
    bots_income = int(bet) * len(outcome.keys())
    for player_n in outcome.keys():
        if outcome[player_n] == 0:
            totals.append(f"Господин {player_n}: {-(int(bet))}")
        else:
            sum = int(bet) * outcome[player_n]
            bots_income -= sum
            totals.append(f"Господин {player_n}: {sum}")
    totals.append(f"Господин Деффиченто: {bots_income}")
    return f"\n".join(totals)


async def change_balance(bet, outcome):
    bot_income = 0
    bank = await deserialize(bank_path)
    for player in bank.keys():
        if player in outcome.keys():
            sum = int(bet) * outcome[player]
            bot_income += -sum
            bank[player] += sum
            bank["DeffichentoBOT"] += bot_income
    await serialize(bank, bank_path)


async def serialize(data, path):
    with open(path, "w") as write_file:
        json.dump(data, write_file)


async def deserialize(path):
    with open(path, "r") as read_file:
        data = json.load(read_file)
    return data


async def on_start_refresh(mem_list):
    cur_bank = await deserialize(bank_path)
    for member in mem_list:
        if member not in cur_bank:
            cur_bank[member] = 10000
        else:
            pass
    await serialize(cur_bank, bank_path)


async def get_rem_bal(name):
    bank = await deserialize(bank_path)
    if name == "*":
        return bank
    else:
        return bank[name]
