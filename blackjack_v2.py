import tkinter as tk
from tkinter import ttk, messagebox
import random

SOLDE_INITIAL = 1000


# ======================
# LOGIQUE
# ======================

def creer_paquet():
    couleurs = ["♠", "♥", "♦", "♣"]
    valeurs = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
    paquet = [(v,c) for c in couleurs for v in valeurs]
    random.shuffle(paquet)
    return paquet


def valeur_carte(v):
    if v in ["J","Q","K"]:
        return 10
    if v == "A":
        return 11
    return int(v)


def calculer_score(main):

    score = sum(valeur_carte(v) for v,_ in main)
    as_count = sum(1 for v,_ in main if v=="A")

    while score > 21 and as_count:
        score -= 10
        as_count -= 1

    return score


# ======================
# GUI
# ======================

class BlackjackGUI:

    def __init__(self,root):

        self.root=root
        self.root.title("🎰 Blackjack Casino")
        self.root.geometry("1100x750")
        self.root.configure(bg="#0b5e2b")

        self.solde=SOLDE_INITIAL
        self.pari=0

        self.paquet=[]
        self.joueur=[]
        self.banque=[]

        self.partie_terminee=False

        style=ttk.Style()
        style.theme_use("clam")
        style.configure("Casino.TButton",font=("Arial",14,"bold"),padding=8)

        # ===== HEADER =====

        header=tk.Frame(root,bg="#0b5e2b")
        header.pack(pady=10)

        self.label_solde=tk.Label(
            header,
            font=("Arial",24,"bold"),
            fg="gold",
            bg="#0b5e2b"
        )
        self.label_solde.pack()

        # ===== TABLE =====

        self.canvas=tk.Canvas(
            root,
            width=1000,
            height=420,
            bg="#0b5e2b",
            highlightthickness=0
        )
        self.canvas.pack(pady=20)

        self.pos_banque=(350,80)
        self.pos_joueur=(350,260)
        self.pos_paquet=(900,160)

        self.dessiner_table()

        # ===== SCORES =====

        self.score_banque=tk.Label(
            root,
            text="Score banque : ?",
            font=("Arial",16),
            fg="white",
            bg="#0b5e2b"
        )
        self.score_banque.pack()

        self.score_joueur=tk.Label(
            root,
            text="Score joueur : 0",
            font=("Arial",16),
            fg="white",
            bg="#0b5e2b"
        )
        self.score_joueur.pack()

        # ===== PARI =====

        frame_pari=tk.Frame(root,bg="#0b5e2b")
        frame_pari.pack(pady=15)

        self.entry_pari=tk.Entry(
            frame_pari,
            font=("Arial",18),
            width=8,
            justify="center"
        )
        self.entry_pari.grid(row=0,column=0,padx=10)

        self.btn_parier=ttk.Button(
            frame_pari,
            text="🎲 Parier",
            command=self.demarrer_partie,
            style="Casino.TButton"
        )
        self.btn_parier.grid(row=0,column=1)

        # ===== ACTIONS =====

        frame_actions=tk.Frame(root,bg="#0b5e2b")
        frame_actions.pack(pady=10)

        self.btn_tirer=ttk.Button(
            frame_actions,
            text="🃏 Tirer",
            command=self.tirer_carte,
            state="disabled",
            style="Casino.TButton"
        )
        self.btn_tirer.grid(row=0,column=0,padx=20)

        self.btn_rester=ttk.Button(
            frame_actions,
            text="✋ Rester",
            command=self.rester,
            state="disabled",
            style="Casino.TButton"
        )
        self.btn_rester.grid(row=0,column=1,padx=20)

        # ===== MESSAGE =====

        self.message=tk.Label(
            root,
            text="",
            font=("Arial",24,"bold"),
            fg="yellow",
            bg="#0b5e2b"
        )
        self.message.pack(pady=20)

        self.mettre_a_jour_solde()


    # ======================
    # TABLE
    # ======================

    def dessiner_table(self):

        self.canvas.delete("all")

        self.canvas.create_arc(
            200,20,800,320,
            start=0,
            extent=180,
            style="arc",
            width=3,
            outline="white"
        )

        self.canvas.create_text(
            500,40,
            text="BLACKJACK PAYS 3:2",
            fill="white",
            font=("Arial",16,"bold")
        )

        # paquet

        self.canvas.create_rectangle(
            self.pos_paquet[0],
            self.pos_paquet[1],
            self.pos_paquet[0]+70,
            self.pos_paquet[1]+100,
            fill="white",
            outline="black",
            width=3
        )

        self.canvas.create_text(
            self.pos_paquet[0]+35,
            self.pos_paquet[1]+50,
            text="🂠",
            font=("Arial",28)
        )


    # ======================
    # CARTES
    # ======================

    def creer_carte(self,x,y,texte):

        rect=self.canvas.create_rectangle(
            x,y,x+70,y+100,
            fill="white",
            outline="black",
            width=3
        )

        txt=self.canvas.create_text(
            x+35,y+50,
            text=texte,
            font=("Arial",18,"bold")
        )

        return rect,txt


    def animer_carte(self,texte,destination,index):

        start_x,start_y=self.pos_paquet
        dest_x=destination[0]+index*80
        dest_y=destination[1]

        rect,txt=self.creer_carte(start_x,start_y,texte)

        dx=(dest_x-start_x)/20
        dy=(dest_y-start_y)/20

        def move(step=0):

            if step<20:
                self.canvas.move(rect,dx,dy)
                self.canvas.move(txt,dx,dy)
                self.root.after(15,lambda:move(step+1))

        move()


    def poser_carte_direct(self,texte,destination,index):

        x=destination[0]+index*80
        y=destination[1]

        self.creer_carte(x,y,texte)


    # ======================
    # GAME
    # ======================

    def mettre_a_jour_solde(self):
        self.label_solde.config(text=f"💰 Solde : {self.solde} €")


    def demarrer_partie(self):

        try:
            self.pari=int(self.entry_pari.get())
        except:
            messagebox.showerror("Erreur","Pari invalide")
            return

        if self.pari<=0 or self.pari>self.solde:
            messagebox.showerror("Erreur","Pari invalide")
            return

        # CORRECTION
        self.partie_terminee=False

        self.message.config(text="")

        self.dessiner_table()

        self.paquet=creer_paquet()

        self.joueur=[self.paquet.pop(),self.paquet.pop()]
        self.banque=[self.paquet.pop(),self.paquet.pop()]

        # distribution initiale

        self.animer_carte(f"{self.joueur[0][0]}{self.joueur[0][1]}",self.pos_joueur,0)
        self.animer_carte("🂠",self.pos_banque,0)
        self.animer_carte(f"{self.joueur[1][0]}{self.joueur[1][1]}",self.pos_joueur,1)
        self.animer_carte(f"{self.banque[1][0]}{self.banque[1][1]}",self.pos_banque,1)

        self.btn_tirer.config(state="normal")
        self.btn_rester.config(state="normal")

        self.score_joueur.config(text=f"Score joueur : {calculer_score(self.joueur)}")
        self.score_banque.config(text="Score banque : ?")


    def tirer_carte(self):

        if self.partie_terminee:
            return

        carte=self.paquet.pop()
        self.joueur.append(carte)

        index=len(self.joueur)-1

        self.animer_carte(
            f"{carte[0]}{carte[1]}",
            self.pos_joueur,
            index
        )

        self.score_joueur.config(text=f"Score joueur : {calculer_score(self.joueur)}")

        if calculer_score(self.joueur)>21:
            self.fin_partie()


    def rester(self):

        if self.partie_terminee:
            return

        self.poser_carte_direct(
            f"{self.banque[0][0]}{self.banque[0][1]}",
            self.pos_banque,
            0
        )

        while calculer_score(self.banque)<17:

            carte=self.paquet.pop()
            self.banque.append(carte)

            self.poser_carte_direct(
                f"{carte[0]}{carte[1]}",
                self.pos_banque,
                len(self.banque)-1
            )

        self.fin_partie()


    def fin_partie(self):

        self.partie_terminee=True

        self.btn_tirer.config(state="disabled")
        self.btn_rester.config(state="disabled")

        score_joueur=calculer_score(self.joueur)
        score_banque=calculer_score(self.banque)

        self.score_banque.config(text=f"Score banque : {score_banque}")

        if score_joueur>21:
            self.solde-=self.pari
            self.message.config(text="💥 PERDU")

        elif score_banque>21 or score_joueur>score_banque:
            self.solde+=self.pari
            self.message.config(text="🏆 GAGNÉ")

        elif score_joueur<score_banque:
            self.solde-=self.pari
            self.message.config(text="😢 BANQUE GAGNE")

        else:
            self.message.config(text="🤝 ÉGALITÉ")

        self.mettre_a_jour_solde()


# ======================
# MAIN
# ======================

root=tk.Tk()
app=BlackjackGUI(root)
root.mainloop()