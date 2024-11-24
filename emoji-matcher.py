import pandas as pd
import logging
from typing import List, Optional

class EmojiMatcher:
    def __init__(self, csv_path: str = "Emoji_Sentiment_Data_v1.0.csv"):
        self.logger = logging.getLogger(__name__)
        self.emoji_data = self._load_emoji_data(csv_path)
        self.default_emojis = ["🤔", "🔍", "✨"]

    def _load_emoji_data(self, csv_path: str) -> Optional[pd.DataFrame]:
        """Load and validate the emoji CSV data."""
        try:
            df = pd.read_csv(csv_path, encoding="utf-8")
            required_columns = {"Unicode name", "Emoji", "Positive"}
            
            if not all(col in df.columns for col in required_columns):
                self.logger.error(f"Missing required columns. Found: {df.columns}")
                return None
                
            # Clean up descriptions and convert to lowercase
            df["Unicode name"] = df["Unicode name"].fillna("").str.lower()
            return df
            
        except Exception as e:
            self.logger.error(f"Failed to load emoji data: {str(e)}")
            return None

    def get_emojis(self, word: str, synonyms: List[str], limit: int = 3) -> List[str]:
        """
        Get relevant emojis based on word and synonyms.
        Returns default emojis if no matches or errors occur.
        """
        if self.emoji_data is None:
            self.logger.warning("Emoji data not available")
            return self.default_emojis[:limit]

        try:
            word = word.lower()
            synonyms = [syn.lower() for syn in synonyms]
            search_terms = [word] + synonyms

            # First try exact matches
            exact_matches = self.emoji_data[
                self.emoji_data["Unicode name"].apply(
                    lambda x: any(term in x.split() for term in search_terms)
                )
            ]

            # If no exact matches, try partial matches
            if exact_matches.empty:
                partial_matches = self.emoji_data[
                    self.emoji_data["Unicode name"].str.contains(
                        '|'.join(search_terms), 
                        case=False, 
                        regex=True,
                        na=False
                    )
                ]
                
                if not partial_matches.empty:
                    self.logger.info(f"Found partial matches for: {word}")
                    matching_emojis = partial_matches
                else:
                    self.logger.info(f"No matches found for: {word}")
                    return self.default_emojis[:limit]
            else:
                self.logger.info(f"Found exact matches for: {word}")
                matching_emojis = exact_matches

            # Get top emojis by sentiment score
            result = list(
                matching_emojis.nlargest(limit, "Positive")["Emoji"]
            )

            # Pad with defaults if we don't have enough matches
            if len(result) < limit:
                result.extend(self.default_emojis[:(limit - len(result))])

            return result

        except Exception as e:
            self.logger.error(f"Error getting emojis for {word}: {str(e)}")
            return self.default_emojis[:limit]
