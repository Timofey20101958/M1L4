import telebot 
from config import token
from random import randint
from logic import Pokemon
from logic import Wizard, Fighter


bot = telebot.TeleBot(token) 

# @bot.message_handler(commands=['go'])
# def go(message):
#     if message.from_user.username not in Pokemon.pokemons.keys():
#         pokemon = Pokemon(message.from_user.username)
#         bot.send_message(message.chat.id, pokemon.info())
#         bot.send_photo(message.chat.id, pokemon.show_img())
#     else:
#         bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['go'])
def start(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        chance = randint(1,3)
        if chance == 1:
            pokemon = Pokemon(message.from_user.username)
        elif chance == 2:
            pokemon = Wizard(message.from_user.username)
        elif chance == 3:
            pokemon = Fighter(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

    pokemon_count = get_pokemon_count(username)
    if pokemon_count >= 3:
        bot.reply_to(message, "У тебя уже есть 3 покемона! Используй /pokemons для просмотра.")
        return
    pokemon_number = None
    if len(message.text.split()) > 1:
        try:
            pokemon_number = int(message.text.split()[1])
            if pokemon_number < 1 or pokemon_number > 150:
                bot.reply_to(message, "Выбери номер покемона от 1 до 150!")
                return
        except ValueError:
            bot.reply_to(message, "Используй: /go <номер>")

# @bot.message_handler(commands=['feed'])
# def feed(message):
#     if message.from_user.username in Pokemon.pokemons.keys():
#         pokemon = Pokemon.pokemons[message.from_user.username]
#         result = pokemon.feed()
#         bot.send_message(message.chat.id, result)
#     else:
#         bot.reply_to(message, "Сначала создай покемона с помощью команды /go")

@bot.message_handler(commands=['feed'])
def feed_pok(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        res = pok.feed()
        bot.send_message(message.chat.id, res)
    else:
        bot.send_message(message.chat.id, "Нельзя кормить покемона, которого нет")

@bot.message_handler(commands=['attack'])
def attack_pok(message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.username in Pokemon.pokemons.keys() and message.from_user.username in Pokemon.pokemons.keys():
            enemy = Pokemon.pokemons[message.reply_to_message.from_user.username]
            pok = Pokemon.pokemons[message.from_user.username]
            res = pok.attack(enemy)
            bot.send_message(message.chat.id, res)
        else:
            bot.send_message(message.chat.id, "Сражаться можно только с покемонами")
    else:
        bot.send_message(message.chat.id, "Чтобы атаковать, нужно ответить на сообщения того, кого хочешь атаковать")

@bot.message_handler(commands=['info'])
def handle_info(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        
        info_text = (
            f"🧬 Информация о вашем покемоне:\n\n"
            f"Имя: {pok.name}\n"
            f"Уровень: {pok.level}\n"
            f"Здоровье: {pok.hp}\n"
            f"Атака: {pok.power}\n"
        )
        bot.send_message(message.chat.id, info_text)
    else:
        bot.send_message(
            message.chat.id,
            "У вас пока нет покемона! Используйте /go, чтобы поймать своего первого покемона."
        )

bot.infinity_polling(none_stop=True)

