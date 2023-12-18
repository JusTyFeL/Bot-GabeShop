import sqlite3, string
import telebot, random, datetime
from dotenv import dotenv_values
from telebot import types



config = dotenv_values('.env')
bot = telebot.TeleBot(config["TELEG_TOKEN"])
print("bot run")



#Генерация ключей для steam
def generate_steam_key():
    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    key2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    key3 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    key4 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    key5 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return key, key2, key3, key4 , key5



#Логика пополнение баланса 
def balance_procces(message):
    number = int(message.text)
    user_id = message.from_user.id
    conn = sqlite3.connect(config.get('DB_NAME'))
    cur = conn.cursor()
    cur.execute(f'SELECT balance FROM users WHERE id = {user_id}')
    result = cur.fetchone()
    if result:
        balance = result[0]
        if number <= 1500 and number > 0:
           new_balance = balance + number
           cur.execute(f'UPDATE users SET balance = {new_balance} WHERE id = {user_id}')
           conn.commit()
           conn.close()
           bot.send_message(message.chat.id, f'Баланс обновился: {new_balance}₽')
        else:
            bot.send_message(message.chat.id, 'Нельзя меньше 0 и нельзя больше 1500')
    else:
        conn.close()
        bot.send_message(message.chat.id, 'Пользователь не найден')

#Старт бота
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Список игр')
    btn2 = types.KeyboardButton('Баланс')
    btn3 = types.KeyboardButton('История покупок')
    btn4 = types.KeyboardButton('Помощь')
    btn5 = types.KeyboardButton('Купить Игру')

    markup.add(btn1,btn2,btn3, btn4, btn5) 
    bot.send_message(message.chat.id, text = f'Добро пожаловать {message.from_user.first_name}! У нас вы найдете Маленький выбор игр различных жанров.  ', reply_markup=markup)
    bot.send_message(message.chat.id, 'В меню бота, вы можете посмотреть баланс,пополнить баланс, увидеть список игр которые есть на данный момент, купить игру. ', reply_markup=markup)
#Главное Меню
@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Список игр')
    btn2 = types.KeyboardButton('Баланс')
    btn3 = types.KeyboardButton('История покупок')
    btn4 = types.KeyboardButton('Помощь')
    btn5 = types.KeyboardButton('Купить Игру')

    markup.add(btn1,btn2,btn3, btn4, btn5) 
    bot.send_message(message.chat.id, '👌', reply_markup=markup)



#Регистрация пользователя
@bot.message_handler(commands=['login'])
def login(message):
    user_id = message.from_user.id 
    balance = 1000
    conn = sqlite3.connect(config.get('DB_NAME'))
    cur = conn.cursor()


    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    us_exit = cur.fetchall()

    if not us_exit:
        cur.execute("INSERT INTO users(id, balance) VALUES (?, ?)", (user_id, balance))
        bot.send_message(message.chat.id, 'Ты зарегистрировался! В кнопке "Меню" нажми /menu что бы попасть в меню')
    else:
        bot.send_message(message.chat.id, 'Ты и так зарегистрирован')
    conn.commit()
    conn.close()
    


