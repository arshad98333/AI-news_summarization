import google.generativeai as genai
from config import GEMINI_API_KEY
import json

# Configure the Gemini API client
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def clean_json_response(text: str) -> str:
    """Cleans the typical Gemini response to extract pure JSON."""
    start = text.find('{')
    end = text.rfind('}') + 1
    if start != -1 and end != 0:
        return text[start:end]
    return text

def generate_summary_and_sentiment(article_content: str) -> dict:
    """Analyzes a single article for a summary, key points, and sentiment."""
    
    prompt = f"""
    You are an expert news analyst. Analyze the following article content and provide a structured JSON output.

    Your response MUST be a valid JSON object with the following keys:
    - "summary": A concise, neutral summary of the article (2-3 sentences).
    - "key_points": A JSON list of 3-5 string bullet points from the article. e.g., ["First key point.", "Second key point."].
    - "sentiment": The overall sentiment of the article (Positive, Negative, or Neutral).

    Article Content:
    ---
    {article_content[:8000]}
    ---

    JSON Output:
    """

    try:
        response = model.generate_content(prompt)
        cleaned_response = clean_json_response(response.text)
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"Gemini API error or JSON parsing failed: {e}")
        return {
            "summary": "Could not generate summary.",
            "key_points": [],
            "sentiment": "Unknown"
        }

def summarize_multiple_articles(articles: list) -> dict:
    """Synthesizes multiple articles into a single, comprehensive analysis."""
    
    formatted_articles = ""
    for i, article in enumerate(articles):
        formatted_articles += f"--- Article {i+1} from {article['url']} ---\n\n{article['content'][:3000]}\n\n"

    prompt = f"""
    You are a master news synthesizer. Analyze the following collection of articles on a similar topic. 
    Synthesize them into a single, comprehensive overview.

    Your response MUST be a valid JSON object with the following keys:
    - "overall_summary": A high-level synthesis of all articles (3-4 sentences).
    - "emerging_themes": A JSON list of 3-5 string bullet points that appear across the articles. e.g., ["First common theme.", "Second theme."].
    - "conflicting_reports": A brief note on any significant contradictions, if any.

    Article Collection:
    ---
    {formatted_articles}
    ---
    
    JSON Output:
    """

    try:
        response = model.generate_content(prompt)
        cleaned_response = clean_json_response(response.text)
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"Gemini multi-summary API error or JSON parsing failed: {e}")
        return {
            "overall_summary": "Could not synthesize articles.",
            "emerging_themes": [],
            "conflicting_reports": "Analysis failed."
        }