import requests
from telegram import Update
from telegram.ext import CallbackContext

# Start command
async def start(update: Update, context: CallbackContext):
    first_name = update.effective_user.first_name
    await update.message.reply_text(f"Hi {first_name}! I'm your bot. How can I assist you today?")

# Echo message handler
async def echo(update: Update, context: CallbackContext):
    user_message = update.message.text
    await update.message.reply_text(f"You said: {user_message}")

# Thesaurus command
async def thesaurus(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Usage: /thesaurus <word>")
        return

    word = context.args[0]
    response = requests.get(f"https://api.datamuse.com/words?rel_syn={word}")
    
    if response.status_code == 200:
        data = response.json()
        if data:
            synonyms = [item['word'] for item in data[:5]]  # Limit to 5 synonyms
            await update.message.reply_text(
                f"Synonyms for '{word}': {', '.join(synonyms)}"
            )
        else:
            await update.message.reply_text(f"Sorry, I couldn't find synonyms for '{word}'.")
    else:
        await update.message.reply_text("There was an error fetching thesaurus data.")
