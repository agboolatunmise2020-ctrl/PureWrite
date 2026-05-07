import os
import logging
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler

# --- LOGGING SETUP ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/gladiatorsofgold")

# Stages
STEP_ONE, STEP_TWO = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Start command triggered")
    keyboard = [[InlineKeyboardButton("👉 دخول", callback_data="go_to_step2")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        "أنت على بعد خطوة من فهم كيف نتداول الذهب بشكل احترافي 📊\n"
        "كل صفقة نشرحها قبل الدخول (مش إشارات عشوائية)\n\n"
        "جاهز تشوف بنفسك؟"
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    return STEP_ONE

async def step_two(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    logger.info("Moving to Step 2")
    
    keyboard = [[InlineKeyboardButton("👉 فتح الوصول", callback_data="go_to_step3")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        "داخل القناة:\n"
        "* تحليل قبل أي صفقة\n"
        "* خطة كاملة (Entry / SL / TP)\n"
        "* تحديثات مباشرة خلال جلسات لندن و نيويورك\n\n"
        "الدخول مفتوح لفترة محدودة ⏳"
    )
    await query.edit_message_text(text, reply_markup=reply_markup)
    return STEP_TWO

async def step_three(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    logger.info("Final link delivered")
    
    keyboard = [[InlineKeyboardButton("👉 دخول القناة", url=CHANNEL_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "اضغط للدخول الآن 👇"
    await query.edit_message_text(text, reply_markup=reply_markup)
    return ConversationHandler.END

if __name__ == '__main__':
    if not TOKEN:
        logger.error("No BOT_TOKEN provided! Exiting.")
        sys.exit(1)

    logger.info("Initializing Application...")
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            STEP_ONE: [CallbackQueryHandler(step_two, pattern='^go_to_step2$')],
            STEP_TWO: [CallbackQueryHandler(step_three, pattern='^go_to_step3$')],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    app.add_handler(conv_handler)
    
    logger.info("Bot is polling. Send /start to your bot in Telegram.")
    app.run_polling()