#Логика Reply кнопок
@bot.message_handler(content_types=['text'])
def func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bbncadd = types.KeyboardButton('Пополнить баланс')
    backbtt = types.KeyboardButton('В меню назад')
    
    markup.add(bbncadd)
    markup.row(backbtt)
    if (message.text == 'Баланс'):
        conn = sqlite3.connect(config.get('DB_NAME'))
        cur = conn.cursor()
        user_id = message.from_user.id
        cur.execute(f"SELECT balance FROM users WHERE id = {user_id}")
        result = cur.fetchone()
        if result:
            balance = result[0]
            bot.send_message(message.chat.id, f'Ваш баланс {balance}₽', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Вы не можете посмотреть свой баланс, потому что вы ещё не зарегистрированы:(.\n Пропишите /login что бы зарегестрироваться')
#Пополнение баланса    
    if (message.text == 'Пополнить баланс'):
        conn = sqlite3.connect(config.get('DB_NAME'))
        cur = conn.cursor()
        user_id = message.from_user.id

        cur.execute(f'SELECT balance FROM users WHERE id = {user_id}')
        result = cur.fetchone()
        if result:
            balance = result[0]
            bot.send_message(message.chat.id, 'Введите сумму для пополнения:',reply_markup= markup)
            bot.register_next_step_handler(message, balance_procces)
        else:
            bot.send_message(message.chat.id, 'Пользователь не найден')
    elif (message.text == 'В меню назад'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnspis = types.KeyboardButton('Список игр')
        btnbal = types.KeyboardButton('Баланс')
        btnhis = types.KeyboardButton('История покупок')
        btnh = types.KeyboardButton('Помощь')
        btnbuy = types.KeyboardButton('Купить Игру')
        markup.add(btnspis,btnbal,btnhis, btnh, btnbuy)

        bot.send_message(message.chat.id, '🔙',reply_markup=markup)



#Список игр
    if (message.text == 'Список игр'):
        markup_Inl = types.InlineKeyboardMarkup()
        Button1 = types.InlineKeyboardButton('Witch It', url = 'https://www.youtube.com/watch?v=nhkmBErjKOI')
        Button2 = types.InlineKeyboardButton('Red Dead Redemption 2 ', url = 'https://www.youtube.com/watch?v=eaW0tYpxyp0')
        Button3 = types.InlineKeyboardButton('Terraria', url = 'https://www.youtube.com/watch?v=bepQu0MFJ_A')
        Button4 = types.InlineKeyboardButton('Tales Of Arise', url = 'https://www.youtube.com/watch?v=mJPrp0QJzJc')
        Button5 = types.InlineKeyboardButton('Black Mesa', url = 'https://www.youtube.com/watch?v=KHKUVdb5YTM')
        Button6 = types.InlineKeyboardButton('The Witcher 3', url = 'https://www.youtube.com/watch?v=qK4gTahM18o')
        Button7 = types.InlineKeyboardButton('Grand Theft Auto VI', url = 'https://www.youtube.com/watch?v=QdBZY2fkU-0')
        Button8 = types.InlineKeyboardButton('Mortal Kombat 1', url = 'https://www.youtube.com/watch?v=ttvi0fY_2og')
        Button9 = types.InlineKeyboardButton('Devil May Cry 5', url = 'https://www.youtube.com/watch?v=0EDAZty7yek')
        Button10 = types.InlineKeyboardButton('Cyberpunk 2077', url = 'https://www.youtube.com/watch?v=hA55WshsKvg')
        Button11 = types.InlineKeyboardButton('PAYDAY2', url = 'https://www.youtube.com/watch?v=9_iJ7Cqiqrg')
        Button12 = types.InlineKeyboardButton('Forza Horizon 4', url = 'https://www.youtube.com/watch?v=hGn1mOgQF-s')
        Button13 = types.InlineKeyboardButton('DOOM(2016)', url = 'https://www.youtube.com/watch?v=3WPkly_rnqk')
        Button14 = types.InlineKeyboardButton('Mortall Shell', url = 'https://www.youtube.com/watch?v=sXB5VM30ai4')
        Button15 = types.InlineKeyboardButton('Portal', url = 'https://www.youtube.com/watch?v=0P2dzIa6pZY' )
        Button16 = types.InlineKeyboardButton('Styx', url = 'https://www.youtube.com/watch?v=_AjArZnDheY')
        markup_Inl.add(Button1, Button2, Button3, Button4, Button5, Button6, Button7, Button8, Button9, Button10, Button11, Button12, Button13, Button14, Button15, Button16)
        bot.send_message(message.chat.id, text = 'Пока в боте очень скромный список:(', reply_markup=markup_Inl)
        
#Вопросы которые может задать пользователь
    if (message.text == 'Помощь'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Как пополнить свой баланс?')
        btn2 = types.KeyboardButton('Сколько у бота игр?')
        btn3 = types.KeyboardButton('Баланс пополняется бесконечно?')
        btn4 =types.KeyboardButton('Создатель бота смотрит аниме?')
        btn5 = types.KeyboardButton('Ключи которые я покупаю настоящие?')
        btn6 = types.KeyboardButton('Правда что создатель бота лох который не смог написать правильно бота за неделю?')
        btnback1 = types.KeyboardButton('В главное меню')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        markup.row(btnback1)
        bot.send_message(message.chat.id, text='Помощь', reply_markup=markup)
    elif (message.text == 'Как пополнить свой баланс?'):
        bot.send_message(message.chat.id, 'Во кнопке "Баланс" можно пополнить свой баланс')
    elif (message.text == 'Сколько у бота игр?'):
        bot.send_message(message.chat.id, 'На данный момент 16 игр')    
    elif (message.text == 'Баланс пополняется бесконечно?'):
        bot.send_message(message.chat.id, 'Ты не можешь закинуть на баланс больше 1500 ')
    elif (message.text == 'Создатель бота смотрит аниме?'):
        bot.send_message(message.chat.id, 'Данет')
    elif (message.text == 'Ключи которые я покупаю настоящие?'):
        bot.send_message(message.chat.id, 'Нет)')
    elif (message.text == 'Правда что создатель бота лох который не смог написать правильно бота за неделю?'):
        bot.send_video(message.chat.id, 'https://tenor.com/ru/view/%D0%BF%D0%BE%D1%88%D0%B5%D0%BB%D0%BD%D0%B0%D1%85%D1%83%D0%B9-%D0%B0%D0%BD%D0%B8%D0%BC%D0%B5-%D1%83%D0%B8%D0%BB%D0%BB%D1%81%D0%BC%D0%B8%D1%82-%D1%81%D0%BC%D0%B8%D1%82-gif-26775208', None, 'Text')
    elif (message.text == 'В главное меню'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnspis = types.KeyboardButton('Список игр')
        btnbal = types.KeyboardButton('Баланс')
        btnhis = types.KeyboardButton('История покупок')
        btnh = types.KeyboardButton('Помощь')
        btnbuy = types.KeyboardButton('Купить Игру')
        markup.add(btnspis,btnbal,btnhis, btnh, btnbuy)

        bot.send_message(message.chat.id, '🔙',reply_markup=markup)
#Бот выдаёт ключи
    key = generate_steam_key()
    if (message.text == 'Купить Игру'):

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Witch It')
        btn2 = types.KeyboardButton('Tales Of Arise')
        btn3 = types.KeyboardButton('Red Dead Redemption 2')
        btn4 = types.KeyboardButton('Terraria')
        btn5 = types.KeyboardButton('Black Mesa')
        btn6 = types.KeyboardButton('The Witcher 3')
        btn7 = types.KeyboardButton('Cyberpunk 2077')
        btnback = types.KeyboardButton('Назад')
        btn8 = types.KeyboardButton('Styx')
        btn9 = types.KeyboardButton('Forza Horizon 4')
        btn10 = types.KeyboardButton('Among Us')
        btn11 = types.KeyboardButton('DOOM(2016)')
        btn12 = types.KeyboardButton('Mortall Shell')
        btn13 = types.KeyboardButton('Grand Theft Auto VI')
        btn14 = types.KeyboardButton('PAYDAY 2')
        btn15 = types.KeyboardButton('Devil May Cry 5')

        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7,btn8,btn9,btn10,btn11,btn12, btn13, btn14)
        markup.row(btnback)
        bot.send_message(message.chat.id, text='Купить Игру', reply_markup=markup )
    
#Процесс покупки игры

    if (
        message.text == 'Witch It' 
        or message.text == 'Cyberpunk 2077' 
        or message.text == 'Red Dead Redemption 2' 
        or message.text == 'Terraria' 
        or message.text == 'Black Mesa' 
        or message.text == 'The Witcher 3' 
        or message.text == 'Tales Of Arise'
        or message.text == 'Grand Theft Auto VI'
        or message.text == 'PAYDAY 2'
        or message.text == 'Styx'
        or message.text == 'Forza Horizon 4'
        or message.text == 'Among Us'
        or message.text == 'DOOM(2016)'
        or message.text == 'Mortall Shell'
        or message.text == 'Devil May Cry 5'
        
        ):
        user_id = message.from_user.id
        conn = sqlite3.connect(config.get('DB_NAME'))
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS words (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT)")
        cur.execute('SELECT balance FROM users WHERE id = ?', (user_id,))
        result = cur.fetchone()
        if (message.text == 'Witch It'):
            balance = result[0]
            Product_price = 200
            if balance >= Product_price:

                # Вычитаем стоимость товара из баланса пользователя
                new_balance = balance - Product_price
                
                # Обновляем баланс пользователя в базе данных
                cur.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
                conn.commit()
                
                # Выполняем операции, связанные с покупкой товара
                bot.send_message(user_id, 'Поздравляю с покупкой!')
                bot.send_message(message.chat.id, f'Ваш баланс {new_balance}₽')
                keys = generate_steam_key()
                #Создаёт файл txt если его нет 
                with open('file.txt', 'w') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                #Открывает файл txt
                with open('keys.txt', 'a') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                file = open('keys.txt ', 'rb')
                bot.send_document(message.chat.id, file ) 
                file.close() 

                conn.commit()
                conn.close()
            else:
                bot.send_message(user_id, 'У вас недостаточно средств на балансе.')
        if (message.text == 'Cyberpunk 2077'):
            balance = result[0]
            Product_price = 2000
            if balance >= Product_price:

                # Вычитаем стоимость товара из баланса пользователя
                new_balance = balance - Product_price
                
                # Обновляем баланс пользователя в базе данных
                cur.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
                conn.commit()
                
                # Выполняем операции, связанные с покупкой товара
                bot.send_message(user_id, 'Поздравляю с покупкой!')
                bot.send_message(message.chat.id, f'Ваш баланс {new_balance}₽')
                keys = generate_steam_key()
                #Создаёт файл txt если его нет 
                with open('file.txt', 'w') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                #Открывает файл txt
                with open('keys.txt', 'a') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                file = open('keys.txt ', 'rb')
                bot.send_document(message.chat.id, file ) 
                file.close() 

                conn.commit()
                conn.close()
            else:
                bot.send_message(user_id, 'У вас недостаточно средств на балансе.')
        if (message.text == 'Black Mesa'):
            balance = result[0]
            Product_price = 600
            if balance >= Product_price:

                # Вычитаем стоимость товара из баланса пользователя
                new_balance = balance - Product_price
                
                # Обновляем баланс пользователя в базе данных
                cur.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
                conn.commit()
                
                # Выполняем операции, связанные с покупкой товара
                bot.send_message(user_id, 'Поздравляю с покупкой!')
                bot.send_message(message.chat.id, f'Ваш баланс {new_balance}₽')
                keys = generate_steam_key()
                #Создаёт файл txt если его нет 
                with open('file.txt', 'w') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                #Открывает файл txt
                with open('keys.txt', 'a') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                file = open('keys.txt ', 'rb')
                bot.send_document(message.chat.id, file ) 
                file.close() 

                conn.commit()
                conn.close()
            else:
                bot.send_message(user_id, 'У вас недостаточно средств на балансе.')
        if (message.text == 'The Witcher 3'):
            balance = result[0]
            Product_price = 3600
            if balance >= Product_price:

                # Вычитаем стоимость товара из баланса пользователя
                new_balance = balance - Product_price
                
                # Обновляем баланс пользователя в базе данных
                cur.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
                conn.commit()
                
                # Выполняем операции, связанные с покупкой товара
                bot.send_message(user_id, 'Поздравляю с покупкой!')
                bot.send_message(message.chat.id, f'Ваш баланс {new_balance}₽')
                keys = generate_steam_key()
                #Создаёт файл txt если его нет 
                with open('file.txt', 'w') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                #Открывает файл txt
                with open('keys.txt', 'a') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                file = open('keys.txt ', 'rb')
                bot.send_document(message.chat.id, file ) 
                file.close() 

                conn.commit()
                conn.close()
            else:
                bot.send_message(user_id, 'У вас недостаточно средств на балансе.')
        if (message.text == 'Tales Of Arise'):
            balance = result[0]
            Product_price = 5600
            if balance >= Product_price:

                # Вычитаем стоимость товара из баланса пользователя
                new_balance = balance - Product_price
                
                # Обновляем баланс пользователя в базе данных
                cur.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
                conn.commit()
                
                # Выполняем операции, связанные с покупкой товара
                bot.send_message(user_id, 'Поздравляю с покупкой!')
                bot.send_message(message.chat.id, f'Ваш баланс {new_balance}₽')
                keys = generate_steam_key()
                #Создаёт файл txt если его нет 
                with open('file.txt', 'w') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                #Открывает файл txt
                with open('keys.txt', 'a') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                file = open('keys.txt ', 'rb')
                bot.send_document(message.chat.id, file ) 
                file.close() 

                conn.commit()
                conn.close()
            else:
                bot.send_message(user_id, 'У вас недостаточно средств на балансе.')
        if (message.text == 'Grand Theft Auto VI'):
            balance = result[0]
            Product_price = 10000
            if balance >= Product_price:

                # Вычитаем стоимость товара из баланса пользователя
                new_balance = balance - Product_price
                
                # Обновляем баланс пользователя в базе данных
                cur.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
                conn.commit()
                
                # Выполняем операции, связанные с покупкой товара
                bot.send_message(user_id, 'Поздравляю с покупкой!')
                bot.send_message(message.chat.id, f'Ваш баланс {new_balance}₽')
                keys = generate_steam_key()
                #Создаёт файл txt если его нет 
                with open('file.txt', 'w') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                #Открывает файл txt
                with open('keys.txt', 'a') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                file = open('keys.txt ', 'rb')
                bot.send_document(message.chat.id, file ) 
                file.close() 

                conn.commit()
                conn.close()
            else:
                bot.send_message(user_id, 'У вас недостаточно средств на балансе.')
        if (message.text == 'PAYDAY 2'):
            balance = result[0]
            Product_price = 450
            if balance >= Product_price:

                # Вычитаем стоимость товара из баланса пользователя
                new_balance = balance - Product_price
                
                # Обновляем баланс пользователя в базе данных
                cur.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
                conn.commit()
                
                # Выполняем операции, связанные с покупкой товара
                bot.send_message(user_id, 'Поздравляю с покупкой!')
                bot.send_message(message.chat.id, f'Ваш баланс {new_balance}₽')
                keys = generate_steam_key()
                #Создаёт файл txt если его нет 
                with open('file.txt', 'w') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                #Открывает файл txt
                with open('keys.txt', 'a') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                file = open('keys.txt ', 'rb')
                bot.send_document(message.chat.id, file ) 
                file.close() 

                conn.commit()
                conn.close()
            else:
                bot.send_message(user_id, 'У вас недостаточно средств на балансе.')
        if (message.text == 'Forza Horizon 4'):
            balance = result[0]
            Product_price = 1500
            if balance >= Product_price:

                # Вычитаем стоимость товара из баланса пользователя
                new_balance = balance - Product_price
                
                # Обновляем баланс пользователя в базе данных
                cur.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
                conn.commit()
                
                # Выполняем операции, связанные с покупкой товара
                bot.send_message(user_id, 'Поздравляю с покупкой!')
                bot.send_message(message.chat.id, f'Ваш баланс {new_balance}₽')
                keys = generate_steam_key()
                #Создаёт файл txt если его нет 
                with open('keys.txt', 'w') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                #Открывает файл txt
                with open('keys.txt', 'a') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                file = open('keys.txt ', 'rb')
                bot.send_document(message.chat.id, file ) 
                file.close() 

                conn.commit()
                conn.close()
            else:
                bot.send_message(user_id, 'У вас недостаточно средств на балансе.')
        if (message.text == 'Among Us'):
            balance = result[0]
            Product_price = 99
            if balance >= Product_price:

                # Вычитаем стоимость товара из баланса пользователя
                new_balance = balance - Product_price
                
                # Обновляем баланс пользователя в базе данных
                cur.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
                conn.commit()
                
                # Выполняем операции, связанные с покупкой товара
                bot.send_message(user_id, 'Поздравляю с покупкой!')
                bot.send_message(message.chat.id, f'Ваш баланс {new_balance}₽')
                keys = generate_steam_key()
                #Создаёт файл txt если его нет 
                with open('file.txt', 'w') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                #Открывает файл txt
                with open('keys.txt', 'a') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                file = open('keys.txt ', 'rb')
                bot.send_document(message.chat.id, file ) 
                file.close() 

                conn.commit()
                conn.close()
            else:
                bot.send_message(user_id, 'У вас недостаточно средств на балансе.')
        if (message.text == 'DOOM(2016)'):
            balance = result[0]
            Product_price = 999
            if balance >= Product_price:

                # Вычитаем стоимость товара из баланса пользователя
                new_balance = balance - Product_price
                
                # Обновляем баланс пользователя в базе данных
                cur.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
                conn.commit()
                
                # Выполняем операции, связанные с покупкой товара
                bot.send_message(user_id, 'Поздравляю с покупкой!')
                bot.send_message(message.chat.id, f'Ваш баланс {new_balance}₽')
                keys = generate_steam_key()
                #Создаёт файл txt если его нет 
                with open('file.txt', 'w') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                #Открывает файл txt
                with open('keys.txt', 'a') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                file = open('keys.txt ', 'rb')
                bot.send_document(message.chat.id, file ) 
                file.close() 

                conn.commit()
                conn.close()
            else:
                bot.send_message(user_id, 'У вас недостаточно средств на балансе.')
        if (message.text == 'Mortall Shell'):
            balance = result[0]
            Product_price = 700
            if balance >= Product_price:

                # Вычитаем стоимость товара из баланса пользователя
                new_balance = balance - Product_price
                
                # Обновляем баланс пользователя в базе данных
                cur.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
                conn.commit()
                
                # Выполняем операции, связанные с покупкой товара
                bot.send_message(user_id, 'Поздравляю с покупкой!')
                bot.send_message(message.chat.id, f'Ваш баланс {new_balance}₽')
                keys = generate_steam_key()
                #Создаёт файл txt если его нет 
                with open('file.txt', 'w') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                #Открывает файл txt
                with open('keys.txt', 'a') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                file = open('keys.txt ', 'rb')
                bot.send_document(message.chat.id, file ) 
                file.close() 

                conn.commit()
                conn.close()
            else:
                bot.send_message(user_id, 'У вас недостаточно средств на балансе.')
        if (message.text == 'Red Dead Redemption 2'):
            balance = result[0]
            Product_price = 1599
            if balance >= Product_price:

                # Вычитаем стоимость товара из баланса пользователя
                new_balance = balance - Product_price
                
                # Обновляем баланс пользователя в базе данных
                cur.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
                conn.commit()
                
                # Выполняем операции, связанные с покупкой товара
                bot.send_message(user_id, 'Поздравляю с покупкой!')
                bot.send_message(message.chat.id, f'Ваш баланс {new_balance}₽')
                keys = generate_steam_key()
                #Создаёт файл txt если его нет 
                with open('file.txt', 'w') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                #Открывает файл txt
                with open('keys.txt', 'a') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                file = open('keys.txt ', 'rb')
                bot.send_document(message.chat.id, file ) 
                file.close() 

                conn.commit()
                conn.close()
            else:
                bot.send_message(user_id, 'У вас недостаточно средств на балансе.')
        if (message.text == 'Terraria'):
            balance = result[0]
            Product_price = 299
            if balance >= Product_price:

                # Вычитаем стоимость товара из баланса пользователя
                new_balance = balance - Product_price
                
                # Обновляем баланс пользователя в базе данных
                cur.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
                conn.commit()
                
                # Выполняем операции, связанные с покупкой товара
                bot.send_message(user_id, 'Поздравляю с покупкой!')
                bot.send_message(message.chat.id, f'Ваш баланс {new_balance}₽')
                keys = generate_steam_key()
                #Создаёт файл txt если его нет 
                with open('file.txt', 'w') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                #Открывает файл txt
                with open('keys.txt', 'a') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                file = open('keys.txt ', 'rb')
                bot.send_document(message.chat.id, file ) 
                file.close() 

                conn.commit()
                conn.close()
            else:
                bot.send_message(user_id, 'У вас недостаточно средств на балансе.')
        if (message.text == 'Styx'):
            balance = result[0]
            Product_price = 99
            if balance >= Product_price:

                # Вычитаем стоимость товара из баланса пользователя
                new_balance = balance - Product_price
                
                # Обновляем баланс пользователя в базе данных
                cur.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
                conn.commit()
                
                # Выполняем операции, связанные с покупкой товара
                bot.send_message(user_id, 'Поздравляю с покупкой!')
                bot.send_message(message.chat.id, f'Ваш баланс {new_balance}₽')
                keys = generate_steam_key()
                #Создаёт файл txt если его нет 
                with open('file.txt', 'w') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                #Открывает файл txt
                with open('keys.txt', 'a') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                file = open('keys.txt ', 'rb')
                bot.send_document(message.chat.id, file ) 
                file.close() 

                conn.commit()
                conn.close()
            else:
                bot.send_message(user_id, 'У вас недостаточно средств на балансе.')
        if (message.text == 'Devil May Cry 5'):
            balance = result[0]
            Product_price = 1500
            if balance >= Product_price:

                # Вычитаем стоимость товара из баланса пользователя
                new_balance = balance - Product_price
                
                # Обновляем баланс пользователя в базе данных
                cur.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
                conn.commit()
                
                # Выполняем операции, связанные с покупкой товара
                bot.send_message(user_id, 'Поздравляю с покупкой!')
                bot.send_message(message.chat.id, f'Ваш баланс {new_balance}₽')
                keys = generate_steam_key()
                #Создаёт файл txt если его нет 
                with open('file.txt', 'w') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                #Открывает файл txt
                with open('keys.txt', 'a') as file:
                    file.write('-'.join([i for i in keys]) + ' ')
                file = open('keys.txt ', 'rb')
                bot.send_document(message.chat.id, file ) 
                file.close() 

                conn.commit()
                conn.close()
            else:
                bot.send_message(user_id, 'У вас недостаточно средств на балансе.')
    if (message.text == 'История покупок'):
        file = open('keys.txt ', 'rb')
        bot.send_document(message.chat.id, file ) 
        file.close() 
#Кнопка назад
    if (message.text == 'Назад'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnspis = types.KeyboardButton('Список игр')
        btnbal = types.KeyboardButton('Баланс')
        btnhis = types.KeyboardButton('История покупок')
        btnh = types.KeyboardButton('Помощь')
        btnbuy = types.KeyboardButton('Купить Игру')
        markup.add(btnspis,btnbal,btnhis, btnh, btnbuy)

        bot.send_message(message.chat.id, '🔙',reply_markup=markup)



bot.polling(none_stop = True) 