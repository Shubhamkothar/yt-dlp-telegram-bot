import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
BOT_TOKEN = os.getenv("7934946142:AAGb409DhETS_hY2jg0gIsF-EBa-ZQYyk7A")
DOWNLOAD_PATH = "downloads"

os.makedirs(DOWNLOAD_PATH, exist_ok=True)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me a YouTube link, and I'll download it for you!")

def download_video(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    update.message.reply_text("Downloading... Please wait.")

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{DOWNLOAD_PATH}/%(title)s.%(ext)s',
        'noplaylist': True,
        'merge_output_format': 'mp4',
        'max_filesize': 2000000000
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            update.message.reply_text("Upload in progress...")
            with open(file_path, 'rb') as video:
                update.message.reply_video(video=video)
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")
        logger.error(e)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
