from deck_stash import deck_vals, deck
import random

q_deck = deck.copy()
p_hand = []
d_hand = []
pas = False


def score(arr):
    sc = 0
    for i in range(len(arr)):
        sc = sc + deck_vals[arr[i]]
    return sc


def hit():
    a = str(input('Ещё? \n'))
    if a == 'y':
        global p_hand
        p_hand.append(q_deck.pop())
        cards()
    elif a == 'n':
        print('Пас')
        global pas
        pas = True
    else:
        print('По русски скажи бля')
        hit()


def fin():
    global d_hand
    while score(d_hand) < 17:
        d_hand.append(q_deck.pop())
    cards()


def q():
    a = str(input('Уходишь?\n'))
    if a == 'y':
        quit()
    elif a == 'n':
        global pas
        pas = False
        global q_deck
        q_deck = deck.copy()
        #print(q_deck)
        print(len(q_deck))
        blackjack()
    else:
        print('По русски скажи бля')
        q()


def cards():
    print(f'Рука диллера: |{"|".join(d_hand)}| ({score(d_hand)})')
    print(f'Ваша рука: |{"|".join(p_hand)}| ({score(p_hand)})')


def compare():
    if score(p_hand) == 21 and score(d_hand) < 21:
        print('Вы выиграли!')
        q()
    elif score(p_hand) < 21 and score(d_hand) == 21:
        print('Вы проиграли...')
        q()
    elif score(p_hand) > 21 and score(d_hand) < 21:
        print('Вы проиграли...')
        q()
    elif score(p_hand) < 21 and score(d_hand) > 21:
        print('Вы выиграли!')
        q()
    else:
        pass


def play():
    compare()
    hit()


def blackjack():
    global p_hand, d_hand, q_deck
    q_deck = deck.copy()
    random.shuffle(q_deck)
    d_hand = [q_deck.pop(), q_deck.pop()]
    p_hand = [q_deck.pop(), q_deck.pop()]

    cards()
    if score(p_hand) == 21 and score(d_hand) == 21:
        print('Зато не проиграл!')
        q()
    else:
        while not pas:
            play()
        fin()
        compare()
        if score(p_hand) < 21 and score(d_hand) < 21:
            if score(p_hand) > score(d_hand):
                print('Вы выиграли!')
                q()
            elif score(p_hand) == score(d_hand):
                print('Зато не проиграл!')
                q()
            else:
                print('Вы проиграли...')
                q()


blackjack()

#print(deck)
