Afin de créer l'environnement adéquate il vous faudra :

Tapez dans votre console Git Bash : git clone https://github.com/FraPar/OC-4-chest-tournament-app
Tapez dans votre console à l'emplacement que vous avez choisi pour votre dossier : "python -m venv env"
Exécutez depuis la console : "env/Scripts/activate.bat" (sous Windows) ou "source env/bin/activate"
Installez l'ensemble des modules : "pip install -r requirements.txt"
Vous êtes maintenant en mesure de lancer l'application :

Tapez dans votre console :
"python __main__.py".

Manuel d'instruction:
Une fois dans le menu d'accueil, vous pourrez naviguer dedans en tapant le numéro correspondant à votre
choix.
Par exemple, pour créer un nouveau tournoi, vous taperez la numéro "1" dans la console et appuierez
sur votre touche entrée.Il vous sera ensuite demandé de saisir les informations du tournoi, vous procéderez
de la même manière que précédement : une fois que votre saisie est correcte, vous appuyez sur entrée pour
valider votre choix.
Il vous sera ensuite demandé d'ajouter les 8 joueurs du tournoi. En tappant "1" dans la console, vous pourrez
choisir un joueur déjà éxistant. En tappant "2", vous créerez un nouveau joueur. En tappant "3", un joueur
sera crée automatiquement si vous souhaitez tester l'application.
Une fois les 8 joueurs renseignés, les matchs peuvent commencer. Le système de tournoi Suisse est utilisé
ici, le joueur 1 sera celui le mieux classé, le joueur 8 le moins bien classé. Saisissez alors le numéro du
gagnant de chaque matchs ou le "0" en cas d'égalité. Si le joueur 1 rencontre le joueur 5 et gagne son tout
premier match, le joueur 1 gagnera alors 1 point, là ou le joueur 5 restera à 0. Les scores sont cumulés
tout au long du tournoi.
Un rapport peut être généré à partir du menu d'accueil de l'application, vous pourrez retrouver le numéro
correspondant à chaque joueur avec une ID propre à chacun.


Si vous souhaitez générer un nouveau rapport Flake8-html, tapez dans votre console :
"flake8 --exclude env --max-line-length 120 --format=html --htmldir=flake-report"

Merci d'avoir utilisé mon application.

Made by François Parenti.