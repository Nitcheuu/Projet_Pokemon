from cgitb import text
from operator import index
from tkinter import *
from tkinter import ttk, Tk
import json
from functools import partial
import os


class TeamCard:

    sprite : PhotoImage
    dossier : str
    frame : Frame
    textButton : str
    bouton : ttk.Button



    def __init__(self, dossier : str, frame : Frame, textButton : str):
        self.dossier = dossier
        self.sprite = PhotoImage(file=f"data/pokemons/{dossier}/front_default.png")
        self.frame = frame
        self.textButton = textButton

    
    def card(self):

        print(self.frame)

        Label(self.frame, image=self.sprite).grid(column=3, row=0)

        ttk.Label(self.frame, text=self.dossier.split("_")[0]).grid(column=1, row=0)

        ttk.Label(self.frame, text=self.dossier.split("_")[1]).grid(column=2, row=0)

        self.bouton = ttk.Button(self.frame, text=self.textButton)

        self.bouton.grid(column=0, row=0)


    def destroy(self):
        self.frame.destroy()

