import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# --- LOGGING ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_LINK = os.getenv("CHANNEL_LINK")

# STEP 1: Put the File IDs here once you get them from the logs
IMAGES = [
    "PASTE_FILE_ID_1_HERE",
    "PASTE_FILE_ID_2_HERE"
]

START_STATE, SHOW_RESULTS_STATE = range(2)

# --- THIS PART HELPS YOU GET THE IDs ---
async def log_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        print(f"--- COPY THIS ID: {file_id}")
        await update.message.reply_text("ID logged! Check Render logs.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("👉 جاهز، أرني النتائج", callback_data="get_pics")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "أنت على بعد خطوة من فهم كيف نتداول الذهب بشكل احترافي 📊\nكل صفقة نشرحها قبل الدخول...\n\nجاهز تشوف بنفسك؟"
    await update.message.reply_text(text, reply_markup=reply_markup)
    return START_STATE

async def send_testimonials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Send Images
    media = [InputMediaPhoto(img) for img in IMAGES if "PASTE" not in img]
    if media:
        await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media)

    # Next Button
    keyboard = [[InlineKeyboardButton("👉 دخول", callback_data="get_features")]]
    await context.bot.send_message(chat_id=update.effective_chat.id, text="اضغط للمتابعة 👇", reply_markup=InlineKeyboardMarkup(keyboard))
    return SHOW_RESULTS_STATE

async def final_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "داخل القناة:\n• تحليل قبل أي صفقة...\nالدخول مفتوح لفترة محدودة ⏳"
    keyboard = [[InlineKeyboardButton("👉 دخول القناة", url=CHANNEL_LINK)]]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=InlineKeyboardMarkup(keyboard))
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()
    
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_STATE: [CallbackQueryHandler(send_testimonials, pattern="^get_pics$")],
            SHOW_RESULTS_STATE: [CallbackQueryHandler(final_step, pattern="^get_features$")],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.PHOTO, log_file_id)) # This captures IDs
    app.run_polling()

if __name__ == "__main__":
    main()
