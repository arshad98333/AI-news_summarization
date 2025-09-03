from difflib import SequenceMatcher

def is_duplicate(text1: str, text2: str, threshold: float = 0.85) -> bool:
    """
    Checks if two texts are semantically similar using SequenceMatcher.
    A ratio > threshold indicates a likely duplicate.
    """
    if not text1 or not text2:
        return False
    
    ratio = SequenceMatcher(None, text1, text2).ratio()
    return ratio > threshold