# main.py

import os
import logging
from telegram.ext import Updater, CommandHandler
from doodstream import DoodStream
from dotenv import load_dotenv

# Load variabel lingkungan dari file .env
load_dotenv()

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Inisialisasi bot dan kelas DoodStream
api_key = os.environ.get("DOODSTREAM_API")
if api_key is None or len(api_key) == 0:
    raise ValueError("Harap atur variabel lingkungan DOODSTREAM_API dengan kunci API Anda")

d = DoodStream(api_key)
updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

# Definisikan fungsi untuk setiap perintah bot

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Halo! Saya bot DoodStream Anda. Ketik /help untuk melihat perintah yang tersedia.")

def account_info(update, context):
    data = d.account_info()
    email = data.get("email", "Not Available")
    balance = data.get("balance", "Not Available")
    storage_used = data.get("storage_used")
    if storage_used is not None:
        storage_used = int(int(storage_used) / 1024)
    else:
        storage_used = "Not Available"
    storage_left = data.get("storage_left", "Not Available")
    premium_expire = data.get("premium_expire", "Not Available")
    
    message = f"Account Info:\nEmail: {email}\nBalance: ${balance}\nUsed Storage: {storage_used} MB\nStorage Left: {storage_left}\nPremium Expire: {premium_expire}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def account_reports(update, context):
    report = d.account_reports()
    message = "Account Reports:\n"
    for data in report.get("result", []):
        day = data.get("day", "Not Available")
        downloads = data.get("downloads", "Not Available")
        views = data.get("views", "Not Available")
        profit_views = data.get("profit_views", "Not Available")
        refs = data.get("refs", "Not Available")
        profit_refs = data.get("profit_refs", "Not Available")
        profit_total = data.get("profit_total", "Not Available")
        
        message += f"Day: {day}\n"
        message += f"Downloads: {downloads}\n"
        message += f"Views: {views}\n"
        message += f"Profit Views: ${profit_views}\n"
        message += f"Referral: {refs}\n"
        message += f"Profit Referral: ${profit_refs}\n"
        message += f"Profit Total: ${profit_total}\n\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def copy(update, context):
    if len(context.args) == 1:
        input_data = context.args[0]
        response = d.copy_video(input_data)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response["msg"])
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Usage: /copy <video_id>")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Contoh: /copy jtzuy7hncv8a")

# Tambahkan handler untuk setiap perintah
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("account", account_info))
dispatcher.add_handler(CommandHandler("reports", account_reports))
dispatcher.add_handler(CommandHandler("copy", copy))

# Jalankan bot Telegram
updater.start_polling()
updater.idle()
