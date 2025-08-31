import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# إعدادات السجلّات
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# قراءة التوكن و ID من متغيرات البيئة
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# إنشاء التطبيق
app = ApplicationBuilder().token(BOT_TOKEN).build()

# مجدول للمهام التلقائية
scheduler = BackgroundScheduler()

# أمر البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت جاهز ويعمل 24/7!\nاستخدم /report لعرض تقرير الآن.")

# أمر التقرير
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ غير مصرح لك باستخدام هذا الأمر.")
        return
    report_text = f"📊 تقرير الساعة {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nكل شيء يعمل بنجاح ✅"
    await update.message.reply_text(report_text)

# مهمة مجدولة ترسل تقرير كل ساعة تلقائياً
async def scheduled_report():
    if OWNER_ID != 0:
        try:
            await app.bot.send_message(chat_id=OWNER_ID,
                text=f"⏰ تقرير تلقائي الساعة {datetime.now().strftime('%H:%M')}")
        except Exception as e:
            logger.error(f"خطأ في إرسال التقرير التلقائي: {e}")

async def main():
    # إضافة الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("report", report))

    # تشغيل المجدول
    scheduler.add_job(lambda: app.create_task(scheduled_report()), "interval", hours=1)
    scheduler.start()

    # تشغيل البوت
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
