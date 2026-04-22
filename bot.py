import telebot
from telebot import types

# INSERT YOUR REAL TOKEN BELOW
API_TOKEN = 'YOUR_BOT_TOKEN'
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
        bot.send_message(chat_id, "Instructions: Type your sentence first, then tap a tone button to see the magic!")
        return

    if call.data.startswith('tone_'):
        original_text = user_data.get(chat_id)
        if not original_text:
            bot.answer_callback_query(call.id, "Please send text first!", show_alert=True)
            return

        bot.answer_callback_query(call.id, "Rewriting...")
        
        # Mapping the tones for the display
        tones = {"pro": "Professional", "simple": "Simple English", "creative": "Creative", "fix": "Grammar Fix"}
        selected_tone = tones.get(call.data.split('_')[1], "Selected Tone")

        # Result display (Clean text to avoid 400 errors)
        result = f"✅ REWRITTEN VERSION ({selected_tone}):\n\n[Your rewritten text for: '{original_text}' will appear here.]"
        
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
