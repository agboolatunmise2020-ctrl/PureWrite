import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler

# --- إعدادات اللوج ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- الإعدادات ---
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/gladiatorsofgold")

# قائمة بروابط الصور التي أرفقتها (يفضل رفعها والحصول على الـ File ID لسرعة أكبر)
TESTIMONIAL_IMAGES = [
    "https://i.ibb.co/V93tS8N/10.jpg",
    "https://i.ibb.co/9H8vH1K/99.jpg",
    "https://i.ibb.co/ZzN5y8Y/88.jpg"
]

STEP_SHOW_TESTIMONIALS = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الرسالة الترحيبية الأولى"""
    keyboard = [[InlineKeyboardButton("👉 جاهز، أرني النتائج", callback_data="show_evidence")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "أنت على بعد خطوة من فهم كيف نتداول الذهب بشكل احترافي 📊\n"
        "كل صفقة نشرحها قبل الدخول (مش إشارات عشوائية)\n\n"
        "جاهز تشوف بنفسك؟"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup)
    return STEP_SHOW_TESTIMONIALS

async def show_evidence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إرسال الشهادات ثم رسالة مميزات القناة وزر الدخول"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text("⏳ جاري استعراض بعض نتائج أعضائنا...")

    # إرسال الصور كمجموعة (Media Group) لتبدو منظمة
    media = [InputMediaPhoto(img) for img in TESTIMONIAL_IMAGES]
    await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media)

    # رسالة مميزات القناة مع الزر النهائي
    feature_text = (
        "داخل القناة:\n"
        "• تحليل قبل أي صفقة\n"
        "• خطة كاملة (Entry / SL / TP)\n"
        "• تحديثات مباشرة خلال جلسات لندن و نيويورك\n\n"
        "الدخول مفتوح لفترة محدودة ⏳"
    )
    
    keyboard = [[InlineKeyboardButton("👉 دخول القناة", url=CHANNEL_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=feature_text,
        reply_markup=reply_markup
    )
    
    return ConversationHandler.END

def main():
    if not TOKEN:
        logger.error("BOT_TOKEN missing!")
        return

    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            STEP_SHOW_TESTIMONIALS: [CallbackQueryHandler(show_evidence, pattern="^show_evidence$")],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)
    
    logger.info("Bot is running with Evidence & Group Media logic...")
    application.run_polling()

if __name__ == "__main__":
    main()
