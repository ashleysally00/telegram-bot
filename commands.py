# commands.py
import requests
import pandas as pd
from telegram import Update
from telegram.ext import ContextTypes
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load the emoji sentiment dataset once when the module is imported
try:
    emoji_data = pd.read_csv("Emoji_Sentiment_Data_v1.0.csv", encoding="utf-8")
    print("Emoji data loaded successfully")
except Exception as e:
    logger.error(f"Error loading emoji data: {e}")
    emoji_data = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    welcome_message = (
        "👋 Welcome to the Thesaurus Bot!\n\n"
        "I can help you find synonyms and matching emojis for words.\n"
        "Just use the /thesaurus command followed by a word.\n\n"
        "Example: /thesaurus happy"
    )
    await update.message.reply_text(welcome_message)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle non-command messages."""
    help_message = (
        "To find synonyms and matching emojis, use the /thesaurus command followed by a word.\n"
        "Example: /thesaurus happy"
    )
    await update.message.reply_text(help_message)

def get_emojis(word: str, synonyms: list) -> list:
    """Get relevant emojis based on word and its synonyms."""
    if emoji_data is None:
        logger.warning("Emoji data not available, returning default emojis")
        return ["🤔", "🔍", "✨"]
    
    try:
        # Create search terms from word and synonyms
        search_terms = [word] + synonyms
        
        # Search for matching emojis
        matching_emojis = emoji_data[
            emoji_data["Description"].str.contains('|'.join(search_terms), na=False, case=False)
        ]
        
        if not matching_emojis.empty:
            # Return top 3 emojis by sentiment score
            return list(matching_emojis.nlargest(3, "Sentiment score")["Emoji"])
        else:
            logger.info(f"No matching emojis found for: {word}")
            return list(emoji_data.nlargest(3, "Sentiment score")["Emoji"])
            
    except Exception as e:
        logger.error(f"Error in get_emojis: {e}")
        return ["🤔", "🔍", "✨"]

async def get_synonyms(word: str) -> list:
    """Get synonyms for a word using Datamuse API."""
    try:
        response = requests.get(
            f"https://api.datamuse.com/words",
            params={"rel_syn": word},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        return [item['word'] for item in data[:5]] if data else []
    except requests.RequestException as e:
        logger.error(f"Error fetching synonyms: {e}")
        return []

async def thesaurus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /thesaurus command."""
    # Check if a word was provided
    if not context.args:
        await update.message.reply_text(
            "Please provide a word after /thesaurus\n"
            "Example: /thesaurus happy"
        )
        return

    word = context.args[0].lower()
    logger.info(f"Processing thesaurus request for word: {word}")

    try:
        # Get synonyms
        synonyms = await get_synonyms(word)
        
        if not synonyms:
            await update.message.reply_text(
                f"Sorry, I couldn't find any synonyms for '{word}'."
            )
            return

        # Get emojis
        emojis = get_emojis(word, synonyms)

        # Format response
        synonyms_text = f"Synonyms for '{word}': {', '.join(synonyms)}"
        emoji_text = f"Matching emojis: {' '.join(emojis)}"
        
        # Send response
        await update.message.reply_text(
            f"{synonyms_text}\n\n{emoji_text}"
        )

    except Exception as e:
        logger.error(f"Error in thesaurus command: {e}")
        await update.message.reply_text(
            "Sorry, there was an error processing your request. Please try again."
        )