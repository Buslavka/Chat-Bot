
import telebot
from telebot import types
from deep_translator import GoogleTranslator

API_TOKEN = '7715842066:AAGwQCW_HxypTsbzqxLPj5kQuMXl7YYrsiA'
bot = telebot.TeleBot(API_TOKEN)

# Храним язык для каждого пользователя
user_language = {}

# Список доступных языков
LANG_OPTIONS = {
    '🇬🇧 Английский': 'en',
    '🇩🇪 Немецкий': 'de',
    '🇱🇻 Латышский': 'lv' ,
    '🇷🇺 Русский': 'ru',
    '🇫🇷 Французский': 'fr',
    '🇪🇸 Испанский': 'es',
    '🇮🇹 Итальянский': 'it'
}

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):

    with open('Елена Федорова (1).png', 'rb') as photo:  # 🔁 Файл должен быть в той же папке
        bot.send_photo(message.chat.id, photo)

    # Отправляем приветственное сообщение с текстом
    text = "Привет! Я твой личный переводчик)\nМоя цель — помочь вам легко и быстро преодолевать языковые барьеры ✈️\n"
    bot.send_message(message.chat.id, text)

    # Создаем кнопки для выбора языка
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for lang in LANG_OPTIONS.keys():
        markup.add(types.KeyboardButton(lang))

    # Отправляем сообщение с предложением выбрать язык
    bot.send_message(message.chat.id, "Выбери язык, на который нужно переводить:", reply_markup=markup)

# Обработка кнопки выбора языка
@bot.message_handler(func=lambda message: message.text in LANG_OPTIONS)
def choose_language(message):
    user_language[message.chat.id] = LANG_OPTIONS[message.text]
    bot.send_message(message.chat.id, f" {message.text}\nВведите фразу✅")

# Обработка текста и перевод
@bot.message_handler(func=lambda message: True)
def translate_text(message):
    chat_id = message.chat.id
    if chat_id not in user_language:
        bot.send_message(chat_id, "Сначала выбери язык перевода, используя кнопки ниже.")
        return

    target_lang = user_language[chat_id]
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(message.text)
        bot.send_message(chat_id, f"Перевод ({target_lang}):\n{translated}")
    except Exception as e:
        bot.send_message(chat_id, "❌ Ошибка при переводе.")

# Запуск бота
bot.polling()
