import telebot
from telebot import types

API_TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# In-memory storage for user text
user_data = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = (
        "✨ *How to use RePhrase AI*\n\n"
        "1. Send me any text you want to rewrite.\n"
        "2. Choose your preferred tone from the buttons.\n"
        "3. Get your result instantly!"
    )
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_data[message.chat.id] = message.text
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👔 Professional", callback_data="tone_pro"),
        types.InlineKeyboardButton("🍃 Simple English", callback_data="tone_simple"),
        types.InlineKeyboardButton("🎨 Creative", callback_data="tone_creative"),
        types.InlineKeyboardButton("🛠️ Fix Grammar", callback_data="tone_fix"),
        types.InlineKeyboardButton("❓ Get Help", callback_data="get_help")
    )
    bot.send_message(message.chat.id, "Select the desired tone:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id

    if call.data == "get_help":
        send_welcome(call.message)
        bot.answer_callback_query(call.id)
        return

    if call.data.startswith('tone_'):
        original_text = user_data.get(chat_id)
        if not original_text:
            bot.send_message(chat_id, "Please send your text again.")
            return

        bot.answer_callback_query(call.id, "Processing...")
        
        # Simulated Result (Connect your AI API here)
        result = f"Here is your rewrite:\n\n[Paraphrased version of: {original_text}]"
        
        # Feedback Buttons
        feedback_markup = types.InlineKeyboardMarkup()
        feedback_markup.add(
            types.InlineKeyboardButton("Helpful 👍", callback_data="feedback_good"),
            types.InlineKeyboardButton("Not Helpful 👎", callback_data="feedback_bad")
        )
        
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=result)
        bot.send_message(chat_id, "Are you satisfied with this result?", reply_markup=feedback_markup)

    elif call.data.startswith('feedback_'):
        response = "Thanks for the feedback! We'll use it to improve." if "good" in call.data else "Sorry about that. We are working to serve you better!"
        bot.answer_callback_query(call.id, "Feedback received")
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=response)

bot.polling()
