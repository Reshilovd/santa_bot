
import random
users = [
     {
        'name': 'Денис',
        'user_id': '',
        'nicknames': ['Ден', 'Денчик'],
        'avatar': 'https://www.instagram.com/p/CL6lEVjHGyk/',
        'child' : '',
        'role': 'admin',
        'register': False
    },
    {
        'name': 'Дима',
        'user_id': '',
        'nicknames': ['Дмитрий', 'Димас', 'Димон', 'Диман'],
        'avatar': 'https://www.instagram.com/p/BiFZIQ5nHYv/',
        'child' : '',
        'role': 'user',
        'register': False
    },
    {
        'name': 'Максим',
        'user_id': '',
        'nicknames': ['Макс', 'Максон'],
        'avatar': 'https://www.instagram.com/p/B1Jp79sB5QX/',
        'child' : '',
        'role': 'user',
        'register': False
    },
    {
        'name': 'Даша',
        'user_id': '',
        'nicknames': ['Дарья'],
        'avatar': 'https://www.instagram.com/p/BnoxtIQl5yg/',
        'child' : '',
        'role': 'user',
        'register': True
    },
    {
        'name': 'Саня',
        'user_id': '',
        'nicknames': ['Александра', 'Саша'],
        'avatar': 'https://www.instagram.com/p/CJdUwYxhruO/',
        'child' : '',
        'role': 'user',
        'register': True
    }
]

def findByName(name):
    for user in users:
        if name == user['name']: return user

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
print('yes' if None else 'no')
# names = [ user['name'] + ': Child = ' + user['child']['name'] for user in users ]
# print('\n'.join(names))
for user in users:
    print(user['name'] != user['child']['name'])
# @bot.message_handler(commands=["info"])
# def send_text(message):
    # id = bot.get_user_profile_photos( message.from_user.id).photos[0][0].file_id
    # bot.send_photo(message.chat.id, id)


# @bot.message_handler(commands=['number']) #Объявили ветку для работы по команде <strong>number</strong>
# def phone(message):
#     keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) #Подключаем клавиатуру
#     button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True) #Указываем название кнопки, которая появится у пользователя
#     keyboard.add(button_phone) #Добавляем эту кнопку
#     bot.send_message(message.chat.id, 'Номер телефона', reply_markup=keyboard) #Дублируем сообщением о том, что пользователь сейчас отправит боту свой номер телефона (на всякий случай, но это не обязательно)
#
# @bot.message_handler(content_types=['contact']) #Объявили ветку, в которой прописываем логику на тот случай, если пользователь решит прислать номер телефона :)
# def contact(message):
#     if message.contact is not None: #Если присланный объект <strong>contact</strong> не равен нулю
#         print(message.contact) #Выводим у себя в панели контактные данные. А вообщем можно их, например, сохранить или сделать что-то еще.
