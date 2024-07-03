from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import random
import logging

# Bot API tokeningizni bu yerga kiriting
TOKEN = '7372362181:AAECWWUfxKEADUi87uBMKGRXSg1S8H2E4Uc'

# Logging sozlamalari
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Global o'zgaruvchilar
secret_number = None
attempts = 0

# Start komandasi
def start(update: Update, context: CallbackContext) -> None:
    global secret_number, attempts
    secret_number = random.randint(1, 100)
    attempts = 0
    update.message.reply_text('Salom! Men 1 dan 100 gacha bir raqamni tanladim. Uni topa olasizmi?')

# Guess komandasi
def guess(update: Update, context: CallbackContext) -> None:
    global secret_number, attempts
    try:
        guess = int(update.message.text)
        attempts += 1
        if guess < secret_number:
            update.message.reply_text('Kattaroq son kiriting.')
        elif guess > secret_number:
            update.message.reply_text('Kichikroq son kiriting.')
        else:
            update.message.reply_text(f'Tabriklayman! Siz {attempts} urinishda to\'g\'ri topdingiz.')
            # Yangi o'yinni boshlash
            secret_number = random.randint(1, 100)
            attempts = 0
            update.message.reply_text('Yangi o\'yin boshlandi. Yana raqamni topishga harakat qiling!')
    except ValueError:
        update.message.reply_text('Iltimos, faqat raqam kiriting.')

# Help komandasi
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Raqamni topish uchun son kiriting.')

# Main funksiyasi
def main() -> None:
    # Updater va Dispatcher yarating
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Komandalarni ro'yxatdan o'tkazish
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Matnli xabarlarni qabul qilish
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, guess))

    # Botni ishga tushirish
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()