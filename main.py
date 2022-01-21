from pokemon import Pokemon
from move import Attaque
from network import Network
from application import Application


def main():
    test = Pokemon(1, 1, "bulbasaur", "default")
    move_test = Attaque('absorb')
    app = Application(1280, 720)
    app.client()



if __name__ == "__main__":
    main()

