import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class DynamicScraper:
    """A web scraper using Selenium to handle JavaScript-rendered content and bypass bot detection."""

    def __init__(self):
        print("Initializing Selenium WebDriver...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run browser in the background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled") # Key for bot evasion
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        print("WebDriver initialized.")

    def scrape_url(self, url: str) -> dict:
        """Fetches and parses the content of a given URL."""
        try:
            self.driver.get(url)
            # Wait for dynamic JavaScript content to load
            time.sleep(5) # A simple wait; can be replaced with more sophisticated WebDriverWait

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            title = soup.title.string if soup.title else "No Title Found"

            # Remove irrelevant tags for cleaner text extraction
            for element in soup(["script", "style", "nav", "header", "footer", "aside", "form"]):
                element.decompose()
            
            text = soup.get_text(separator='\n', strip=True)

            return {"url": url, "title": title, "content": text}
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return {"url": url, "title": "Error", "content": f"Failed to scrape content. {e}"}

    def close(self):
        """Closes the WebDriver."""
        print(" shutting down WebDriver.")
        self.driver.quit()