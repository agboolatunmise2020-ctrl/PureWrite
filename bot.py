import os
import logging
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler

# --- LOGGING ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- CONFIG ---
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/gladiatorsofgold")

# Stages
STEP_ONE = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Step 1: The Hook"""
    keyboard = [[InlineKeyboardButton("👉 أريد رؤية النتائج", callback_data="show_testimonials")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "أنت على بعد خطوة من فهم كيف نتداول الذهب بشكل احترافي 📊\n"
        "كل صفقة نشرحها قبل الدخول (مش إشارات عشوائية)\n\n"
        "جاهز تشوف بنفسك؟"
    )
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    return STEP_ONE

async def testimonials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Step 2: Testimonials + Final Redirect"""
    query = update.callback_query
    await query.answer()

    # Final Join Button
    keyboard = [[InlineKeyboardButton("👉 دخول القناة الآن", url=CHANNEL_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Combined Step: Testimonials + Urgency
    text = (
        "⭐ **آراء المتداولين معنا:**\n"
        "• 'أفضل قناة تحليل ذهب تابعتها فعلياً' - أحمد م.\n"
        "• 'الدقة في الأهداف خيالية، شكراً لكم' - سارة\n\n"
        "داخل القناة:\n"
        "✅ تحليل حي ومباشر\n"
        "✅ خطة كاملة (Entry / SL / TP)\n\n"
        "الدخول مفتوح لفترة محدودة ⏳"
    )
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    return ConversationHandler.END

def main():
    if not TOKEN:
        logger.error("No BOT_TOKEN found!")
        return

    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            STEP_ONE: [CallbackQueryHandler(testimonials, pattern="^show_testimonials$")],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)
    
    logger.info("Bot starting with Testimonial logic...")
    application.run_polling()

if __name__ == "__main__":
    main()
