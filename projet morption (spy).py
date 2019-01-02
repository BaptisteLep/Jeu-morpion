# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 08:29:16 2018

@author: blepa
"""

#############################
#                           #
#  TicTacToe                #
#    05/12/2018             #
# Leparoux Baptiste et      #
# Juret Lucas               #
#############################

from tkinter import *
from random import randrange

#création des variables importantes
tour =   "j1"
nb_coup=0
grille = [["","",""],\
         ["","",""],\
         ["","",""]]
fini     = False # le jeu est-il fini ?
modeordi = False # le mode ordi est-il activé ?
son      = True
matchnul = False


class Carre : #création de l'espace de jeu recevant les X et les O
    def __init__(self, x, y, color="grey"):
        self.x=x #position X
        self.y=y #position Y
        self.taille=100 #Taille
        self.on=False #est-ce que la zone est activée ? (True = Vrai et False = Faux)
        self.zone=Canvas(jeu, height=self.taille, width=self.taille, bg=color)
        self.zone.grid(row=y, column=x)
        self.zone.bind("<Enter>", self.Entrer)
        self.zone.bind("<Leave>", self.Quitter)
        self.zone.bind("<Button-1>", self.Placer)

    def Raffraichir(self): #raffaichir la zone en fonction de la grille
        if grille[self.y][self.x] != "":
            if grille[self.y][self.x] == "O":
                self.TraceO()
            elif grille[self.y][self.x] == "X":
                self.TraceX()
            self.on=True #le passer en mode actif si la zone n'est pas vide


    def Entrer(self,event): #quand la souris entre dans la zone du Carre
        global tour
        if not self.on and not fini:
            if tour == "j1" :
                self.TraceX(False)
            elif tour =="j2" :
                self.TraceO(False)

    def Quitter(self,event): #quand la souris quitte la zone
        if not self.on and not fini:
            self.Effacer()

    def Placer(self,event): #quand la souris clique
        global tour, grille, nb_coup, modeordi, son
        if not self.on and not fini: # si le carre n'est pas plein et si le jeu n'est pas fini
            self.on=True
            nb_coup += 1
            
            if tour == "j1":
                self.TraceX()
                grille[self.y][self.x]="X"
                tour = "j2"
                self.Raffraichir()
                TicTacToe.Verifier()

                if modeordi == True and not fini:
                    print ("") # pourfaire calculer l'ordi # la X ne  s'affiche pas toltalement durant les 100 ms
                    jeu.after(100,TicTacToe.CoupOrdi()) #met 100 ms avant de jouer (pour effet de non-immediat)
                    TicTacToe.Verifier()



            elif tour == "j2" and modeordi == False:
                self.TraceO()
                grille[self.y][self.x]="O"
                tour = "j1"
        TicTacToe.Verifier()

    def TraceX(self,vrai=True):      #tracer une croix 
        self.Effacer()
        if vrai :
            self.zone.create_line((10,10,self.taille-10,self.taille-10),fill="red",width=5)
            self.zone.create_line((10,self.taille-10,self.taille-10,10),fill="red",width=5)
        else :
            self.zone.create_line((10,10,self.taille-10,self.taille-10),fill="red",width=5)
            self.zone.create_line((10,self.taille-10,self.taille-10,10),fill="red",width=5)
    def TraceO(self,vrai=True):      #tracer un rond 
        self.Effacer()
        if vrai :
            self.zone.create_oval((5,5,self.taille-5,self.taille-5),fill="blue",width=2)
            self.zone.create_oval((10,10,self.taille-10,self.taille-10),fill="grey",width=2)
        else :
            self.zone.create_oval((5,5,self.taille-5,self.taille-5),fill="blue",width=2)
            self.zone.create_oval((10,10,self.taille-10,self.taille-10),fill="grey",width=2)
    def Effacer(self): # effacer le Carre
        self.zone.delete(ALL)

class Jeu :
    def __init__(self):
        self.carre=[[[],[],[]],\
               [[],[],[]],\
               [[],[],[]]]
        for a in range(3):  #création des Carrés
            for i in range(3):
                self.carre[a][i]=Carre(a,i)
        self.j=Label(jeu, text="Joueur "+tour[1]+", c'est ton tour")
        self.j.grid(row=4, column=0, columnspan=3)

        menu=Menu(jeu) #création des menus
        option=Menu(menu, tearoff=0)
        mode=Menu(menu, tearoff=0)

        menu.add_cascade(label="Option", menu=option)
        menu.add_cascade(label="Mode", menu=mode)

        option.add_command(label="Quitter", command=jeu.destroy)
        option.add_command(label="Recommencer (R)", command=self.Reinit)
        

        mode.add_command(label="1 joueur", command = lambda : self.ModeOrdi(True))
        mode.add_command(label="2 joueurs", command = lambda : self.ModeOrdi(False))
        jeu.bind_all("<r>", lambda event : self.Reinit())

        jeu.config(menu=menu)
   
    def ModeOrdi(self, mode): #passage en mode ordi
        global modeordi, tour
        modeordi = mode
        if mode == True :
            tour = "j1"
        self.Reinit()

    def CoupOrdi(self): #créer un coup aléatoire
        global grille, carre, tour, nb_coup
        coupX, coupY= randrange(0,3), randrange(0,3)
        if fini == False :
            while 1 : #tant que le coup sera sur une case occupée, il relancera l'aléatoire
                coupX = randrange(0,3)
                coupY = randrange(0,3)
                if grille[coupY][coupX] == "":
                    grille[coupY][coupX] = "O"
                    break
        nb_coup += 1 #augmenter le nombre de coups joués
        tour ="j1" # c'est à j1 de jouer
        self.carre[coupX][coupY].Raffraichir()


    def Reinit(self): #réinisialisation
        global grille, nb_coup, fini, tour
        grille=[["","",""],\
         ["","",""],\
         ["","",""]]
        nb_coup=0
        fini=False
        matchnul = False
        self.carre=[[[],[],[]],\
               [[],[],[]],\
               [[],[],[]]]
        for a in range(3):
            for i in range(3):
                self.carre[a][i]=Carre(a,i)
        if modeordi == True :
            tour = "j1"


    def Verifier(self): #vérification des positions des X et des O
        self.j.config(text="Joueur "+tour[1]+", c'est ton tour")
        global fini, nb_coup, son, matchnul
        if nb_coup == 9 : #quand toutes les cases sont occupées, match nul
            self.j.config(text="Match Nul !")
            matchnul = True

        if grille[0][0]==grille[0][1] and grille[0][0]==grille[0][2] and grille[0][0] != "" :
            if grille[0][0]=="X":
                self.j.config(text="Joueur 1 à Gagné !")
            elif grille[0][0]=="O":
                self.j.config(text="Joueur 2 à Gagné !")
            fini =True

        elif grille[1][0]==grille[1][1] and grille[1][0]==grille[1][2] and grille[1][0] != "" :
            if grille[1][0]=="X":
                self.j.config(text="Joueur 1 à Gagné !")
            elif grille[1][0]=="O":
                self.j.config(text="Joueur 2 à Gagné !")
            fini =True

        elif grille[2][0]==grille[2][1] and grille[2][0]==grille[2][2] and grille[2][0] != "" :
            if grille[2][0]=="X":
                self.j.config(text="Joueur 1 à Gagné !")
            elif grille[2][0]=="O":
                self.j.config(text="Joueur 2 à Gagné !")
            fini =True


        elif grille[0][0]==grille[1][0] and grille[0][0]==grille[2][0] and grille[0][0] != "" :
            if grille[0][0]=="X":
                self.j.config(text="Joueur 1 à Gagné !")
            elif grille[0][0]=="O":
                self.j.config(text="Joueur 2 à Gagné !")
            fini =True

        elif grille[0][1]==grille[1][1] and grille[0][1]==grille[2][1] and grille[0][1] != "" :
            if grille[0][1]=="X":
                self.j.config(text="Joueur 1 à Gagné !")
            elif grille[0][1]=="O":
                self.j.config(text="Joueur 2 à Gagné !")
            fini =True

        elif grille[0][2]==grille[1][2] and grille[0][2]==grille[2][2] and grille[0][2] != "" :
            if grille[0][2]=="X":
                self.j.config(text="Joueur 1 à Gagné !")
            elif grille[0][2]=="O":
                self.j.config(text="Joueur 2 à Gagné !")
            fini =True

        elif grille[0][0]==grille[1][1] and grille[0][0]==grille[2][2] and grille[0][0] != "" :
            if grille[0][0]=="X":
                self.j.config(text="Joueur 1 à Gagné !")
            elif grille[0][0]=="O":
                self.j.config(text="Joueur 2 à Gagné !")
            fini =True

        elif grille[0][2]==grille[1][1] and grille[0][2]==grille[2][0] and grille[0][2] != "" :
            if grille[0][2]=="X":
                self.j.config(text="Joueur 1 à Gagné !")
            elif grille[0][2]=="O":
                self.j.config(text="Joueur 2 à Gagné !")
            fini =True

        if matchnul :
            fini= True

        if fini == True :
            matchnul=False
            nb_coup=0


if __name__ == '__main__' : 
    jeu=Tk()
    jeu.title("Morpion")
    jeu.resizable(width=False, height=False)
    TicTacToe=Jeu()
    jeu.mainloop()