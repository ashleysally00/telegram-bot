import requests
import logging
from telegram import Update
from telegram.ext import ContextTypes
from emojis import EmojiMatcher

# Initialize emoji matcher
emoji_matcher = EmojiMatcher("Emoji_Sentiment_Data_v1.0.csv")

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

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

        # Get emojis using the improved emoji matcher
        emojis = emoji_matcher.get_emojis(word, synonyms)

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
