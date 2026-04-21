import telebot
from telebot import types

API_TOKEN = '7971769630:AAHJRyN3AgtJvb0zg8HZx6EEWwSW94V81iw' # Ensure your token is here!
bot = telebot.TeleBot(API_TOKEN)

user_data = {}

def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👔 Professional", callback_data="tone_pro"),
        types.InlineKeyboardButton("🍃 Simple English", callback_data="tone_simple"),
        types.InlineKeyboardButton("🎨 Creative", callback_data="tone_creative"),
        types.InlineKeyboardButton("🛠️ Fix Grammar", callback_data="tone_fix"),
        types.InlineKeyboardButton("❓ Help", callback_data="get_help")
    )
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "✨ *RePhrase AI is Ready*\n\n"
        "Send me any text you want to rewrite, then choose a tone below."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=get_main_menu())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_data[message.chat.id] = message.text
    bot.send_message(message.chat.id, "Select the desired tone for your text:", reply_markup=get_main_menu())

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id

    if call.data == "get_help":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "Simply type your sentence and click a tone button to rewrite it!")
        return

    if call.data.startswith('tone_'):
        original_text = user_data.get(chat_id)
        if not original_text:
            bot.answer_callback_query(call.id, "Please send text first!", show_alert=True)
            return

        bot.answer_callback_query(call.id, "Processing...")
        
        # Result logic
        result = f"✅ *Rewritten Version:*\n\nYour new text will appear here based on the {call.data} selection."
        
        feedback_markup = types.InlineKeyboardMarkup()
        feedback_markup.add(
            types.InlineKeyboardButton("Helpful 👍", callback_data="feedback_good"),
            types.InlineKeyboardButton("Not Helpful 👎", callback_data="feedback_bad")
        )
        
        bot.send_message(chat_id, result, parse_mode="Markdown", reply_markup=feedback_markup)

    elif call.data.startswith('feedback_'):
        bot.answer_callback_query(call.id, "Feedback saved!")
        bot.edit_message_text("Thanks for helping us improve!", chat_id, call.message.message_id)

bot.polling()
