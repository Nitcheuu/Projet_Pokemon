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
    index : int
    textButton : str
    bouton : ttk.Button



    def __init__(self, sprite : PhotoImage, dossier : str, frame : Frame, index : int, textButton : str):
        self.sprite = sprite
        self.dossier = dossier
        self.frame = frame
        self.index = index
        self.textButton = textButton

    
    def card(self):

        Label(self.frame, image=self.sprite).grid(column=3, row=0)

        ttk.Label(self.frame, text=self.dossier.split("_")[0]).grid(column=1, row=0)

        ttk.Label(self.frame, text=self.dossier.split("_")[1]).grid(column=2, row=0)

        self.bouton = ttk.Button(self.frame, text=self.textButton)

        self.bouton.grid(column=0, row=0)


    def destroy(self):
        self.frame.destroy()

