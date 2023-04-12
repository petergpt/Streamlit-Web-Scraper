# URL Summarizer

URL Summarizer is a Python application that uses the GPT-4 model to generate a summary and sentiment analysis of a given URL or keyword. It supports two modes of operation: direct URL input/keyword or selection from a list of pre-listed UK news websites.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Core Files](#core-files)
- [Dependencies](#dependencies)
- [License](#license)
- [Contribution](#contribution)
- [Prerequisites](#prerequisites)
- [Testing and Development](#testing-and-development)
- [Troubleshooting](#troubleshooting)
- [Credits and References](#credits-and-references)

## Installation

1. Clone the repository

```
git clone https://github.com/petergpt/Streamlit-Web-Scraper
```

2. Install the required packages
```
pip install -r requirements.txt
```

## Usage

1. Set your OpenAI API key as an environment variable:
```
export OPENAI_API_KEY="your-api-key"
```

2. Run the Streamlit app:
```
streamlit run app.py
```

3. Open the Streamlit app in your browser at `http://localhost:8501`.

## Core Files

### app.py

The main file that handles user input and integrates the functionality provided by `helpers.py`.

- Imports required modules and helper functions
- `get_generated_url(prompt)`: Generates a URL based on the user's input using GPT-4
- Uses Streamlit to create a user interface, accept inputs, and display the summary and sentiment analysis

### helpers.py

This file contains helper functions for web scraping, sentiment analysis, and summarizing text.

- `format_url(url)`: Formats the URL to include the scheme if not provided
- `scrape_website(url)`: Scrapes the content of the given URL
- `get_sentiment(text)`: Returns the sentiment analysis of the text using GPT-4
- `get_summary(text)`: Returns a summary of the text using GPT-4

## Dependencies

- Python 3.8 or higher
- Streamlit
- Requests
- BeautifulSoup4
- OpenAI API

## License

This project is licensed under the MIT License.

## Contribution

Contributions are welcome! Please submit a pull request or create an issue to discuss proposed changes.

## Prerequisites

Before using this project, please ensure you have the following:

- Python 3.8 or higher
- An OpenAI API key

## Testing and Development

The easiest way to set up a development environment is to import this Git repository into [Replit](https://replit.com/), a collaborative online code editor and runtime.

## Troubleshooting

Some known issues and solutions include:

- If the amount of text scraped from the website exceeds the max token length (8,000 tokens), the summarization will not work on the OpenAI side. To resolve this, you may need to truncate or split the text before sending it to the OpenAI API.

Please report any additional issues you encounter by creating an issue on the GitHub repository.

## Credits and References

This project utilizes open-source libraries and tools, including:

- Streamlit
- Requests
- BeautifulSoup4
- OpenAI API

Special thanks to [Replit](https://replit.com/) for providing a convenient online development environment.