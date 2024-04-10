import requests
import os
import sys
import configparser
import random  # Ajout du module random
from telebot import types
import telebot

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

# Fonction pour lire les messages du fichier "letter.txt" et en choisir un au hasard
def get_random_message():
    with open('letter.txt', 'r') as file:
        messages = file.read().strip().split('\n')
    return random.choice(messages)

# Commande de start
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    # Ajouter le chat_id au fichier texte s'il n'est pas déjà présent
    if save_chat_id(chat_id):
        welcome_message = "😸 Welcome to Cat Meow Newsletter! We will send you a message every morning to brighten your day :)\n\nTo unsubscribe, use the /stop command. MEEOOOWWW"
    else:
        welcome_message = "You are already subscribed to Cat Meow Newsletter! We will continue sending you messages to brighten your day :)"
    telegram_send_message(welcome_message, chat_id)

# Commande de stop
@bot.message_handler(commands=['stop'])
def handle_stop(message):
    chat_id = message.chat.id
    # Supprimer le chat_id du fichier texte
    remove_chat_id(chat_id)
    telegram_send_message("You have unsubscribed from Cat Meow Newsletter. We'll miss you 😿", chat_id)

# Commande pour envoyer un message aléatoire
@bot.message_handler(commands=['send_random'])
def send_random_message(message):
    with open('chat_ids.txt', 'r') as file:
        chat_ids = file.read().split(',')
    for chat_id in chat_ids:
        random_message = get_random_message()
        telegram_send_message(random_message, chat_id)

bot.polling()

