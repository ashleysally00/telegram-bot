from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
from telegram.ext.filters import TEXT
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hi! I'm your bot. Send me a message, and I'll echo it back!")

# Echo message handler
async def echo(update: Update, context: CallbackContext):
    user_message = update.message.text
    await update.message.reply_text(f"You said: {user_message}")

# Main function to start the bot
def main():
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(TEXT, echo))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
