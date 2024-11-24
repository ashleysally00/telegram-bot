from telegram.ext import Application, CommandHandler, MessageHandler
from telegram.ext.filters import TEXT
from dotenv import load_dotenv
import os
from commands import start, echo, thesaurus  # Import commands from commands.py

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))          # Start command
    application.add_handler(CommandHandler("thesaurus", thesaurus))  # Thesaurus command
    application.add_handler(MessageHandler(TEXT, echo))              # Echo for text messages

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
