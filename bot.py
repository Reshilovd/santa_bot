import requests
import random
import telebot
from auth_data import token
participants_list = ['Денис','Дима','Максим','Даша','Саня']
defaultAvatars = {
    'Денис':'https://www.instagram.com/p/CL6lEVjHGyk/',
    'Дима':'https://www.instagram.com/p/BiFZIQ5nHYv/',
    'Максим':'https://www.instagram.com/p/B1Jp79sB5QX/',
    'Даша':'https://www.instagram.com/p/BnoxtIQl5yg/',
    'Саня':'https://www.instagram.com/p/CJdUwYxhruO/'
}
list_santa = []
user_list = {}

users = {}

def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_photo(message.chat.id,'https://1.bp.blogspot.com/-qjqIsAS4SOM/X9DRolbC72I/AAAAAAABAqo/NbbazgUKPGUbiwfmjyQ445K7zwWe0UQrgCLcBGAsYHQ/s2048/santa-%25D0%25B4%25D0%25B5%25D0%25B4%2B%25D0%25BC%25D0%25BE%25D1%2580%25D0%25BE%25D0%25B7-DoV%2B%25281%2529.png')
        bot.send_message(message.chat.id,'Привет человек! Как ты мог заметить приближается уже 2022-й год, \
и поэтому выбирать санту по бумажке из шапки уже не модно! Я создан хорошим человеком специально \
для того, чтобы помочь тебе найти и сделать счастливым своего Санту!')
        bot.send_message(message.chat.id, 'Если хочешь участвовать назови свое имя:')

    @bot.message_handler(commands=["santa"])
    def send_text(message):
        uid = message.from_user.id
        user = users[uid]
        print(user)
        child = user['child']

        if child != '':
            bot.send_message(message.chat.id,'Ты что забыл?')
            bot.send_photo( message.chat.id, users[ user['child'] ]['avatar'] )
        else:
            tmpUsers = users.copy()
            del tmpUsers[uid]
            print(users)
            print(tmpUsers)
            key = random.choice(list(tmpUsers.keys()))
            print(key)
            users[uid]['child'] = key

            bot.send_photo(message.chat.id, users[key]['avatar'])
            bot.send_message(message.chat.id, 'Узнаешь этого человека? Поздравляю, ты его Санта! (Если не узнал набери /who_is_it и я подскажу!')

    @bot.message_handler(commands=["who_is_it"])
    def send_text(message):
        user = users[ message.from_user.id ]
        name = users[ user['child'] ]['name']
        bot.send_message(message.chat.id,f"Ты точно из этой компании!? Это же {name}!")

    @bot.message_handler(content_types=['text'])
    def add_user(message):
        uid = message.from_user.id
        name = message.text

        if uid in users:
            bot.send_message(message.chat.id, 'Я уже знаю как тебя зовут')
        else:

            # user_list[name] = message.from_user.id
            # list_santa.append(name)
            if name in defaultAvatars:
                avatar = defaultAvatars[name]
            else:
                avatar = 'NoIMG'

            users[uid] = {'name': name, 'child': '', 'avatar': avatar}

            bot.send_message(message.chat.id,
                             f"Привет {name}! Добавил тебя в список участников. {users}")

    bot.polling()

if __name__ == '__main__':
    # get_data()
    telegram_bot(token)