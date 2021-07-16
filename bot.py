import requests
import random
import telebot
import json
from auth_data import token
from telebot import types #Подключили дополнения


def createUser(name, avatar = '', nicknames = [], admin = False):
    return {
        'name': name,
        'user_id': '',
        'nicknames': nicknames,
        'avatar': avatar,
        'child' : '',
        'role': 'admin' if admin else 'user',
        'register': False,
        'gotChild': False,
        'boughtPresent': False
    }

users = [
    createUser('Денис', 'https://www.instagram.com/p/CL6lEVjHGyk/', ['Ден', 'Денчик'], True),
    createUser('Дима', 'https://www.instagram.com/p/BiFZIQ5nHYv/', ['Дмитрий', 'Димас', 'Димон', 'Диман']),
    createUser('Максим', 'https://www.instagram.com/p/B1Jp79sB5QX/', ['Макс', 'Максон']),
    createUser('Даша', 'https://www.instagram.com/p/BnoxtIQl5yg/', ['Дарья', 'Дашка']),
    createUser('Саня', 'https://www.instagram.com/p/CJdUwYxhruO/', ['Александра', 'Саша'])
]
process = {
    'addUser': {
        'enterName': False,
        'enterNicknames': False,
        'enterAvatar': False,
    },
    'run': False
}

def findByName(name):
    for user in users:
        if name == user['name']: return user

    return False

def findByID(id):
    for user in users:
        if id == user['user_id']: return user

    return False

def findByNick(name):
    for user in users:
        try:
            idx = user['nicknames'].index(name)
            return user
        except ValueError:
            pass

    return False

def findInChild(name):
    for user in participants:
        try:
            idx = user['nicknames'].index(name)
            return user
        except ValueError:
            pass

    return False

def qSort(users):
    names = [ user['name'] for user in users ]
    res = True
    while res:
        for user in users:
            tmpNames = list(filter(lambda n: n != user['name'], names))
            if len(tmpNames) == 0: break

            name = random.choice( tmpNames )
            names = list(filter(lambda n: n != name, names))
            user['child'] = findByName(name)
        if len(names) == 0: res = False

qSort(users)

for u in users:
    print(f"{u['name']} -> {u['child']['name']}")
tmpUser = {}
def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start(message):
        bot.send_photo(message.chat.id,'https://1.bp.blogspot.com/-qjqIsAS4SOM/X9DRolbC72I/AAAAAAABAqo/NbbazgUKPGUbiwfmjyQ445K7zwWe0UQrgCLcBGAsYHQ/s2048/santa-%25D0%25B4%25D0%25B5%25D0%25B4%2B%25D0%25BC%25D0%25BE%25D1%2580%25D0%25BE%25D0%25B7-DoV%2B%25281%2529.png')
        bot.send_message(message.chat.id,'Привет человек! Как ты мог заметить приближается уже 2022-й год, \
и поэтому выбирать санту по бумажке из шапки уже не модно! Я создан хорошим человеком специально \
для того, чтобы помочь тебе найти и сделать счастливым своего Санту!')

        bot.send_message(message.chat.id, 'Если хочешь участвовать назови свое имя:')

    @bot.message_handler(commands=["santa"])
    def santa(message):
        uid = message.from_user.id
        user = findByID(uid)
        if not user:
            bot.send_message(message.chat.id,'Сначала представься!')
            return

        name = user['name']
        child = user['child']
        gotChild = user['gotChild']

        if gotChild:
            if not child['name']:
                bot.send_message(message.chat.id, 'Кажется что - то пошло не так...')
                return

            bot.send_photo(message.chat.id, child['avatar'])
            bot.send_message(message.chat.id, 'Ты что, забыл!?\n(Если ты забыл и кто это, то набери /who_is_it и я подскажу!)')
            return

        user['gotChild'] = True
        bot.send_photo(message.chat.id, user['child']['avatar'])
        bot.send_message(message.chat.id, 'Узнаешь этого человека? Поздравляю, ты его Санта!\n(Если не узнал набери /who_is_it и я подскажу!)')

    @bot.message_handler(commands=["who_is_it"])
    def who_is_it(message):
        user = findByID(message.from_user.id)
        if not user:
            bot.send_message(message.chat.id,'Сначала представься!')
            return
        if not user['gotChild']:
            bot.send_message(message.chat.id,'Узнай кому дарить подарок!\nОтправь /santa и я расскажу тебе!')
            return

        name = user['child']['name']
        bot.send_message(message.chat.id,f"Ты точно из этой компании!? Это же {name}!")

    @bot.message_handler(commands=['adduser'])
    def addUser(message):
        uid = message.from_user.id
        user = findByID(uid)
        if not user or user['role'] != 'admin':
            bot.send_message(message.chat.id, 'Посторонним В!')
            return

        process['run'] = True
        process['addUser']['enterName'] = True
        bot.send_message(message.chat.id, 'Введите имя')

    @bot.message_handler(content_types=['text'])
    def text(message):
        uid = message.from_user.id
        name = message.text
        user = findByID(uid)

        if user and user['role'] == 'admin' and process['run']:
            global tmpUser, users

            if process['addUser']['enterAvatar']:
                tmpUser['avatar'] = name

                process['addUser']['enterAvatar'] = False
                process['run'] = False
                users.append(dict(tmpUser))
                tmpUser = {}

                qSort(users)

                names = [ user['name'] for user in users ]
                bot.send_message(message.chat.id, 'Пользователь создан')
                bot.send_message(message.chat.id, f"Все участники: {', '.join(names)}")

            if process['addUser']['enterNicknames']:
                if name.lower() == 'end':
                    process['addUser']['enterNicknames'] = False
                    process['addUser']['enterAvatar'] = True

                    bot.send_message(message.chat.id, 'Пришли мне ссылку на аватарку!')
                    return

                if not tmpUser['nicknames']: tmpUser['nicknames'] = []
                tmpUser['nicknames'].append(name)

            if process['addUser']['enterName']:
                tmpUser = createUser(name)
                process['addUser']['enterName'] = False
                process['addUser']['enterNicknames'] = True

                bot.send_message(message.chat.id, 'Теперь введите псевдонимы. Вводите по одному. Если псевдонимов больше нет отправьте end')

            return

        if user:
            msg = 'Я уже знаю как тебя зовут'
            if user['name'] != name and not findByNick(name):
                msg = 'Э, зачем обманывать?'

            bot.send_message(message.chat.id, msg)
            return

        user = findByName(name) or findByNick(name)
        if not user:
            bot.send_message( message.chat.id, f"{name}, очень жаль, но тебя нет в списке участников. Свяжись с организатором, что бы исправить это!" )
            return

        if user['register']:
            bot.send_message( message.chat.id, f"Кажется это не ты! Если же все правильно, свяжись с организатором" )
            return

        user['user_id'] = uid
        user['register'] = True

        names = [ user['name'] for user in users if user['register'] ]

        bot.send_message( message.chat.id, f"Привет {user['name']}! Добавил тебя в список участников.\nУчастники: {', '.join(names)}" )


    bot.polling()

if __name__ == '__main__':
    # get_data()
    telegram_bot(token)
