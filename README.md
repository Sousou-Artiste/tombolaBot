# Tombola RP Discord Bot

Ce bot a été conçu pour gérer des tombolas sur des serveurs Discord, principalement dans des contextes de jeux de rôle (RP). Il permet d'organiser et de gérer des tombolas, où les participants peuvent s'inscrire et participer à des tirages au sort pour remporter des lots. Le bot permet également de suivre les participations, de réaliser des tirages, et de gérer la distribution des récompenses.

## Fonctionnalités principales

- **Lancer une tombola** : Un administrateur peut configurer et lancer une tombola avec une date de fin, un nombre de gagnants et des lots à attribuer.
- **Participer à la tombola** : Les utilisateurs peuvent s'inscrire à la tombola en inscrivant leur nom RP.
- **Afficher les participants** : Les administrateurs peuvent afficher la liste des participants et leur nombre de tickets.
- **Tirage au sort** : Les administrateurs peuvent effectuer un tirage pour déterminer les gagnants de la tombola.
- **Pagination avec réactions** : Affichage des participants de manière paginée avec des réactions pour naviguer entre les pages des résultats.

## Installation et Prérequis

### Prérequis

- **Python 3.8+** : Ce bot utilise Python, donc assurez-vous que vous avez installé une version compatible.
- **Bibliothèques Python** :
  - `discord.py` : Pour interagir avec l'API de Discord.
  - `python-dotenv` : Pour charger les variables d'environnement depuis un fichier `.env`.
  - `json` : Pour gérer les données de la tombola (les fichiers `.json`).
  - `asyncio` : Pour gérer l'asynchrone dans le bot.

### Étapes d'installation

1. **Clonez le dépôt ou téléchargez les fichiers** :
   - Clonez ce dépôt GitHub ou téléchargez les fichiers du bot sur votre machine.

2. **Installez les dépendances** :
   - Créez un environnement virtuel :
     ```bash
     python -m venv venv
     ```
   - Activez l'environnement virtuel :
     - Sur Windows : `venv\Scripts\activate`
     - Sur macOS/Linux : `source venv/bin/activate`
   - Installez les dépendances :
     ```bash
     pip install -r requirements.txt
     ```

3. **Créer le fichier `.env`** :
   - Dans le répertoire du projet, créez un fichier `.env` et ajoutez la ligne suivante avec votre token Discord :
     ```plaintext
     DISCORD_TOKEN=VOTRE_TOKEN_DISCORD
     ```

4. **Lancer le bot** :
   - Après avoir configuré le fichier `.env`, vous pouvez démarrer le bot avec la commande suivante :
     ```bash
     python bot.py
     ```

## Utilisation du bot

### Commandes principales

- **!launch JJ/MM/AAAA [Nombre Gagnants] [lot1;lot2;lot3;...]** : Lance une tombola. Cette commande crée une tombola avec une date de fin et un nombre de gagnants. Les lots sont séparés par des points-virgules.
- **!tombola [Nom du personnage RP]** : Permet à un utilisateur de participer à la tombola en inscrivant son nom RP. Chaque utilisateur peut participer un certain nombre de fois selon les règles définies par l'administrateur.
- **!liste** : Affiche la liste des participants à la tombola avec le nombre de tickets. Les administrateurs peuvent naviguer entre les pages des résultats avec des réactions.
- **!tirage** : Réalise le tirage au sort pour désigner les gagnants. Les gagnants reçoivent les lots de manière aléatoire.

### Responsabilités et Modifications

Ce bot a été développé par **Sousou Artiste** (créateur du code). Le bot peut être utilisé et modifié par les administrateurs des serveurs qui l'installent. Cependant, **toute modification du code ou adaptation spécifique au serveur ne relève pas de ma responsabilité**, et je décline toute responsabilité liée à l'utilisation du bot après modification.

**Auteur du code : Sousou Artiste**

**Licence** : Ce bot est sous **licence libre**. Vous pouvez l'utiliser et le modifier selon vos besoins, mais vous devez mentionner **Sousou Artiste** comme auteur du code, même en cas de modifications.

### Disclaimer

Le bot est fourni **"tel quel"** sans garantie d'aucune sorte. Je ne suis pas responsable des éventuels bugs, dysfonctionnements ou autres problèmes pouvant survenir lors de l'utilisation ou après modification du code.

---

Merci d'avoir choisi ce bot pour gérer vos tombolas RP ! Amusez-vous bien et bonne chance à tous les participants !
