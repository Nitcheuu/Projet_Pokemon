import socket
from _thread import *
import pickle
from game import Game


# Pour le client : si il est le joueur 1 ou 2 (currentPlayer) et dans quelle partie (gameID)
def threaded_client(conn, currentPlayer, gameID):
    global idCount
    # envoyer au network l'ID du joueur (0 ou 1)
    print("Nouvelle connexion")
    conn.send(str.encode(str(currentPlayer)))
    data = None
    while True:
        try:
            try:
                data = conn.recv(4096*8).decode()
            except:
                pass
            if gameID in games:
                game = games[gameID]
                if not data:
                    break
                """if data == "point":
                    game.point = True
                if data == "reset":
                    print("reset de la partie")
                    game.reset()
                if data == "finpoint":
                    game.point = False
                if "SendPosition" in data:
                    position = data.split("_")
                    game.players_positions[currentPlayer] = float(position[1])
                if "Ball" in data:
                    data_ball = data.split("_")
                    game.ball_position = [float(data_ball[1]), float(data_ball[2])]
                    game.ball_direction_x = float(data_ball[3])
                    game.ball_direction_z = float(data_ball[4])
                    game.ball_old_position.append([float(data_ball[1]), float(data_ball[2])])
                    if len(game.ball_old_position) > 100:
                        game.ball_old_position = game.ball_old_position[-15:-1]
                if "Score" in data:
                    score = data.split("_")
                    game.score = [int(score[1]), int(score[2])]
                if "PlayerConfiguration" in data:
                    player_data = data.split("#")
                    player_color = player_data[1].split("/")
                    game.players_colors[currentPlayer] = [float(player_color[0]), float(player_color[1]), float(player_color[2]), float(player_color[3])]
                    game.players_textures[currentPlayer] = player_data[2]
                    game.players_pseudo[currentPlayer] = player_data[3]
                    game.players_ready[currentPlayer] = True"""


                reply = pickle.dumps(game)
                conn.sendall(reply)

            else:
                pass
        except:
            break

    print("Connexion perdue\nFermeture du jeu")
    try:
        del games[gameID]
    except:
        pass
    idCount -= 1
    conn.close()


# Définition du serveur et du port
server = "192.168.43.94"
port = 5555
# Définition du socket
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Paramaètrage du socket
try:
    # Le paramètrage peut échouer
    soc.bind((server, port))
except socket.error as e:
    # Si c'est le cas on affiche le message d'erreur
    print(str(e))

# Attente d'une connexion
soc.listen()
print("Serveur statut : OK\nEn attente d'une connexion ...")

connected = set()
games = {}
idCount = 0
while True:
    # établissement de la connexion avec le joueur
    conn, addr = soc.accept()
    print(f"Connecté à : {addr[0]}")
    idCount += 1
    player = 0
    gameID = (idCount - 1) // 2

    if idCount % 2 == 1:
        games[gameID] = Game(gameID)
        print(f"Création de la partie {gameID}")
    else:
        games[gameID].pret = True
        print("Partie prête")
        player = 1

    start_new_thread(threaded_client, (conn, player, gameID))
