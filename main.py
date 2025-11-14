import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# التوكن من متغيرات البيئة
BOT_TOKEN = os.environ.get('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(
        f"🎯 **مرحباً {user.first_name}!**\n\n"
        "🤖 **أنا البوت الذكي لأبو علي**\n\n"
        "✅ **الميزات المتاحة:**\n"
        "• تحليل البوتات الذكي\n"
        "• إدارة المحافظ\n"
        "• نظام الإحالات\n"
        "• إدارة المشاريع\n"
        "• تقارير تلقائية\n\n"
        "🚀 **البوت يعمل على Render بنجاح!**",
        parse_mode='Markdown'
    )

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 **نظام تحليل البوتات جاهز**\n\n"
        "أرسل username أي بوت لتحليله!",
        parse_mode='Markdown'
    )

def main():
    # إعداد التسجيل
    logging.basicConfig(level=logging.INFO)
    
    if not BOT_TOKEN:
        logging.error("❌ BOT_TOKEN غير موجود!")
        return
    
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        # إضافة الأوامر
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("analyze", analyze))
        
        # بدء البوت
        application.run_polling()
        logging.info("✅ البوت يعمل على Render!")
        
    except Exception as e:
        logging.error(f"❌ خطأ: {e}")

if __name__ == '__main__':
    main()
