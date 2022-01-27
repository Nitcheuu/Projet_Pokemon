import json


class Pokemon:
    def __init__(self, id : int, generation : int, nom : str, sprite : str, genre : str = None):
        self.id : int = id # ID du pokémon dans le pokédex
        self.generation : str = f"{generation}G" # Génération à laquelle le pokémon apparatient
        self.nom : str = nom # Nom du pokémon
        # Chemin du dossier qui contient les informations du pokémon
        self.dossier : str = f"data/pokemons/{self.id}_{self.nom}/"
        # Lecture du fichier json qui contient les données du pokémon
        with open(self.dossier + "data.json", "r") as pokemon_data:
            self.data = json.load(pokemon_data)
        # définition du genre du pokémon
        self.genre : str = genre
        # Liste des talents du pokémon
        self.talents : list[dict] = self.data["abilities"]
        # Stat d'expérience de base du pokémon
        self.experience : int = self.data["base_experience"]
        # Taille du pokémon
        self.taille : int = self.data["height"]
        # Poids du pokémon
        self.poids : int = self.data["weight"]
        # Capacités que le pokémon peut apprendre
        self.attaques : list[dict] = []
        # Remplissage de la liste
        for i in range(len(self.data["moves"])):
            self.attaques.append(self.data["moves"][i]["move"])
        # Statistiques du pokémon
        self.stats : list[int] = []
        # Remplissage de la liste
        for i in range(len(self.data["stats"])):
            self.stats.append(self.data["stats"][i]["base_stat"])
        # Type(s) du pokémon
        self.types : list[dict] = self.data["types"]
        # Sprites du pokémon
        self.sprites : list[str] = [
            self.dossier + f"back_{sprite}.png",
            self.dossier + f"front_{sprite}.png"
        ]


    def __str__(self):
        return "Pokemon{" + \
               "generation="+self.generation+";"+\
               "nom="+self.nom+"}"