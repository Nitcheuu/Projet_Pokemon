import requests
from bs4 import BeautifulSoup
import json
import os
from threading import Thread


def get_abilities(debut : int, fin : int):
    dir = "data/abilities/"
    for i in range(debut, fin):
        url = f"https://pokeapi.co/api/v2/ability/{i}"
        reponse = requests.get(url)
        if reponse.ok:
            donnees = BeautifulSoup(reponse.text, 'html.parser')
            abilitie = json.loads(donnees.text)
            with open(dir + f"{abilitie['name']}.json", "w", encoding="utf-8") as f:
                f.write(str(abilitie))
        else:
            print("Erreur lors de la connexion à l'API")


def get_pokemons(debut : int, fin : int, generation : int):
    parent_dir = "data/pokemons/"
    path = os.path.join(parent_dir, f"{generation}G")
    os.mkdir(path)
    for i in range(debut, fin):
        url = f"https://pokeapi.co/api/v2/pokemon/{i}/"
        reponse = requests.get(url)
        if reponse.ok:
            donnees = BeautifulSoup(reponse.text, 'html.parser')
            pokemon = json.loads(donnees.text)
            pokemon_path = path + f"/{i}_{pokemon['forms'][0]['name']}"
            os.mkdir(pokemon_path)
            with open(pokemon_path + "/data.json", "w") as f:
                f.write(str(pokemon).replace("'", '"').replace("None", '"None"').replace("False", 'false').replace("True", "true"))
            for pos in pokemon["sprites"]["versions"]["generation-iv"]["heartgold-soulsilver"].keys():
                pic_url = pokemon["sprites"]["versions"]["generation-iv"]["heartgold-soulsilver"][pos]
                if pic_url is not None:
                    with open(pokemon_path + f'/{pos}.png', 'wb') as handle:
                        response = requests.get(pic_url, stream=True)
                        if not response.ok:
                            print(response)
                        for block in response.iter_content(1024):
                            if not block:
                                break
                            handle.write(block)
        else:
            print("Erreur lors de la connexion avec l'API")
            return


def get_moves(debut : int, fin : int):
    dir = "data/moves/"
    for i in range(debut, fin):
        url = f"https://pokeapi.co/api/v2/move/{i}/"
        reponse = requests.get(url)
        if reponse.ok:
            donnees = BeautifulSoup(reponse.text, 'html.parser')
            move = json.loads(donnees.text)
            json.encoder.JSONEncoder()
            with open(dir + f"{move['name']}.json", "w", encoding="utf-8") as f:
                json.dump(move, f)
        else:
            print("Erreur lors de la connexion à l'API")


def main():
    threads = []
    threads.append(Thread(target=get_moves, args=(1, 201,)))
    threads.append(Thread(target=get_moves, args=(201, 401,)))
    threads.append(Thread(target=get_moves, args=(401, 601,)))
    threads.append(Thread(target=get_moves, args=(601, 827,)))

    for thread in threads:
        print("Début du thread")
        thread.start()


    for thread in threads:
        thread.join()

    print("Fin du programme")





if __name__ == "__main__":
    main()
