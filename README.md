# Gemini News Summarizer AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced news aggregator and summarizer that leverages Selenium for dynamic web scraping and Google's Gemini AI for intelligent, multi-document analysis. The application features a user-friendly web interface built with Gradio.

![App Screenshot](https://raw.githubusercontent.com/Arshad0220/news-summarizer-ai/main/demo-screenshot.png)
*(Note: You will need to add your own screenshot named `demo-screenshot.png` to the repository for this image to display).*

## Features

-   **Dynamic Content Scraping**: Uses Selenium to control a real web browser, ensuring it can parse content from modern, JavaScript-heavy websites.
-   **Intelligent Summarization**: Powered by the Google Gemini API (`gemini-1.5-flash-latest`) for concise single-article summaries and insightful multi-article synthesis.
-   **Sentiment Analysis**: Automatically determines the sentiment (Positive, Negative, Neutral) of each news article.
-   **Duplicate Detection**: Intelligently identifies and filters out duplicate or highly similar articles before analysis to save time and API costs.
-   **Interactive Web UI**: A clean and responsive user interface built with Gradio for easy interaction.
-   **Bot Evasion**: Configured with common techniques to bypass basic bot detection systems.

## Tech Stack

-   **Backend**: Python 3.13+
-   **AI Model**: Google Gemini API
-   **Web Scraping**: Selenium, BeautifulSoup4
-   **UI Framework**: Gradio
-   **Configuration**: `python-dotenv` for environment variable management.

---

## Step-by-Step Execution Guide

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

-   [Python 3.13](https://www.python.org/downloads/) or later
-   [Git](https://git-scm.com/downloads) installed
-   A **Google Gemini API Key**. You can get one for free from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 1. Clone the Repository

Open your terminal or command prompt and clone this repository.

```bash
git clone https://github.com/Arshad0220/news-summarizer-ai.git
cd news-summarizer-ai
```

### 2. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

**On Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

Your terminal prompt should now be prefixed with `(venv)`.

### 3. Install Dependencies

Install all required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```
*Note: The first time you run the application, `webdriver-manager` will automatically download the correct version of ChromeDriver for your system.*

### 4. Configure Your API Key

The application loads your Gemini API Key from a `.env` file for security.

1.  In the root of the project folder, create a new file named `.env`.
2.  Open the `.env` file and add the following line, replacing `"YOUR_GEMINI_API_KEY_HERE"` with your actual key:

```ini
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```

### 5. Run the Application

You are now ready to launch the Gradio web interface.

```bash
python main.py
```

After a few moments, the terminal will display a local URL, typically `http://12.0.0.1:7860`. Open this URL in your web browser to use the News Summarizer AI.

---

## Project Structure

A brief overview of the key files in this project.

```
/news-summarizer-ai
├── .env                  # (Local Only) Stores your secret API key.
├── .gitignore            # Specifies files for Git to ignore (like .env and venv).
├── LICENSE               # The MIT License for the project.
├── README.md             # This documentation file.
├── requirements.txt      # List of Python package dependencies.
├── packages.txt          # System-level dependencies for Hugging Face deployment.
├── config.py             # Loads and validates the API key from .env.
├── main.py               # The main entry point; builds the Gradio UI.
├── scraper.py            # Contains the Selenium logic for dynamic web scraping.
├── summarizer.py         # Handles all API calls to Google Gemini.
└── utils.py              # Helper functions, such as duplicate detection.
```

## Deployment

This application is ready for deployment on services like Hugging Face Spaces. For deployment, a `packages.txt` file is required to instruct the server to install necessary system-level software for Selenium.

Create a file named `packages.txt` in the root of the project with the following content:

```text
chromium
libgl1
```

You can then use the `gradio deploy` command to push your application to a public Space.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.