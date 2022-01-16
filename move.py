import json



class Attaque:
    def __init__(self, nom : str):
        # Nom de l'attaque en anglais
        self.nom_en : str = nom
        # Chargement des données de l'attaque
        with open(f"data/moves/{self.nom_en}.json", "r") as move_data:
            self.data = json.load(move_data)
        # Récupération de l'id
        self.id: int = self.data["id"]
        # Précision de l'attaque [[0;100]] ou None si elle n'échoue jamais
        self.precision : int = self.data["accuracy"]
        # Classe : Physique , spéciale, status, etc.
        self.classe : str = self.data["damage_class"]["name"]
        # Description de l'attaque en anglais
        self.description_en : str = self.data["effect_entries"][0]["effect"]
        # PP : Nombre de fois où le pokémon peut utiliser la capacité en 1 combat
        self.pp = self.data["pp"]
        # Priorité de l'attaque 0 1 ou 2
        self.priorite = self.data["priority"]
        # Cible de l'attaque (le joueur ou l'ennemi)
        self.cible = self.data["target"]["name"]
        # Type de l'attaque
        self.type = self.data["type"]["name"]

