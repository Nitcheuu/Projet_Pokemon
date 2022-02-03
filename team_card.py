from cgitb import text
from operator import index
from tkinter import *
from tkinter import ttk, Tk
import json
from functools import partial
import os


class TeamCard:

    sprite : PhotoImage
    fond_carte : PhotoImage
    dossier : str
    frame : Frame
    textButton : str
    bouton : ttk.Button



    def __init__(self, dossier : str, frame : Frame, textButton : str):
        # Dossier qui contient les informations du pokémon
        self.dossier = dossier
        # Contient le sprite par défault du pokémon
        self.sprite = PhotoImage(file=f"data/pokemons/{dossier}/front_default.png")
        # La méthode subsample permet de dezoomer l'image
        self.fond_carte = PhotoImage(file="assets/equipe/carte.png").subsample(2, 6)
        # Frame de la carte
        self.frame = frame
        # Contient le texte du bouton
        self.textButton = textButton
        # Coleur de fond
        self.coleur_fond = "#334257"

        self.fond = Label(self.frame, image=self.fond_carte, background=self.coleur_fond)

        self.bouton = ttk.Button(self.frame, text=self.textButton)



    
    def equipe_carte(self, chargement=False):

        self.fond.grid(columnspan=4, row=0)

        Label(self.frame, image=self.sprite).grid(column=3, row=0)

        ttk.Button(self.frame, text="Modifier").grid(column=1, row=0)

        ttk.Label(self.frame, text=self.dossier.split("_")[1]).grid(column=2, row=0)

        self.bouton.grid(column=0, row=0)



    def equipe_carte_vide(self):
        Label(self.frame, image=self.fond_carte, background=self.coleur_fond).grid(columnspan=4, row=0)


    def destroy(self):
        self.frame.destroy()

