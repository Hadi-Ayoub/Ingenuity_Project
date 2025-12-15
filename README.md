Branche principale: main

# Projet

Contient les exécutables Godot (Windows et Linux), ainsi que le code source de la partie du projet réalisée avec Godot.

Contient le script .py de l'agent Python et le script ingescape.

<img width="3341" height="1380" alt="Capture d&#39;écran 2025-12-15 010705" src="https://github.com/user-attachments/assets/76e3e902-63cf-4fa1-ab9c-556cf7a35bae" />



On a réalisé les fondations d'un dungeon crawler en 3D, en utilisant Godot comme outil supplémentaire.

Le joueur peut se déplacer dans un donjon généré de manière aléatoire, il cherche le but. 

Lorsqu'il l'atteint, un message est affiché dans le chat du Whiteboard, et lorsqu'il explore des cases, celle-ci sont dessinées sur le Whiteboard pour former une carte.

En se basant sur une bibliothèque déjà existante, on a ensuite randomisé la génération de carte, ajouté un but visible sur la carte en 3D, qui est placé le plus loin possible.
De Godot, on a également transmis les coordonnées des cases visitées et indiquer quand le joueur atteint l'objectif à un agent Python (main.py) via TCP.

Il nous a par ailleurs fallu réassigner les commandes (avance, recule, droite et gauche, tourner la caméra à gauche, tourner la caméra à droite), car les commandes étaient pour un clavier QWERTY.

Afin de limiter la dépendance au type de clavier, on a deux dispositions de touches:

Flèches directionnelles: 
- Flèche du Haut: Avancer
- Flèche du Bas: Reculer
- Flèche de Droite: Tourner la caméra à droite
- Flèche de Gauche: Tourner la caméra à gauche

ZQSD:
- Z: Avancer
- S: Reculer
- Q: Pas de côté à gauche
- D: Pas de côté à droite
- E: Tourne la caméra à droite
- A: Tourne la caméra à gauche

# Pré requis
- Python 3.10
- Ingescape Circle
- Whiteboard
- La bibliothèque Python pour ingescape>=4 (se trouve dans requirements.txt)

# Fonctionnement


- Lancer pip install -r "requirements.txt"
- Lancer le script ingescape ingenuity.igssystem
- Connecter ingescape circle à une interface réseau valide avec un numéro de port valide
- Lancer le Whiteboard
- Connecter le Whiteboard à la même interface réseau avec le même numéro de port que ingescape circle
- Lancer le script Python main.py avec comme paramètres \<NomAgent\> \<AdresseIP\> \<Port\>.  
  Pour obtenir l'adresse IP, on peut réaliser un ipconfig (pour Windows) ou ip a (pour Linux) et sélectionner l'adresse IP correspondant à l'interface réseau utilisée.
- Lancer l'exécutable 3D_Dungeon_RPG.exe (jeu/executables) si l'ordinateur est sous Windows ou 3D_Dungeon_RPG.sh (jeu/executables) si l'ordinateur est sous Linux
- Sélectionner la fenêtre Godot ouverte comme fenêtre active, vous pouvez à présent vous déplacer pour trouver l'objectif

# Pour aller plus loin
On a pensé à ajouter des coffres aux trésors et à ce que une fois ouvert le contenu s'affiche dans le chat du Whiteboard. 

On a aussi envisagé un système de combat au tour par tour.

Enfin, on a également considéré de passer à un autre niveau une fois l'objectif atteint.

# Difficultés rencontrées
Au début du projet, on a utilisé une bibliothèque différente pour générer le donjon, car celle-ci s'occupait déjà de la génération aléatoire.

Cependant, lorsqu'on a voulu placer le but, on s'est rendu compte que la génération aléatoire générait des pièces qui n'étaient pas nécessairement connectées entre elles.

Ainsi, il était possible que le but soit inatteignable par le joueur.

Choisir un but pour avoir un chemin valide s'est avéré impossible, car le spawn du joueur était choisi dans une liste de points de spawns de manière aléatoire.

Même en tentant de choisir le point de départ correspondant au spawn du joueur et ensuite d'aller chercher la pièce la plus loin de ce point de départ, nous n'avons pas réussi. 

Le but n'était simplement pas atteignable, nous avions le nom de la node dans lequel le but se trouvait, mais aucune idée d'où se trouvait la dite node, que nous n'arrivons jamais à trouver, même en explorant.

Il semble donc que le but était en dehors de la partie du donjon qui était atteignable par joueur, ce qui nous a poussé à changer de bibliothèque.

Aussi, nous n'avons pas pu rendre le port TCP modulaire, car nous ne savons pas comment faire dans Godot, car nous avons utilisé Godot pour la première fois dans le cadre de ce projet.

Enfin Ingescape Circle ne marchait pas avec le réseau privé de l'un de nous deux, pour contourner ce problème, on a dû utilisé un partage de connexion.

Même ainsi, ingescape.start_with_device n'arrivait pas à se connecter à l'interface utilisée par circle, ainsi on a passé directement l'adresse IP pour ingescape.start_with_ip. 


# Remerciments
3d-dungeon-godot-4: https://github.com/NyanPanDev/3d-dungeon-godot-4.git

Qui est elle-même un Fork de https://github.com/uheartbeast/3d-dungeon
