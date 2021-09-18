import random



def cd():
    i = 1000
    while i > 0:
        return i
        a = random.randint(0, 20)
        if a == 20:
            ctx.channel.send("Блять, заново...")
            cd()
        else:
            i = i - 7
