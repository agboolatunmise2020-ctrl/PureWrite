import telebot
from telebot import types

# 1. INSERT YOUR REAL TOKEN BELOW
# Keep the quote ' on the SAME line as the token!
API_TOKEN = '7971769630:AAHJRyN3AgtJvb0zg8HZx6EEWwSW94V81iw'

bot = telebot.TeleBot(API_TOKEN)
user_texts = {}

def get_format_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("UPPERCASE", callback_data="fmt_upper"),
        types.InlineKeyboardButton("lowercase", callback_data="fmt_lower"),
        types.InlineKeyboardButton("Title Case", callback_data="fmt_title"),
        types.InlineKeyboardButton("sWaP cAsE", callback_data="fmt_swap"),
        types.InlineKeyboardButton("❓ Help", callback_data="fmt_help")
    )
    return markup

@bot.message_handler(commands=['start', 'help'])
def start(message):
    welcome = (
        "✨ *PureWrite is Ready*\n\n"
        "Send me any text or sentence, and I will format it for you instantly."
    )
    bot.send_message(message.chat.id, welcome, parse_mode="Markdown", reply_markup=get_format_menu())

@bot.message_handler(func=lambda message: True)
def save_text(message):
    user_texts[message.chat.id] = message.text
    bot.send_message(message.chat.id, "Choose a format for your text:", reply_markup=get_format_menu())

@bot.callback_query_handler(func=lambda call: True)
def handle_format(call):
    chat_id = call.message.chat.id
    original = user_texts.get(chat_id)

    if call.data == "fmt_help":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "Type your sentence first, then click a button to change how the letters look!")
        return

    if not original:
        bot.answer_callback_query(call.id, "Please send some text first!", show_alert=True)
        return

    bot.answer_callback_query(call.id, "Processing...")

    if call.data == "fmt_upper":
        result = original.upper()
    elif call.data == "fmt_lower":
        result = original.lower()
    elif call.data == "fmt_title":
        result = original.title()
    elif call.data == "fmt_swap":
        result = original.swapcase()

    bot.send_message(chat_id, f"✅ *Formatted Text:*\n\n`{result}`", parse_mode="Markdown")

bot.polling()
