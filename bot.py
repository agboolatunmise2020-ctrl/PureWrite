import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler

# --- LOGGING SETUP ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- ENVIRONMENT VARIABLES ---
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/gladiatorsofgold")

# --- IMAGE LIST (Using your GitHub Raw Links) ---
# Ensure these names match your GitHub filenames exactly (e.g., .jpeg vs .jpg)
IMAGES = [
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/10.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/99.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/88.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/77.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/66.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/55.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/44.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/33.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/22.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/11.jpeg"
]

START_STATE, SHOW_RESULTS_STATE = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the first welcome message with the button."""
    keyboard = [[InlineKeyboardButton("👉 جاهز، أرني النتائج", callback_data="get_pics")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "أنت على بعد خطوة من فهم كيف نتداول الذهب بشكل احترافي 📊\n"
        "كل صفقة نشرحها قبل الدخول (مش إشارات عشوائية)\n\n"
        "جاهز تشوف بنفسك؟"
    )
    
    await update.message.reply_text(text, reply_markup=reply_markup)
    return START_STATE

async def send_media_album(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends all 10 images at once as an album when the button is clicked."""
    query = update.callback_query
    await query.answer()
    
    chat_id = update.effective_chat.id

    # Create the list of photos for the album
    media_group = [InputMediaPhoto(media=url) for url in IMAGES]

    try:
        # Send all images together
        await context.bot.send_media_group(chat_id=chat_id, media=media_group)
        
        # Immediately send the follow-up button for the final link
        keyboard = [[InlineKeyboardButton("👉 دخول القناة", callback_data="get_final")]]
        await context.bot.send_message(
            chat_id=chat_id, 
            text="اضغط للمتابعة إلى القناة 👇", 
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return SHOW_RESULTS_STATE
        
    except Exception as e:
        logger.error(f"Error sending images: {e}")
        await context.bot.send_message(chat_id=chat_id, text="Error loading images. Please check if files are on GitHub.")
        return ConversationHandler.END

async def final_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the final channel link."""
    query = update.callback_query
    await query.answer()
    
    text = (
        "داخل القناة:\n"
        "• تحليل قبل أي صفقة\n"
        "• خطة كاملة (Entry / SL / TP)\n"
        "• تحديثات مباشرة خلال جلسات لندن و نيويورك\n\n"
        "الدخول مفتوح لفترة محدودة ⏳"
    )
    
    keyboard = [[InlineKeyboardButton("👉 دخول القناة الرسمية", url=CHANNEL_LINK)]]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=InlineKeyboardMarkup(keyboard))
    return ConversationHandler.END

def main():
    """Starts the bot."""
    if not TOKEN:
        print("Error: BOT_TOKEN not found in environment variables.")
        return

    app = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_STATE: [CallbackQueryHandler(send_media_album, pattern="^get_pics$")],
            SHOW_RESULTS_STATE: [CallbackQueryHandler(final_step, pattern="^get_final$")],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    app.add_handler(conv_handler)
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
