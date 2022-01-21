from tkinter import *
from tkinter import ttk, Tk
import json


class Application:

    """
    Zone des attributs
    """

    principal: Tk   # Fenêtre principale de l'application
    largeur : int   # Dimensions de la fenêtre
    hauteur : int
    save : dict     # Dictionaire qui contient les informations de la sauvegarde

    """
    Zone constructeurs
    """
    
    def __init__(self, largeur : int, hauteur : int):
        self.largeur = largeur
        self.hauteur = hauteur
        self.principal = Tk()
        # Paramètrage de la fenêtre Tkinter
        self.principal.geometry(f"{largeur}x{hauteur}")
        self.principal.resizable(False, False)
        self.principal.title("Pokemon fight - online")
        self.principal.iconphoto(False, PhotoImage(file="assets/logo/logo_fenetre.png"))
        with open("data/save/save.json", "r") as save_data:
            self.save = json.load(save_data)

    """
    Zone des méthodes
    """

    def sauvegarder(self):

        """
        VA : Permet de sauvegarder la session du joueur
        :return:
        """

        with open("data/save/save.json", "w", encoding="utf-8") as save_file:
            json.dump(self.save, save_file, indent=2, separators=(',', ': '))

    def client(self):

        """
        VA : Permet de gérer toutes les actions préalables au lancement d'une partie
        """

        # Définition de la frame principale
        frm = Frame(self.principal, width=self.largeur, height=self.hauteur)

        # Comme la position de la frame est relative au coin bas gauche de la frame
        # on utilise les options rel x et y qui permettent de palier ce problème
        frm.place(anchor=CENTER, relx=.5, rely=.5)

        # Si c'est la première connexion du joueur
        if self.save["game"]["first_connexion"]:
            self.premiere_connexion(frm)
        else:
            self.lobby(frm)



        self.principal.mainloop()

    def enregister_premiere_connexion(self, nom_joueur : StringVar, frms : list[Frame]):

        """
        VA : Permet d'enregistrer dans le fichier de sauvegarde les données du joueur
             saisies par ce dernier
        :param nom_joueur: Pseudo du joueur
        :param frms: Liste contenant les frames à supprimer
        :return: None
        """

        # Sauvegarde du pseudo du joueur
        self.save["player"]["name"] = nom_joueur.get()

        # On passe le champ first connexion sur false
        self.save["game"]["first_connexion"] = False

        self.sauvegarder()

        # Destruction des frames de l'application de première connexion
        for frm in frms:
            frm.destroy()

        # On recharge le client
        self.client()

    def premiere_connexion(self, frm : Frame):

        """
        :param frm: Frame principal de l'application
        :return: None
        """

        # variable qui contient le nom saisi par le joueur
        nom_joueur : StringVar = StringVar()

        ttk.Label(frm, text="Veuillez choisir un nom en jeu : ", font=("Courrier", 20)).grid(column=0, row=0, pady=10)

        ttk.Entry(frm, width=40, textvariable=nom_joueur).grid(column=0, row=1, pady=10)

        ttk.Button(frm, text="Valider",
                   command=lambda : self.enregister_premiere_connexion(nom_joueur, [frm])
                   ).grid(column=0, row=2, pady=10)



    def lobby(self, frm : Frame):

        """
        VA : Permet d'afficher l'ensemble des éléments du lobby
        :param frm: Frame principale de l'application
        :return: None
        """

        # Pseudo du joueur
        ttk.Label(frm, text=self.save["player"]["name"], font=("Courrier", 10)
                  ).grid(column=0, row=0)

        # Niveau du joueur
        ttk.Label(frm, text=f'{self.save["player"]["level"]}', font=("Courrier", 10)
                  ).grid(column=1, row=0)

        # Montant de jetons du joueur
        ttk.Label(frm, text=f'{self.save["player"]["coin_amount"]}', font=("Courrier", 10),
                  foreground="green").grid(column=2, row=0)

        # Boutique
        ttk.Button(frm, text="Boutique"
                   ).grid(column=0, row=1)

        # Ouverture de l'onglet équipe
        ttk.Button(frm, text="Mon équipe"
                   ).grid(column=0, row=2)

        # Lancement d'une partie
        ttk.Button(frm, text="Lancer une partie"
                   ).grid(column=1, row=2)

        # Quitter le jeu
        ttk.Button(frm, text="Quitter le jeu", command=self.principal.destroy
                   ).grid(column=0, row=3)


