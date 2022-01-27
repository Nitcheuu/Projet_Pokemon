from cProfile import label
from email.mime import image
from tkinter import *
from tkinter import ttk, Tk
import json
from functools import partial
import os
from team_card import TeamCard

from PIL import ImageTk,Image


class Application:

    """
    Zone des attributs
    """

    principal: Tk   # Fenêtre principale de l'application
    largeur : int   # Dimensions de la fenêtre
    hauteur : int
    save : dict     # Dictionaire qui contient les informations de la sauvegarde
    sprites : list[PhotoImage]
    dimension : int # Dimension de la matrice qui modélise le pc
    unlock_pokemons : list[list[list[str]]] # Modélise le pc

    poke_cards_liste : list[TeamCard]   # Liste des pokémons débloqués
    poke_cards_equipe : list[TeamCard]  # Liste des pokémons de l'équipe du joueur
    poke_cards_liste_frame: list[Frame]  # Liste des pokémons débloqués
    poke_cards_equipe_frame: list[Frame]  # Liste des pokémons de l'équipe du joueur


    dossiers : list[str]

    imageCombat : PhotoImage
    imageBoutique : PhotoImage
    imageEquipe : PhotoImage
    imageQuitter : PhotoImage

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
        self.sprites = []
        self.poke_cards_liste = []
        self.poke_cards_equipe = []
        self.poke_cards_liste_frame = []
        self.poke_cards_equipe_frame = []
        self.dimension_pc = (3, 3)

        
        # Recuperation de la liste des dossiers des pokémons
        self.dossiers = os.listdir("data/pokemons")

        self.imageCombat = PhotoImage(file= "assets/menu/battle.png").subsample(3,3)
        self.imageBoutique = PhotoImage(file= "assets/menu/boutique.png").subsample(4,4)
        self.imageEquipe = PhotoImage(file= "assets/menu/equipe.png").subsample(4,4)
        self.imageQuitter = PhotoImage(file= "assets/menu/quitter.png").subsample(4,4)
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

    def vider_frame(self, frm : Frame):

        frm.destroy()

        # Définition du frame principale
        frm = Frame(self.principal, width=self.largeur, height=self.hauteur)

        # Comme la position de la frame est relative au coin bas gauche de la frame
        # on utilise les options rel x et y qui permettent de palier ce problème
        frm.place(anchor=CENTER, relx=.5, rely=.5)

        return frm

    def client(self, frm=None):

        """
        VA : Permet de gérer toutes les actions préalables au lancement d'une partie
        """
        if frm is not None:
            self.vider_frame(frm)

        # Définition du frame principale
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


    def informations_utilisateur(self, frm : Frame):


        self.sprites = []

        for pokemon in self.save["player"]["team"]:
            self.sprites.append(PhotoImage(file=f"data/pokemons/{pokemon}/front_default.png"))

        # affiche les pokemons dans l'équipe 
        for i in range(len(self.sprites)):
            Label(frm, image=self.sprites[i]).grid(column=i, row=0)


        # Pseudo du joueur
        ttk.Label(frm, text=self.save["player"]["name"], font=("Courrier", 10)
                  ).grid(column=0, row=0)

        # Niveau du joueur
        ttk.Label(frm, text=f'{self.save["player"]["level"]}', font=("Courrier", 10)
                  ).grid(column=1, row=0)

        # Montant de jetons du joueur
        ttk.Label(frm, text=f'{self.save["player"]["coin_amount"]}', font=("Courrier", 10),
                  foreground="green").grid(column=2, row=0)

    def lobby(self, frm : Frame):

        """
        VA : Permet d'afficher l'ensemble des éléments du lobby
        :param frm: Frame principale de l'application
        :return: None
        """


        self.informations_utilisateur(frm)

        # Boutique
        Button(frm, text="Boutique", image=self.imageBoutique, relief=FLAT,
                   ).grid(column=0, row=2)

        # Ouverture de l'onglet équipe
        Button(frm, text="Mon équipe", image=self.imageEquipe, relief=FLAT, command=lambda : self.equipe(frm)
                   ).grid(column=2, row=2)

        # Lancement d'une partie
        Button(frm, text="Lancer une partie", image=self.imageCombat, relief=FLAT,
                   ).grid(column=1, row=1)

        # Quitter le jeu
        Button(frm, text="Quitter le jeu", image=self.imageQuitter, relief=FLAT, command=self.principal.destroy
                   ).grid(column=1, row=2)


    def equipe(self, frm : Frame):

        """
        VA : Permet au joueur de gérer son équipe en affichant l'ensemble des éléments et des outils de la gestion
             de l'équipe
        :param frm: Frame princial de l'application
        :return: None
        """
        # Vider le frame principal
        frm_equipe_principal : Frame = self.vider_frame(frm)

        # Frame de la liste des pokémons disponibles
        frm_liste : Frame = Frame(frm_equipe_principal, background='#%02x%02x%02x' % (64, 204, 208))
        frm_liste.grid(column=0, row=0, padx=50)

        # Frame de l'équipe du joueur
        frm_equipe : Frame = Frame(frm_equipe_principal, background='#%02x%02x%02x' % (64, 0, 208))
        frm_equipe.grid(column=1, row=0, padx=50)

        for i in range(len(self.save["player"]["unlock_pokemons"])):
            """
            Dans cette boucle, on défini les "cartes" des pokémons que le joueur a débloqué
            """
            frm_carte = Frame(frm_liste)
            frm_carte.place(anchor=CENTER, rely=.5, relx=.5)
            frm_carte.grid(column=0, row=i)
            self.poke_cards_liste_frame.append(frm_carte)
            # Chargement du sprite du pokémon
            sprite : PhotoImage = PhotoImage(file=f'data/pokemons/{self.save["player"]["unlock_pokemons"][i]}/front_default.png')
            # On instancie une nouvelle "carte" qu'on ajoute à la liste des cartes
            self.poke_cards_liste.append(TeamCard(sprite, self.save["player"]["unlock_pokemons"][i], frm_carte, i, "Ajouter"))
            # On appelle la méthode de la classe qui permet d'afficher la carte à l'écran pour chaque carte
            self.poke_cards_liste[i].card()

            self.poke_cards_liste[i].bouton.bind("<Button-1>", partial(print, i))

        for i in range(len(self.save["player"]["team"])):
            for dossier in self.dossiers:
                if dossier == self.save["player"]["team"][i]:
                    frm_carte = Frame(frm_equipe)
                    frm_carte.place(anchor=CENTER, rely=.5, relx=.5)
                    frm_carte.grid(column=0, row=i)
                    self.poke_cards_equipe_frame.append(frm_carte)

                    sprite : PhotoImage = PhotoImage(file=f"data/pokemons/{dossier}/front_default.png")

                    self.poke_cards_equipe.append(TeamCard(sprite, dossier, frm_equipe, i, "Retirer"))


                    self.poke_cards_equipe[i].card()

                    self.poke_cards_equipe[i].bouton.bind("<Button-1>", partial(self.swap, i, frm))
                    """"# On ouvre et on stock les images dans un attribut de l'objet courant
                    # à cause du garbage collector
                    self.sprites.append(PhotoImage(file=f"data/pokemons/{dossier}/front_default.png"))
                    # Création de la zone qui contiendra l'image
                    Label(frm_equipe, image=self.sprites[-1]
                          ).grid(column=3, row=i)

                    ttk.Label(frm_equipe, text=dossier.split("_")[0]
                              ).grid(column=1, row=i)

                    ttk.Label(frm_equipe, text=dossier.split("_")[1]
                              ).grid(column=2, row=i)
=======
        for i in range(len(self.save["player"]["team"])):
            for dossier in self.dossiers:
                for pokemon in self.save["player"]["team"]:
                    if dossier == pokemon:
                        # On ouvre et on stock les images dans un attribut de l'objet courant
                        # à cause du garbage collector
                        self.sprites.append(PhotoImage(file=f"data/pokemons/{dossier}/front_default.png"))
                        # Création de la zone qui contiendra l'image
                        Label(frm_equipe, image=self.sprites[-1]
                              ).grid(column=3, row=i)
>>>>>>> fb467850e6b9bf474ef22e044f85cf872794fc08

                    ttk.Button(frm_equipe, text="Retirer", command=partial(print, str(i))
                               ).grid(column=0, row=i)"""

        ttk.Button(frm_equipe, text="Menu principal", command=lambda : self.client(frm)).grid(column=0, row=len(self.poke_cards_equipe))


    def swap(self, index : int, frm : Frame, team2pc = True):
        if team2pc:
            self.save["player"]["unlock_pokemons"].append(f"{self.poke_cards_equipe[index].dossier.split('_')[0]}_{self.poke_cards_equipe[index].dossier.split('_')[1]}")
            self.poke_cards_liste.append(self.poke_cards_equipe[index])
            self.poke_cards_equipe[index].destroy()
            self.poke_cards_equipe.pop(index)
            self.poke_cards_equipe_frame[index].destroy()
            self.save["player"]["team"].pop(index)
            self.sauvegarder()
            self.equipe(frm)
