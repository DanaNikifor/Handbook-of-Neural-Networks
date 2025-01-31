import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
from Token import API_TOKEN

bot = telebot.TeleBot(API_TOKEN)
main_path = './test1'

# Функция для создания основного уровня кнопок
def create_main_buttons():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="О проекте", callback_data="about_project"))

    try:
        with open(f'{main_path}//main.txt', 'r', encoding='utf-8') as file:
            for line in file:
                button = InlineKeyboardButton(text=line.strip(), callback_data=f"main_{line.strip()}")
                keyboard.add(button)
    except FileNotFoundError:
        print("Файл main.txt не найден!")
    
    return keyboard

# Функция для создания второго уровня кнопок
def create_second_level_buttons(selected_item):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Инструкции", callback_data=f"instructions_{selected_item}"))
    keyboard.add(InlineKeyboardButton(text="Модели", callback_data=f"models_{selected_item}"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="go_back_to_main"))
    return keyboard

# Функция для создания кнопок из текстовых файлов
def create_buttons_from_file(file_path):
    keyboard = InlineKeyboardMarkup()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                button = InlineKeyboardButton(text=line.strip(), callback_data=f"{file_path.split('/')[-2]}_{line.strip()}")
                keyboard.add(button)
    except FileNotFoundError:
        print(f"Файл {file_path} не найден!")
    
    return keyboard

# Обработчик команд при старте бота
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=create_main_buttons())

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "about_project":
        bot.send_message(call.message.chat.id, "Это бот для управления проектом.")

    elif call.data.startswith("main_"):
        selected_item = call.data.split("_")[1]
        bot.send_message(call.message.chat.id, f"Вы выбрали: {selected_item}", reply_markup=create_second_level_buttons(selected_item))

    elif call.data.startswith("instructions_"):
        selected_item = call.data.split("_")[1]
        file_path = f'{main_path}/{selected_item}/instructions.txt'
        keyboard = InlineKeyboardMarkup()
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                instructions = file.read().splitlines()
                for instruction in instructions:
                    keyboard.add(InlineKeyboardButton(text=instruction, callback_data=f"instruction_{instruction}_{selected_item}"))
            bot.send_message(call.message.chat.id, f"Инструкции для {selected_item}:", reply_markup=keyboard)
        except FileNotFoundError:
            bot.send_message(call.message.chat.id, f"Файл {file_path} не найден!")

    elif call.data.startswith("models_"):
        selected_item = call.data.split("_")[1]
        file_path = f'{main_path}/{selected_item}/models.txt'
        keyboard = InlineKeyboardMarkup()
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                models = file.read().splitlines()
                for model in models:
                    keyboard.add(InlineKeyboardButton(text=model, callback_data=f"model_{model}_{selected_item}"))
            bot.send_message(call.message.chat.id, f"Модели для {selected_item}:", reply_markup=keyboard)
        except FileNotFoundError:
            bot.send_message(call.message.chat.id, f"Файл {file_path} не найден!")

    elif call.data.startswith("instruction_"):
        instruction = call.data.split("_")[1]
        selected_item = call.data.split("_")[2]
        вывод = open(f'{main_path}/{selected_item}/{instruction}.txt', 'r', encoding='utf-8').read()
        bot.send_message(call.message.chat.id, вывод)

    elif call.data.startswith("model_"):
        model = call.data.split("_")[1]
        selected_item = call.data.split("_")[2]
        вывод = open(f'{main_path}/{selected_item}/{model}.txt', 'r', encoding='utf-8').read()
        bot.send_message(call.message.chat.id, вывод)

    elif call.data == "go_back_to_main":
        bot.send_message(call.message.chat.id, "Выберите опцию:", reply_markup=create_main_buttons())

# Запускаем бота
if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f'Ошибка: {e}')
            time.sleep(1)  # Пауза перед повторной попыткой