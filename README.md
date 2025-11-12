
# telegram-db-helper

**A Telegram bot to search, log, and manage database entries.**

## Overview

`telegram-db-helper` is a lightweight Telegram bot designed to interact with your database directly from Telegram. It allows users to search records, log messages,and export data—all from within a chat interface.

The bot is ideal for small teams, admins, or anyone who wants to manage and query a database without leaving Telegram.

## Features

* 🔍 **Search Database:** Look up entries by name, index, or phone number using `/find`.
* 📝 **Logging:** Automatically logs all user messages and commands for audit or analytics purposes.
* 📤 **Export:** Export database data with `/export`.
* ✅ **Interactive Templates:** Conversation handlers with inline buttons for easy workflow.
* 🛠 **Lightweight and Extendable:** Easy to add more commands and features.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Abdulrahim-M/telegram-db-helper.git
cd telegram-db-helper
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up your database (SQLite/MySQL/PostgreSQL) and configure the connection in your code (in database folder).

5. Create a `config.py` file with your Telegram bot token, and database path:

```python
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
DB_PATH = "PATH/TO/YOUR/DATABASE" # if using SQLite
```


## Usage

Run the bot:

```bash
python bot.py
```

Available commands:

| Command                      | Description                               |
| ---------------------------- | ----------------------------------------- |
| `/start`                     | Show welcome message and instructions     |
| `/find <query>`              | Search database by name, index, or phone  |
| `/export`                    | Export database records                   |
| `/template`                  | Interactive templates with inline buttons |

All messages and commands sent to the bot are logged for auditing.

## Contributing

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Add feature"`
4. Push to the branch: `git push origin feature-name`
5. Open a Pull Request

## License

MIT License © Abdulrahim-M