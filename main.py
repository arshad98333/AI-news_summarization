import gradio as gr
from scraper import DynamicScraper
from summarizer import generate_summary_and_sentiment, summarize_multiple_articles
from utils import is_duplicate
import time

# --- Main processing logic as a generator function for live UI updates ---
def process_and_analyze(url_input: str):
    """
    Scrapes, de-duplicates, and analyzes a list of URLs, yielding updates to the UI.
    """
    urls = [url.strip() for url in url_input.split('\n') if url.strip()]
    if not urls:
        yield "Status: Please enter at least one URL.", None, gr.update(visible=False), gr.update(visible=False)
        return

    yield "Status: Starting...", "", gr.update(visible=True), gr.update(visible=False)

    # --- 1. Scraping Phase ---
    yield "Status: Initializing scraper...", "", gr.update(visible=True), gr.update(visible=False)
    scraped_articles = []
    scraper = DynamicScraper()
    for i, url in enumerate(urls):
        status_update = f"Status: Scraping URL {i+1}/{len(urls)}: {url.split('//')[-1].split('/')[0]}"
        yield status_update, "", gr.update(visible=True), gr.update(visible=False)
        scraped_articles.append(scraper.scrape_url(url))
    scraper.close()
    yield "Status: Scraping complete. Analyzing for duplicates...", "", gr.update(visible=True), gr.update(visible=False)

    # --- 2. De-duplication Phase ---
    unique_articles = []
    if scraped_articles:
        if scraped_articles[0]['content']:
            unique_articles.append(scraped_articles[0])
        for article in scraped_articles[1:]:
            if not article['content']:
                continue
            is_dup = any(is_duplicate(article['content'], unique_article['content']) for unique_article in unique_articles)
            if not is_dup:
                unique_articles.append(article)
    
    num_duplicates = len(scraped_articles) - len(unique_articles)
    yield f"Status: Found and removed {num_duplicates} duplicate(s). Now summarizing...", "", gr.update(visible=True), gr.update(visible=False)
    time.sleep(1)

    # --- 3. Summarization Phase ---
    final_markdown = ""
    if not unique_articles:
        final_markdown = "### No unique articles with content could be processed."

    elif len(unique_articles) == 1:
        article = unique_articles[0]
        yield f"Status: Analyzing single article...", "", gr.update(visible=True), gr.update(visible=False)
        result = generate_summary_and_sentiment(article['content'])
        
        final_markdown = f"## Analysis of: [{article['title']}]({article['url']})\n"
        final_markdown += f"**Sentiment:** `{result.get('sentiment', 'N/A')}`\n\n"
        final_markdown += f"### Summary\n{result.get('summary', 'No summary available.')}\n\n"
        final_markdown += "### Key Points\n"
        key_points = result.get('key_points', [])
        if key_points:
            for point in key_points:
                final_markdown += f"- {point}\n"
        else:
            final_markdown += "No key points generated."

    else:
        yield f"Status: Synthesizing {len(unique_articles)} articles...", "", gr.update(visible=True), gr.update(visible=False)
        result = summarize_multiple_articles(unique_articles)

        final_markdown = f"## Synthesized Analysis of {len(unique_articles)} Articles\n"
        final_markdown += f"### Overall Summary\n{result.get('overall_summary', 'No summary available.')}\n\n"
        final_markdown += "### Emerging Themes\n"
        emerging_themes = result.get('emerging_themes', [])
        if emerging_themes:
            for theme in emerging_themes:
                final_markdown += f"- {theme}\n"
        else:
            final_markdown += "No emerging themes were identified.\n\n"
            
        final_markdown += f"\n### Conflicting Reports\n{result.get('conflicting_reports', 'None specified.')}"

    yield "Status: Analysis Complete!", final_markdown, gr.update(visible=False), gr.update(visible=True)


# --- Inline CSS for business-class UI/UX ---
custom_css = """
#title {
    font-size: 2rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 10px;
    color: #1a1a1a;
    letter-spacing: 0.5px;
    animation: fadeIn 1.2s ease-in-out;
}
#subtitle {
    font-size: 1.1rem;
    text-align: center;
    color: #444;
    margin-bottom: 30px;
    max-width: 850px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.6;
    animation: slideUp 1.2s ease-in-out;
}
.loader-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}
.loader {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #007bff;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    animation: spin 1s linear infinite;
}
#results-box {
    padding: 20px;
    background: #fafafa;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.06);
    animation: fadeIn 1s ease-in-out;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
"""

# --- Gradio UI Definition ---
with gr.Blocks(css=custom_css, theme=gr.themes.Soft(primary_hue="blue", secondary_hue="sky")) as demo:
    gr.Markdown("<div id='title'>AI-Powered Global News Scraper & Summarizer</div>")
    gr.Markdown(
        """
        <div id='subtitle'>
        One of the most powerful AI-driven news scrapers.
        Extract insights from the top global news websites like <b>BBC News</b>, <b>CNN</b>,
        <b>Reuters</b>, <b>The New York Times</b>, and <b>Al Jazeera</b>.
        Automatically remove duplicates, and receive accurate, unified summaries powered by
        <b>Google Intelligence LLM</b>.
        Designed for professionals, researchers, and businesses that demand real-time, reliable news analysis.
        </div>
        """
    )
    
    with gr.Row():
        url_input = gr.Textbox(
            lines=5,
            label="Enter News Article URLs (one per line)",
            placeholder="https://www.example.com/news-story-1\nhttps://www.anothersite.com/related-story-a"
        )
    
    with gr.Row():
        analyze_btn = gr.Button("Analyze Articles", variant="primary")

    with gr.Column():
        status_box = gr.Textbox(label="Progress Status", interactive=False)
        loader = gr.HTML("""
            <div class="loader-container">
                <div class="loader"></div>
            </div>
        """, visible=False)
        results_markdown = gr.Markdown(elem_id="results-box", visible=False)

    analyze_btn.click(
        fn=process_and_analyze,
        inputs=[url_input],
        outputs=[status_box, results_markdown, loader, results_markdown]
    )

if __name__ == "__main__":
    demo.launch(share=True)
