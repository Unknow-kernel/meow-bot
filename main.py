import requests
import configparser
import telebot
import schedule
import time
import random

# Chargement de la configuration
telegram_info = configparser.RawConfigParser()
telegram_info.read('config.ini')

telegram_bot_token = telegram_info['telegram']['bottoken']

bot = telebot.TeleBot(telegram_bot_token)

# Fonction pour envoyer un message
def telegram_send_message(message, chat_id):
    apiURL = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': chat_id, 'text': message, 'parse_mode': 'html', 'disable_web_page_preview': True})
        print(response.text)
    except Exception as e:
        print(e)

# Fonction pour enregistrer un chat_id dans un fichier texte
def save_chat_id(chat_id):
    with open('chat_ids.txt', 'r') as file:
        chat_ids = file.read().split(',')
        if str(chat_id) not in chat_ids:
            chat_ids.append(str(chat_id))
            with open('chat_ids.txt', 'w') as write_file:
                write_file.write(','.join(chat_ids))
            return True
        else:
            return False

# Fonction pour supprimer un chat_id du fichier texte
def remove_chat_id(chat_id):
    with open('chat_ids.txt', 'r') as file:
        chat_ids = file.read().split(',')
    if str(chat_id) in chat_ids:
        chat_ids.remove(str(chat_id))
    with open('chat_ids.txt', 'w') as file:
        file.write(','.join(chat_ids))

# Commande de start
@bot.message_handler(commands=['start', 'stop'])
def handle_command(message):
    if message.text == '/start':
        chat_id = message.chat.id
        # Ajouter le chat_id au fichier texte s'il n'est pas déjà présent
        if save_chat_id(chat_id):
            welcome_message = "😸 Welcome to Cat Meow Newsletter! We will send you a message every morning to brighten your day :) \n\n /stop to unsubscribe MEEOOOWWW"
        else:
            welcome_message = "You are already subscribed to Cat Meow Newsletter! We will continue sending you messages to brighten your day :)"
        telegram_send_message(welcome_message, chat_id)
    elif message.text == '/stop':
        chat_id = message.chat.id
        # Supprimer le chat_id du fichier texte
        remove_chat_id(chat_id)
        telegram_send_message("You have unsubscribed. We'll miss you 😿", chat_id)

# Fonction pour envoyer des messages à 11h chaque jour
def send_messages():
    with open('letter.txt', 'r') as file:
        messages = file.readlines()
    
    with open('chat_ids.txt', 'r') as file:
        chat_ids = file.read().split(',')
    
    for chat_id in chat_ids:
        # Choisissez un message aléatoire parmi les messages disponibles
        random_message = random.choice(messages)
        
        # Envoyez le message au chat_id
        telegram_send_message(random_message, chat_id)

# Planifie l'envoi de messages à 11h chaque jour
schedule.every().day.at("11:00").do(send_messages)

# Boucle principale du bot
while True:
    schedule.run_pending()
    time.sleep(1)  # Attendez une seconde avant de vérifier à nouveau
