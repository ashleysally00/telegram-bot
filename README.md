# Thesaurus Bot with Emoji Sentiment Analysis 🤖☀️☁️ 💖

Thesaurus Bot is a Telegram bot that allows users to find synonyms for a given word along with relevant emojis. The emojis are dynamically selected based on their sentiment score from the **Emoji Sentiment Dataset**.

The Emoji Sentiment Dataset used in this project is sourced from:

- **P. Kralj Novak, J. Smailović, B. Sluban, I. Mozetič**, "Emoji Sentiment Ranking," PLOS ONE, 2015.
- Dataset: [Emoji Sentiment Ranking](http://hdl.handle.net/11356/1054)

---

## Thesaurus Bot Snapshot

Below is a snapshot of the Thesaurus Bot working on Telegram, showing its chatbot-like interface:
<img src="https://github.com/ashleysally00/telegram-bot/blob/main/thesaurus-bot.png?raw=true" width="70%" alt="Thesaurus Bot in Action">

## Features

- **Synonym Finder**: Get up to 5 synonyms for a given word using the Datamuse API.
- **Emoji Suggestions**: Suggest emojis that match the sentiment and context of the input word (default emojis are returned in this version).
- **User-Friendly Commands**: Easy-to-use commands with clear instructions for users.

---

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- A Telegram bot token (obtainable via [BotFather](https://core.telegram.org/bots#botfather))
- Required Python libraries: `python-telegram-bot`, `requests`, `pandas`, `python-dotenv`

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/ashleysally00/telegram-bot
   cd thesaurus-bot
   ```

## Try the Bot Online 🤖

Click the link below to test the bot on Telegram:
[Test the Thesaurus Bot](https://t.me/YourBotUsername)

**Important:** The online link will only work when the bot is running on my local machine. If the bot is unavailable, please follow the installation instructions above to set up and run your own instance of the bot.
