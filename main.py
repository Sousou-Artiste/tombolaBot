import discord
from discord.ext import commands
import asyncio
from datetime import datetime
import random
import json
import os
from dotenv import load_dotenv

# Charger le token depuis un fichier .env (à créer)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # Le token doit être dans un fichier .env (par exemple DISCORD_TOKEN=ton_token)

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="ny!", intents=intents)

COOLDOWN = 600  # 10 minutes en secondes

# Chemin du dossier où sont stockées les données de chaque serveur
DATA_DIR = "data"

# Assurez-vous que le dossier 'data' existe
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Fonction pour charger les données de la tombola pour un serveur
def load_data(guild_id):
    file_path = f"data/{guild_id}.json"  # Crée un fichier JSON spécifique pour chaque serveur
    if not os.path.exists(file_path):
        print(f"Aucune donnée trouvée pour {guild_id}.")
        return None
    
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            # Vérification de la structure attendue
            if "tombola" not in data:
                print(f"Données de tombola manquantes pour {guild_id}.")
                return None
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erreur lors du chargement des données pour {guild_id}: {e}")
        return None

# Fonction pour sauvegarder les données pour un serveur spécifique
def save_data(guild_id, tombola_data):
    file_path = f"data/{guild_id}.json"  # Crée un fichier JSON spécifique pour chaque serveur
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Crée le répertoire si nécessaire
    try:
        with open(file_path, "w") as f:
            json.dump(tombola_data, f, indent=4)  # Utilisation de 'indent' pour rendre le JSON plus lisible
        print(f"Données de la tombola pour le serveur {guild_id} sauvegardées avec succès.")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données pour le serveur {guild_id}: {e}")

# Chargement des données au démarrage du bot
@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')

# Commande pour lancer la tombola
@bot.command()
@commands.has_permissions(administrator=True)
async def launch(ctx, date_str: str = None, winners: int = None, *, prize_list: str = None):
    if not date_str or not winners or not prize_list:
        await ctx.send("⚠️ Utilisation correcte: !launch JJ/MM/AAAA [Nombre Gagnants] [lot1;lot2;lot3;...]")
        return
    
    try:
        guild_id = str(ctx.guild.id)
        # Le format de la date doit maintenant correspondre à la date de fin
        end_time = datetime.strptime(date_str + " 20:00", "%d/%m/%Y %H:%M")
        
        tombola_data = load_data(guild_id) or {}  # Charge les données ou crée un dict vide
        tombola_data["tombola"] = {
            "end_time": end_time.strftime("%d/%m/%Y %H:%M"),  # On enregistre la date de fin
            "num_winners": max(1, winners),
            "prizes": prize_list.split(";"),
            "tombola_usage": {},
            "launch_channel": ctx.channel.id,
            "active": True  # La tombola commence active
        }
        
        save_data(guild_id, tombola_data)
        
        await ctx.send(f"📅 Tombola lancée, elle se termine le {end_time.strftime('%d/%m/%Y à %H:%M')} avec {winners} gagnant(s) et {len(prize_list.split(';'))} lot(s) !")
    except ValueError:
        await ctx.send("⚠️ Format de commande invalide. Utilisation correcte: !launch JJ/MM/AAAA [Nombre Gagnants] [lot1;lot2;lot3;...]")

@bot.command()
async def tombola(ctx, nom_rp: str = None):
    # Vérification si le nom du personnage RP a été fourni
    if not nom_rp:
        await ctx.send("⚠️ Utilisation correcte: !tombola [Nom du personnage RP]")
        return
    
    guild_id = str(ctx.guild.id)
    tombola_data = load_data(guild_id)

    # Vérification si les données de tombola existent pour ce serveur
    if not tombola_data or "tombola" not in tombola_data:
        await ctx.send("⏳ Aucune tombola trouvée pour ce serveur !")
        return
    
    tombola_info = tombola_data["tombola"]

    # Vérification de l'activation de la tombola
    if not tombola_info.get("active", False):
        await ctx.send("⏳ La tombola n'est pas active sur ce serveur !")
        return
    
    # Vérification de la date de fin de la tombola
    now = datetime.now()
    end_time = datetime.strptime(tombola_info["end_time"], "%d/%m/%Y %H:%M")
    
    if now > end_time:
        tombola_info["active"] = False  # Désactive la tombola si la date de fin est passée
        tombola_data["tombola"] = tombola_info
        save_data(guild_id, tombola_data)
        await ctx.send(f"⏳ La tombola est terminée ! Elle s'est terminée le {end_time.strftime('%d/%m/%Y à %H:%M')}.")
        return

    # Gestion du cooldown pour le personnage RP
    tombola_usage = tombola_info.get("tombola_usage", {})
    now_ts = asyncio.get_event_loop().time()

    if nom_rp in tombola_usage:
        last_used = tombola_usage[nom_rp]["last_used"]
        if now_ts - last_used < COOLDOWN:
            time_left = COOLDOWN - (now_ts - last_used)
            await ctx.send(f"⏳ Le personnage '{nom_rp}' doit attendre encore {int(time_left)} secondes avant de rejouer !")
            return
    
    # Enregistrement de la participation
    tombola_usage[nom_rp] = {"last_used": now_ts, "count": tombola_usage.get(nom_rp, {}).get("count", 0) + 1}
    tombola_info["tombola_usage"] = tombola_usage
    tombola_data["tombola"] = tombola_info
    save_data(guild_id, tombola_data)

    # Confirmation de la participation
    await ctx.send(f"🎟️ {nom_rp} participe à la tombola ! Bonne chance !")

