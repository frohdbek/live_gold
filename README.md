📈 Gold Momentum & Price Drop Tracker
This is an automated Python bot that tracks gold prices (specifically Ziraat Bank Gram Gold) and sends real-time Telegram notifications when a price drop occurs. Unlike standard trackers, this bot doesn't rely on a fixed target price; instead, it compares the current price with the previous hour's data to catch downward trends.

🚀 How It Works
The bot operates on a Zero-Infrastructure Hafıza (Memory) principle using GitHub Actions:

Automated Execution: Runs every hour via GitHub Actions (CRON job).

Scraping: Fetches live gold prices from financial sources using BeautifulSoup.

State Persistence: * The bot reads the "last known price" from a local file named last_price.txt.

It compares the Live Price with the Cached Price.

Smart Alerting: * If the price is lower than the previous hour, it triggers a Telegram alert with the exact drop amount.

If the price is higher or stable, it remains silent to prevent notification fatigue.

Self-Updating Memory: The bot automatically commits and pushes the updated price back to the GitHub repository, effectively using the repo as a lightweight database.

🛠️ Technical Stack
Language: Python 3.x

Libraries: Requests, BeautifulSoup4

Automation: GitHub Actions (CI/CD)

Database: Local .txt file persistence via Git commits.

Communication: Telegram Bot API

⚙️ Setup & Environment Variables
To keep the bot secure, the following secrets must be added to your GitHub Repository:

TELEGRAM_TOKEN: Your Telegram Bot API token.

CHAT_ID: Your personal Telegram chat ID.

💡 Why This Approach?
Most free bots lose their memory after every run because GitHub Actions environments are ephemeral. This bot overcomes that limitation by auto-committing its state, ensuring it always knows what the price was an hour ago without requiring a paid SQL database or a VPS.

🛠️ Installation for Personal Use
Fork this repository.

Add your TELEGRAM_TOKEN and CHAT_ID to Settings > Secrets and variables > Actions.

Enable Actions in the Actions tab.

The bot will automatically create last_price.txt on its first run and begin tracking.
