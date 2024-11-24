from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os
from commands import start, echo, thesaurus

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    """Start the bot."""
    # Create the application
    print("Starting bot...")
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers - order matters!
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("thesaurus", thesaurus))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Start the bot
    print("Bot started successfully!")
    application.run_polling(allowed_updates=["message", "edited_message"])

if __name__ == "__main__":
    main()
