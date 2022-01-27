from cgitb import text
from operator import index
from tkinter import *
from tkinter import ttk, Tk
import json
from functools import partial
import os

class TeamCard:

    sprites : PhotoImage
    dossier : str
    frame : Frame
    index : int
    textButton : str


    def __init__(self, sprites : PhotoImage, dossier : str, frame : Frame, index : int, textButton : str):
        self.sprites = sprites
        self.dossier = dossier
        self.frame = frame
        self.index = index
        self.textButton = textButton

    
    def card(self):
        self.sprites.append(PhotoImage(file=f"data/pokemons/{self.dossier}/front_default.png"))

        Label(self.frame, image=self.sprites).grid(column=3, row=self.index)

        ttk.Label(self.frame, text=self.dossier.split("_")[0]).grid(column=1, row=self.index)

        ttk.Label(self.frame, text=self.dossier.split("_")[0]).grid(column=2, row=self.index)

        ttk.Button(self.frame, text=self.textButton, command=partial(print, str(self.index))).grid(column=0, row=self.index)
