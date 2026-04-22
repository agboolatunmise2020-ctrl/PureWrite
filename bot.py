import telebot
from telebot import types
import g4f  # This handles the free AI rewriting

# INSERT YOUR REAL TOKEN BELOW
API_TOKEN = '7971769630:AAHJRyN3AgtJvb0zg8HZx6EEWwSW94V81iw'
'
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
    welcome_text = "✨ RePhrase AI is Ready\n\nSend me any text you want to rewrite, then choose a tone below."
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_data[message.chat.id] = message.text
    bot.send_message(message.chat.id, "Select the desired tone for your text:", reply_markup=get_main_menu())

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id

    if call.data == "get_help":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "Instructions: Type your sentence first, then tap a tone button to rewrite it!")
        return

    if call.data.startswith('tone_'):
        original_text = user_data.get(chat_id)
        if not original_text:
            bot.answer_callback_query(call.id, "Please send text first!", show_alert=True)
            return

        bot.answer_callback_query(call.id, "AI is rewriting...")
        
        tones = {"pro": "Professional", "simple": "Simple English", "creative": "Creative", "fix": "Grammar correction"}
        selected_tone = tones.get(call.data.split('_')[1])

        try:
            # The AI Logic
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Paraphrase the following text in a {selected_tone} tone. Keep it human-like and simple: {original_text}"}],
            )
            
            result = f"✅ REWRITTEN ({selected_tone}):\n\n{response}"
        except Exception:
            result = "⚠️ AI is busy. Please try again in a moment."

        feedback_markup = types.InlineKeyboardMarkup()
        feedback_markup.add(
            types.InlineKeyboardButton("Helpful 👍", callback_data="feedback_good"),
            types.InlineKeyboardButton("Not Helpful 👎", callback_data="feedback_bad")
        )
        
        bot.send_message(chat_id, result, reply_markup=feedback_markup)

    elif call.data.startswith('feedback_'):
        bot.answer_callback_query(call.id, "Feedback received!")
        bot.edit_message_text("Thanks! We'll use your feedback to improve.", chat_id, call.message.message_id)

bot.polling()
