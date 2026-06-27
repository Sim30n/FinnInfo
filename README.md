# FinnInfo — Stock News Sentiment Analyzer

Analyze the sentiment of recent news articles for any stock ticker using the Finnhub API and OpenAI GPT, surfaced through a simple Streamlit interface.

**[Read the full write-up on Medium](https://medium.com/@petteri.sarkka/build-a-stock-news-sentiment-analyzer-with-python-streamlit-gpt-and-finnhub-bcb770223945)**

---

## How it works

1. Fetches the last 24 hours of company news from **Finnhub**
2. Sends each article's summary to **GPT** with a financial analyst prompt
3. GPT classifies each article as Positive, Negative, or Neutral
4. The app calculates a sentiment score scaled from -100 to +100
5. A final GPT call produces a concise investor-focused summary of all the news

## Demo

Enter any stock ticker (e.g. `NVDA`, `MSFT`, `AAPL`) and the app returns:

- Positive / Negative / Neutral article counts
- A sentiment score between -100 and +100
- A 5-sentence summary of the day's news

## Setup

### Prerequisites

- Python 3.9+
- A [Finnhub](https://finnhub.io/) API key (free tier works)
- An [OpenAI](https://platform.openai.com/) API key

### Install dependencies

```bash
pip install streamlit finnhub-python openai python-dotenv
```

### Configure API keys

Create a `.env` file in the project root:

```
FINNHUB_API_KEY=your_finnhub_key_here
OPENAI_API_KEY=your_openai_key_here
```

## Running the app

```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

## Project structure

```
FinnInfo/
├── app.py            # Streamlit UI
├── NewsAnalyzer.py   # Finnhub + GPT logic
├── .env              # API keys (not committed)
└── .gitignore
```

## Running without Streamlit

`NewsAnalyzer.py` can also be run directly as a script:

```bash
python NewsAnalyzer.py
```

Edit the `company_symbol` variable near the bottom of the file to change the ticker.
