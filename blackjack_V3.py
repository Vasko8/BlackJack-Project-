import tkinter as tk
import random

# ======================
# VARIABLES
# ======================

solde = 1000
pari = 0

paquet = []
main_joueur = []
main_banque = []

partie_finie = False

# ======================
# FONCTIONS
# ======================

def creer_paquet():
    couleurs = ["♠", "♥", "♦", "♣"]
    valeurs = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]

    p = []
    for c in couleurs:
        for v in valeurs:
            p.append((v, c))

    random.shuffle(p)
    return p


def calcul_score(main):
    score = 0
    nb_as = 0

    for carte in main:
        v = carte[0]

        if v in ["J","Q","K"]:
            score += 10
        elif v == "A":
            score += 11
            nb_as += 1
        else:
            score += int(v)

    while score > 21 and nb_as > 0:
        score -= 10
        nb_as -= 1

    return score


# ======================
# INTERFACE
# ======================

fenetre = tk.Tk()
fenetre.title("Blackjack")

label_solde = tk.Label(fenetre, text="Solde : 1000 €")
label_solde.pack()

entry_pari = tk.Entry(fenetre)
entry_pari.pack()

label_joueur = tk.Label(fenetre, text="Score joueur : 0")
label_joueur.pack()

label_banque = tk.Label(fenetre, text="Score banque : ?")
label_banque.pack()

label_message = tk.Label(fenetre, text="")
label_message.pack()

# ======================
# JEU
# ======================

def commencer():
    global paquet, main_joueur, main_banque, pari, partie_finie

    try:
        pari = int(entry_pari.get())
    except:
        label_message.config(text="Pari invalide")
        return

    if pari <= 0 or pari > solde:
        label_message.config(text="Pari incorrect")
        return

    paquet = creer_paquet()

    main_joueur = [paquet.pop(), paquet.pop()]
    main_banque = [paquet.pop(), paquet.pop()]

    partie_finie = False

    label_joueur.config(text="Score joueur : " + str(calcul_score(main_joueur)))
    label_banque.config(text="Score banque : ?")
    label_message.config(text="Partie commencée")


def tirer():
    global partie_finie

    if partie_finie:
        return

    main_joueur.append(paquet.pop())

    score = calcul_score(main_joueur)
    label_joueur.config(text="Score joueur : " + str(score))

    if score > 21:
        label_message.config(text="Perdu (dépassé 21)")
        fin()


def rester():
    global partie_finie

    if partie_finie:
        return

    while calcul_score(main_banque) < 17:
        main_banque.append(paquet.pop())

    fin()


def fin():
    global solde, partie_finie

    if partie_finie:
        return

    partie_finie = True

    score_j = calcul_score(main_joueur)
    score_b = calcul_score(main_banque)

    label_banque.config(text="Score banque : " + str(score_b))

    if score_j > 21:
        solde -= pari
        label_message.config(text="Perdu")

    elif score_b > 21 or score_j > score_b:
        solde += pari
        label_message.config(text="Gagné")

    elif score_j < score_b:
        solde -= pari
        label_message.config(text="Banque gagne")

    else:
        label_message.config(text="Egalité")

    label_solde.config(text="Solde : " + str(solde) + " €")


# ======================
# BOUTONS
# ======================

tk.Button(fenetre, text="Commencer", command=commencer).pack()
tk.Button(fenetre, text="Tirer", command=tirer).pack()
tk.Button(fenetre, text="Rester", command=rester).pack()

# ======================
# LANCEMENT
# ======================

fenetre.mainloop()