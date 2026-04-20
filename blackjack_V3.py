import tkinter as tk
import random

# ======================
# VARIABLES
# ======================

solde = 1000 #solde initial du joueur en euros
pari = 0 #ici on a le montant misé par le joueur pour la partie qui est en cours 

paquet = [] #le paquet de 52 cartes (liste de tuples(valeur, couleur))
main_joueur = [] #les cartes en mains du joeur de la partie 
main_banque = [] # les cartes en mains de la banque( le joueur en face ) 

partie_finie = False # verouiller : ça empeche d'agir après la fin d'une manche 

# ======================
# FONCTIONS
# ======================

def creer_paquet():
    """
    Crée et retourne un paquet de 52 cartes qui est mélangé aléatoirement. 

    Chaque carte est représentée par un tuple avec une valeur et une couleur
    Exemple : ("A","♠") pour l'As de Pique.
    
    et on va retourner : 
        list : Liste de 52 tuples qui vont représenter les cartes mélangées 
    
    """
    couleurs = ["♠", "♥", "♦", "♣"]
    valeurs = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]

    p = []
    for c in couleurs:
        for v in valeurs:
            p.append((v, c)) #On ajoute chaque combinaison couleur / valeur a p 

    random.shuffle(p) # puis on fait un mélange aléatoire du paquet 
    return p


def calcul_score(main):
    """
    Cette fonction va calculer et retourner le score d'une main selon les règles du blackjack 

    Les règles a appliquées :
    - Les figures (J, Q, K) elle valent 10 point dans les règles 
    - L'As ( A) vaut 11 points dans les règles par défaut, mais il peut ètre réduit à 1 
    - les autres ont leurs valeurs par défaut et valent leurs valeurs numérique

    Args ( parametre de la fonction ) : 
    main est une liste qui contient des tuples ou chaque tuple contient deux éléments les valeurs et couleurs sur les cartes 
    exemple : [("A", "♠"), ("7", "♥"), ("K", "♦")]

    et le return :
        int: le score total de la main, toujours <= 21 si c'est possible. 
    """
    score = 0
    nb_as = 0 #Compte les As pour pouvoir les revaluer si besoin donner soit 11 ou 1 

    for carte in main:
        v = carte[0] # On va extraire uniquement la valeur ( ex: "A", "10", "K")

        if v in ["J","Q","K"]:  
            score += 10 # Les figures valent toujours 10 et n'ont pas changés
        elif v == "A":
            score += 11 # l'as vaut 11 par défaut 
            nb_as += 1 
        else:
            score += int(v) # les cartes numériques valent leur chifrre 
            
# condition : si on dépasse 21 et qu'on a des As compté à 11, on les repasse à 1
    
    while score > 21 and nb_as > 0:
        score -= 10
        nb_as -= 1

    return score


# ======================
# INTERFACE GRAFIQUE (Tkinter) 
# ======================

fenetre = tk.Tk()
fenetre.title("Blackjack")

#Affichage du solde actuel du joeur
label_solde = tk.Label(fenetre, text="Solde : 1000 €")
label_solde.pack()

#Champ de saisie pour que le joueur entre son pari 
entry_pari = tk.Entry(fenetre)
entry_pari.pack()

#Affichage du score du joueur (mis à jour dynamiquement) 
label_joueur = tk.Label(fenetre, text="Score joueur : 0")
label_joueur.pack()

#Affichage du score de la banque ( "?" tant que la partie est en cours... ) 
label_banque = tk.Label(fenetre, text="Score banque : ?")
label_banque.pack()

#zone de message d'information ( donc le résultat, erreurs, etat de la partie) 
label_message = tk.Label(fenetre, text="")
label_message.pack()

# ======================
# LOGIQUE DU JEU
# ======================

def commencer():
    """
    Initialise et démare une nouvelle partie 

    -Vérifie que le pari saisi est valide donc il faut un entier, positif, <= solde 
    -on va crée un nouveau paquet mélangé.
    - Distribue 2 cartes au joueur et 2 cartes à la banque.
    - et on va réinitialisé les labels de l'interface
    
    """
    global paquet, main_joueur, main_banque, pari, partie_finie
    
    #on a une lecture et une validation du pari depuis le champs de saisie 
    try:
        pari = int(entry_pari.get())
    except:
        label_message.config(text="Pari invalide") # saisie non numérique 
        return

    if pari <= 0 or pari > solde:
        label_message.config(text="Pari incorrect") # pari qui est hors limites 
        return
    
    #Création d'un nouveau paquet a chaque nouvelle partie ( réappel la fonction ) 
    paquet = creer_paquet()

    #distribution initiale : 2 cartes chacun le joueur et la banque et on pioche en haut du paquet 
    main_joueur = [paquet.pop(), paquet.pop()]
    main_banque = [paquet.pop(), paquet.pop()]

    partie_finie = False # la partie peut commencer  

    # on met a jour l'interface en refaisant appel a Tkinter et les labels 
    label_joueur.config(text="Score joueur : " + str(calcul_score(main_joueur)))
    label_banque.config(text="Score banque : ?") # score de la banque masqué 
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
