import telebot
import info
import ID

from telebot import types

token = input("Input your bot token: ")

bot = telebot.TeleBot(token)

# Инициализация переменных
test_passed = False
character = ""
questions = 1


@bot.message_handler(commands=['start'])
def start(message):
    for i in ID.ID:
        tp = ID.ID["Test_Passed"]
        if tp == message.from_user.id:
            test_passed = True
        else:
            test_passed = False
    if not test_passed:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton(text="Пройти тест", callback_data="пройти_тест")
        keyboard.add(button1)
        bot.send_message(message.chat.id, "Привет! Я бот-анкета, пройди тест и узнай кто ты из Dota 2",
                         reply_markup=keyboard)
    elif test_passed:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton(text="Да", callback_data="пройти_тест")
        button2 = types.InlineKeyboardButton(text="Нет", callback_data="нет")
        keyboard.add(button1, button2)
        bot.send_message(message.chat.id, f"Ты уже прошел тест ты {character}. \nНе хочешь пройти тест снова?",
                         reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Доступные команды:\n/start - пройти тест")


@bot.message_handler(content_types=['text'])
def main(message):
    bot.send_message(message.chat.id, "Я тебя не понимаю, нажми /help")


def SendSticker(message, position, complexity, attribute, type_of_battle):
    global test_passed
    for i in info.HEROES:
        hero = i
        pos = int(info.HEROES[hero]["position"])
        comp = info.HEROES[hero]["complexity"]
        attr = info.HEROES[hero]["attribute"]
        tob = info.HEROES[hero]["type_of_battle"]
        if hero == "None":
            bot.send_message(message,f"Мы не нашли героя подходящего под ваши желания :("
                                          f"\nВы можете перепройти тест нажав /start")
            break
        elif pos == position and comp == complexity and attr == attribute and tob == type_of_battle:
            bot.send_message(message, f"Вы - {hero}")
            sticker = open(f'heroes\{hero}.png', "rb")
            bot.send_sticker(message, sticker)
            sticker.close()
            if not test_passed:
                ID.ID["Test_Passed"] = message
            break


def test(message, questions):
    str_questions = str(questions)
    if str_questions == "1":
        keyboard_questions_1 = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton(text="Фармить", callback_data="фармить")
        button2 = types.InlineKeyboardButton(text="Помогать", callback_data="помогать")
        keyboard_questions_1.add(button1, button2)
        bot.send_message(message, f"Вопрос №{questions}")
        bot.send_message(message, info.QUESTIONS[str_questions]["text"], reply_markup=keyboard_questions_1)
    elif str_questions == "2":
        keyboard_questions_2 = types.InlineKeyboardMarkup(row_width=3)
        button1 = types.InlineKeyboardButton(text="Немного", callback_data="немного")
        button2 = types.InlineKeyboardButton(text="Средне", callback_data="средне")
        button3 = types.InlineKeyboardButton(text="Много", callback_data="много")
        keyboard_questions_2.add(button1, button2, button3)
        bot.send_message(message, f"Вопрос {questions}")
        bot.send_message(message, info.QUESTIONS[str_questions]["text"], reply_markup=keyboard_questions_2)
    elif str_questions == "3":
        keyboard_questions_3 = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton(text="Пойду инициировать бой", callback_data="сила")
        button2 = types.InlineKeyboardButton(text="Я подойду драться", callback_data="ловкость")
        button3 = types.InlineKeyboardButton(text="Я в стороне постою", callback_data="интеллект")
        button4 = types.InlineKeyboardButton(text="Когда как", callback_data="универсал")
        keyboard_questions_3.add(button1, button2, button3, button4)
        bot.send_message(message, f"Вопрос {questions}")
        bot.send_message(message, info.QUESTIONS[str_questions]["text"], reply_markup=keyboard_questions_3)
    elif str_questions == "4":
        keyboard_questions_4 = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton(text="Ближний бой ", callback_data="melee")
        button2 = types.InlineKeyboardButton(text="Дальний бой", callback_data="range")
        keyboard_questions_4.add(button1, button2)
        bot.send_message(message, f"Вопрос {questions}")
        bot.send_message(message, info.QUESTIONS[str_questions]["text"], reply_markup=keyboard_questions_4)

@bot.callback_query_handler(func=lambda call: True)
def response_handler(call):
    global position, attribute, complexity, type_of_battle, close_test
    close_test = False
    # Запуск теста
    if call.data == "пройти_тест":
        bot.send_message(call.message.chat.id, "Запускаю тест")
        test(message=call.message.chat.id, questions=1)
    elif call.data == "нет":
        bot.send_message(call.message.chat.id, "До встречи")
    # Первый вопрос
    elif call.data == "фармить":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=info.QUESTIONS["1"]["text"], reply_markup=None)
        position = 1
        test(message=call.message.chat.id, questions=2)
        return position
    elif call.data == "помогать":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=info.QUESTIONS["1"]["text"], reply_markup=None)
        position = 5
        test(message=call.message.chat.id, questions=2)
        return position
    # Второй вопрос
    elif call.data == "немного":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=info.QUESTIONS["2"]["text"], reply_markup=None)
        complexity = "easy"
        test(message=call.message.chat.id, questions=3)
    elif call.data == "средне":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=info.QUESTIONS["2"]["text"], reply_markup=None)
        complexity = "medium"
        test(message=call.message.chat.id, questions=3)
    elif call.data == "много":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=info.QUESTIONS["2"]["text"], reply_markup=None)
        complexity = "hard"
        test(message=call.message.chat.id, questions=3)
    # Третий вопрос
    elif call.data == "сила":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=info.QUESTIONS["3"]["text"], reply_markup=None)
        attribute = "strength"
        test(message=call.message.chat.id, questions=4)
    elif call.data == "ловкость":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=info.QUESTIONS["3"]["text"], reply_markup=None)
        attribute = "agility"
        test(message=call.message.chat.id, questions=4)
    elif call.data == "интеллект":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=info.QUESTIONS["3"]["text"], reply_markup=None)
        attribute = "intellect"
        test(message=call.message.chat.id, questions=4)
    elif call.data == "универсал":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=info.QUESTIONS["3"]["text"], reply_markup=None)
        attribute = "universal"
        test(message=call.message.chat.id, questions=4)
    # Четвертый вопрос
    elif call.data == "melee":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=info.QUESTIONS["4"]["text"], reply_markup=None)
        type_of_battle = "melee"
        close_test = True
    elif call.data == "range":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=info.QUESTIONS["4"]["text"], reply_markup=None)
        type_of_battle = "range"
        close_test = True
    # Перезапуск теста
    if test_passed and call.data == "да" or call.data == "нет":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f"Ты уже прошел тест ты {character}. \nНе хочешь пройти тест снова?",
                              reply_markup=None)
    elif call.data == "пройти_тест":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text="Привет! Я бот-анкета, пройди тест и узнай кто ты из Dota 2",
                              reply_markup=None)
    # Отправка на обработку результата
    if close_test:
        SendSticker(message=call.message.chat.id, position=position, complexity=complexity, attribute=attribute, type_of_battle=type_of_battle)


bot.infinity_polling(none_stop=True)
