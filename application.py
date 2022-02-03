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
    poke_cards_liste_visible: list[TeamCard]  # Liste des pokémons débloqués visibles
    poke_cards_equipe : list[TeamCard]  # Liste des pokémons de l'équipe du joueur
    poke_cards_liste_frame: list[Frame]  # Liste des pokémons débloqués
    poke_cards_equipe_frame: list[Frame]  # Liste des pokémons de l'équipe du joueur
    poke_cards_liste_index_min : int  # Les index min et max indiquent quelles cartes affiché pour la navigation
    poke_cards_liste_index_max : int


    dossiers : list[str]

    imageCombat : PhotoImage
    imageBoutique : PhotoImage
    imageEquipe : PhotoImage
    imageQuitter : PhotoImage

    couleur_fond : str

    """
    Zone constructeurs
    """

    def __init__(self, largeur : int, hauteur : int):
        self.largeur = largeur
        self.hauteur = hauteur
        self.principal = Tk()
        # Paramètrage de la fenêtre Tkinter
        #self.principal.geometry(f"{largeur}x{hauteur}")
        self.principal.attributes('-fullscreen', True)
        self.principal.resizable(False, False)
        self.principal.title("Pokemon fight - online")
        self.principal.iconphoto(False, PhotoImage(file="assets/logo/logo_fenetre.png"))
        self.principal.config(background="#334257")
        with open("data/save/save.json", "r") as save_data:
            self.save = json.load(save_data)
        self.sprites = []

        self.poke_cards_liste = []
        self.poke_cards_liste_visible = []
        self.poke_cards_equipe = []
        self.poke_cards_liste_index_min = 0
        self.poke_cards_liste_index_max = 6

        # Recuperation de la liste des dossiers des pokémons
        self.dossiers = os.listdir("data/pokemons")

        self.imageCombat = PhotoImage(file= "assets/menu/battle.png")
        self.imageBoutique = PhotoImage(file= "assets/menu/boutique.png")
        self.imageEquipe = PhotoImage(file= "assets/menu/equipe.png")
        self.imageQuitter = PhotoImage(file= "assets/menu/quitter.png")

        self.couleur_fond = "#334257"
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

    def vider_frame(self, frm : Frame, couleur : str = None):

        frm.destroy()

        # Définition du frame principale
        frm = Frame(self.principal, width=self.largeur, height=self.hauteur, background=couleur)
        self.principal.config(background=couleur)

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

        # Création du frame qui affiche les informations du joueur
        frm_joueur = Frame(frm)

        # Placement des informations du joueur sur la fenêtre
        frm_joueur.grid(column=0, row=0, columnspan=3)

        # Pseudo du joueur
        ttk.Label(frm_joueur, text=self.save["player"]["name"], font=("Courrier", 10), background=self.couleur_fond,
                  foreground="white"
                  ).grid(column=0, row=0)

        # Niveau du joueur
        ttk.Label(frm_joueur, text=f'{self.save["player"]["level"]}', font=("Courrier", 10), background=self.couleur_fond,
                  foreground="white"
                  ).grid(column=1, row=0)

        # Montant de jetons du joueur
        ttk.Label(frm_joueur, text=f'{self.save["player"]["coin_amount"]}', font=("Courrier", 10), background=self.couleur_fond,
                  foreground="green").grid(column=2, row=0)


    def lobby_afficher_pokemons(self, frm : Frame):

        frm_pokemon : Frame = Frame(frm)

        frm_pokemon.grid(column=0, row=1, columnspan=3)

        self.sprites = []

        for pokemon in self.save["player"]["team"]:
            self.sprites.append(PhotoImage(file=f"data/pokemons/{pokemon}/front_default.png"))

        # affiche les pokemons dans l'équipe
        for i in range(len(self.sprites)):
            Label(frm_pokemon, image=self.sprites[i], background=self.couleur_fond).grid(column=i, row=0)

    def lobby(self, frm : Frame):

        """
        VA : Permet d'afficher l'ensemble des éléments du lobby
        :param frm: Frame principale de l'application
        :return: None
        """

        frm = self.vider_frame(frm, couleur="#334257")

        self.informations_utilisateur(frm)

        self.lobby_afficher_pokemons(frm)

        # Boutique
        Button(frm, text="Boutique", image=self.imageBoutique, relief=FLAT, background=self.couleur_fond
                   ).grid(column=0, row=4)

        # Ouverture de l'onglet équipe
        Button(frm, text="Mon équipe", image=self.imageEquipe, relief=FLAT, command=lambda : self.equipe(frm), background=self.couleur_fond
                   ).grid(column=2, row=4)

        # Lancement d'une partie
        Button(frm, text="Lancer une partie", image=self.imageCombat, relief=FLAT, background=self.couleur_fond
                   ).grid(column=0, row=3, columnspan=3)

        # Quitter le jeu
        Button(frm, text="Quitter le jeu", image=self.imageQuitter, relief=FLAT, command=self.principal.destroy, background=self.couleur_fond
                   ).grid(column=1, row=4)


    def equipe(self, frm : Frame):
        # On vide dans un premier temps les listes qui contiennent les cartes
        self.poke_cards_equipe = []
        self.poke_cards_liste = []
        # On vide le frame principal pour avoir un nouvel espace de travail
        frm_principal = self.vider_frame(frm, couleur="#334257")
        # Définition du frame qui contiendra la liste des pokémons disponibles
        frm_liste : Frame = Frame(frm_principal, padx=25, background="#334257")
        frm_liste.grid(column=0, row=0)
        # Définiton du frame qui contiendra la liste des pokémons de l'équipe du joueur
        frm_equipe : Frame = Frame(frm_principal, padx=25, background="#334257")
        frm_equipe.grid(column=1, row=0)
        # Affichage de l'équipe du joueur
        self.equipe_afficher_equipe(frm_principal, frm_equipe)
        self.equipe_afficher_liste(frm_principal, frm_liste)
        Button(frm_principal, text="Menu Principal", command=lambda: self.lobby(frm_principal), width=102, height=2).grid(columnspan=2, row=2)

    def equipe_afficher_equipe(self, frm : Frame, frm_equipe : Frame):
        # Variable qui contient l'équipe du joueur sous forme de liste
        equipe : list[str] = self.save["player"]["team"]
        # On parcourt chaque membre de l'équipe
        for i in range(len(equipe)):
            # Paramètrage du frame qui contiendra la carte du pokémon
            frm_card: Frame = Frame(frm_equipe, background=self.couleur_fond)
            frm_card.grid(column=0, row=i)
            # On stocke la carte dans une liste pour le garbage collector
            self.poke_cards_equipe.append(TeamCard(equipe[i], frm_card, "Retirer"))
            # Affichage de la carte à l'écran
            self.poke_cards_equipe[i].equipe_carte()
            # Paramètrage de la commande du bouton
            self.poke_cards_equipe[i].bouton.bind("<Button-1>", partial(self.equipe_swap_equipe_a_pc, i, frm))
        self.equipe_afficher_equipe_vide(frm, frm_equipe, equipe)


    def equipe_afficher_equipe_vide(self, frm : Frame, frm_equipe : Frame, equipe : list[str]):
        for i in range(len(equipe), 6):
            frm_vide: Frame = Frame(frm_equipe, background=self.couleur_fond)
            frm_vide.grid(column=0, row=len(equipe) + i)
            # On stocke la carte dans une liste pour le garbage collector
            self.poke_cards_equipe.append(TeamCard("25_pikachu", frm_vide, "Retirer"))
            # Affichage de la carte à l'écran
            self.poke_cards_equipe[i].equipe_carte_vide()



    def equipe_afficher_liste(self, frm : Frame, frm_liste : Frame):
        # Variable qui contient la liste des pokémons débloqués par le joueur
        liste : list[str] = self.save["player"]["unlocked_pokemons"]
        # On parcourt chaque membre de l'équipe
        for i in range(len(liste)):
            # Paramètrage du frame qui contiendra la carte du pokémon
            frm_card: Frame = Frame(frm_liste, background=self.couleur_fond)
            frm_card.grid(column=0, row=i)
            # On stocke la carte dans une liste pour le garbage collector
            self.poke_cards_liste.append(TeamCard(liste[i], frm_card, "Ajouter"))
            # Affichage de la carte à l'écran
            #self.poke_cards_liste[i].equipe_carte()
            # Paramètrage de la commande du bouton
            self.poke_cards_liste[i].bouton.bind("<Button-1>", partial(self.equipe_swap_pc_a_equipe, i, frm))

        self.poke_cards_liste_visible = self.poke_cards_liste[
                                        self.poke_cards_liste_index_min: self.poke_cards_liste_index_max]

        for poke_card in self.poke_cards_liste_visible:
            poke_card.equipe_carte()


    def equipe_swap_equipe_a_pc(self,  index : int, frame : Frame, team2Pc=True):
        if len(self.save["player"]["team"]) > 1:
            self.save["player"]["unlocked_pokemons"].append(
                f"{self.poke_cards_equipe[index].dossier.split('_')[0]}_{self.poke_cards_equipe[index].dossier.split('_')[1]}")
            self.poke_cards_liste.append(self.poke_cards_equipe[index])
            self.poke_cards_equipe[index].destroy()
            self.poke_cards_equipe.pop(index)
            self.save["player"]["team"].pop(index)
            self.sauvegarder()
            self.equipe(frame)


    def equipe_swap_pc_a_equipe(self,  index : int, frame : Frame, team2Pc=False):
        if len(self.save["player"]["team"]) < 6:
            self.save["player"]["team"].append(
                f"{self.poke_cards_liste[index].dossier.split('_')[0]}_{self.poke_cards_liste[index].dossier.split('_')[1]}")
            self.poke_cards_equipe.append(self.poke_cards_liste[index])
            self.poke_cards_liste[index].destroy()
            self.poke_cards_liste.pop(index)
            self.save["player"]["unlocked_pokemons"].pop(index)
            self.sauvegarder()
            self.equipe(frame)

    def equipe_changer_page(self, str):
        pass