@bot.command()
@commands.has_permissions(administrator=True)
async def liste(ctx):
    guild_id = str(ctx.guild.id)  # Utilisation du guild_id actuel
    tombola_data = load_data(guild_id)
    
    if not tombola_data or "tombola" not in tombola_data or not tombola_data["tombola"].get("tombola_usage"):
        await ctx.send("📜 Aucun participant encore enregistré pour cette tombola.")
        return
    
    tombola_usage = tombola_data["tombola"]["tombola_usage"]  # Accéder à tombola_usage
    if not tombola_usage:
        await ctx.send("📜 Aucun participant n'a encore participé à cette tombola.")
        return
    
    # Tri des participants en fonction du nombre de participations
    sorted_list = sorted(tombola_usage.items(), key=lambda x: x[1]['count'], reverse=True)
    
    # Paramètres de pagination
    participants_per_page = 10
    num_pages = (len(sorted_list) // participants_per_page) + (1 if len(sorted_list) % participants_per_page > 0 else 0)
    
    # Création d'une fonction pour envoyer une page d'embed
    def create_embed(page):
        start = page * participants_per_page
        end = start + participants_per_page
        page_participants = sorted_list[start:end]
        
        embed = discord.Embed(title="📜 Top des participants à la tombola", description="Liste des participants avec le plus de tickets.", color=discord.Color.blue())
        
        for i, (nom, data) in enumerate(page_participants, start=1 + start):
            embed.add_field(name=f"{i}. {nom}", value=f"Tickets : {data['count']}", inline=False)
        
        embed.set_footer(text=f"Page {page + 1} sur {num_pages}")
        return embed
    
    # Envoi de la première page
    current_page = 0
    embed_message = await ctx.send(embed=create_embed(current_page))
    
    # Ajout des réactions pour la navigation
    if num_pages > 1:
        await embed_message.add_reaction("⬅️")  # Flèche gauche pour la page précédente
        await embed_message.add_reaction("➡️")  # Flèche droite pour la page suivante

    # Fonction pour gérer les réactions de navigation
    def check(reaction, user):
        return user != bot.user and str(reaction.emoji) in ["⬅️", "➡️"] and reaction.message.id == embed_message.id

    # Navigation entre les pages
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == "⬅️" and current_page > 0:
                current_page -= 1
                await embed_message.edit(embed=create_embed(current_page))
                await embed_message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "➡️" and current_page < num_pages - 1:
                current_page += 1
                await embed_message.edit(embed=create_embed(current_page))
                await embed_message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            break  # Arrêt de la navigation après 60 secondes sans réaction

# Commande pour faire le tirage de la tombola
@bot.command()
@commands.has_permissions(administrator=True)
async def tirage(ctx):
    guild_id = str(ctx.guild.id)
    tombola_data = load_data(guild_id)
    
    # Vérification si la tombola est active
    if not tombola_data or not tombola_data.get("tombola") or not tombola_data["tombola"].get("active", False):
        await ctx.send("⏳ Aucune tombola active à tirer sur ce serveur !")
        return
    
    tombola_info = tombola_data["tombola"]
    participants = list(tombola_info["tombola_usage"].keys())  # Liste des participants
    num_winners = tombola_info["num_winners"]  # Nombre de gagnants
    prizes = tombola_info["prizes"]  # Liste des lots disponibles
    
    # Vérification s'il y a des participants
    if not participants:
        await ctx.send("🎟️ Aucun participant n'a été enregistré pour cette tombola.")
        return
    
    # Choix des gagnants
    winners = random.sample(participants, min(num_winners, len(participants)))  # Tirage au sort des gagnants
    result_message = "🎉 **Résultats de la tombola !** 🎉\n"
    
    # Attribuer les lots aux gagnants
    for i, winner in enumerate(winners):
        prize = prizes[i] if i < len(prizes) else "aucun lot disponible"  # Si pas de lot, aucun lot
        result_message += f"🏆 {winner} remporte : {prize}\n"
    
    # Envoi des résultats dans le canal de lancement
    launch_channel = bot.get_channel(tombola_info["launch_channel"])
    if launch_channel:
        await launch_channel.send(result_message)
    else:
        await ctx.send(result_message)
    
    # Désactiver la tombola après le tirage
    tombola_info["active"] = False
    tombola_data["tombola"] = tombola_info
    save_data(guild_id, tombola_data)  # Sauvegarder les données de la tombola

bot.run(TOKEN)
