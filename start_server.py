import os
import webbrowser
import subprocess
import time
import sys

def start_server():
    # Lancer le serveur Django dans un sous-processus
    process = subprocess.Popen(["python", "manage.py", "runserver"])

    # Attendez un peu pour que le serveur se lance avant d'ouvrir le navigateur
    time.sleep(2)

    # Ouvre le navigateur sur l'URL par défaut
    webbrowser.open("http://127.0.0.1:8000")

    # Attendre que le serveur se termine
    process.wait()

    # Ferme la fenêtre de commande après l'exécution du processus (force la sortie)
    os._exit(0)

# Appeler la fonction pour démarrer le serveur
start_server()
