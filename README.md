# 🚀 Telegram Pro Cleaner

A high-performance, asynchronous CLI tool built with Python and Telethon. This utility is designed to help users manage their Telegram accounts by bulk-leaving groups/channels and removing stubborn "ghost" chats or bots that clutter the chat list.

## ✨ Key Features
* **Ghost Buster:** Force-removes "Ghost" chats that display the "No messages here yet" screen.
* **Bot Banisher:** Automatically blocks and removes bots to prevent them from staying in your active dialogs.
* **Nuclear Mode:** A "Wipe All" feature to clear your entire account list in one session.
* **Folder Targeting:** Clean specific chat folders (e.g., a "Delete" folder) while leaving others untouched.
* **Dynamic Whitelist:** Protect important contacts, family, or work groups by @username, Title, or ID via the terminal.
* **Flood Protection:** Built-in asynchronous delays to respect Telegram's rate limits and prevent account cooling periods.

## 🛠️ Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/yourusername/telegram-cleaner.git](https://github.com/yourusername/telegram-cleaner.git)
    cd telegram-cleaner
    ```

2.  **Install Requirements:**
    ```bash
    pip install telethon python-dotenv colorama
    ```

3.  **Environment Configuration:**
    Create a file named `.env` in the root directory (see the "How to get API Hashes" section below).
    ```text
    TG_API_ID=your_id_here
    TG_API_HASH=your_hash_here
    ```

4.  **Run the Tool:**
    ```bash
    python main.py
    ```

## 🔑 How to get API Hashes

To use this tool, you must register an application on the Telegram API platform. **Warning: Never share your Hash or Session files with anyone.**

1.  Log in to your Telegram account at [https://my.telegram.org](https://my.telegram.org).
2.  Go to **"API development tools"**.
3.  Fill out the form to create a new application (e.g., Title: `AccountManager`, Short Name: `tgclean`).
4.  Copy the `App api_id` and `App api_hash` into your `.env` file.

## 📋 Usage Guide
* **Whitelist:** When prompted, enter names or @usernames separated by commas (e.g., `Mom, @WorkGroup, MyBestFriend`).
* **Confirmation:** For safety, "Nuclear Mode" requires you to type `CONFIRM` in all caps to prevent accidental wipes.
* **Session File:** On the first run, you will be asked for your phone number and login code. This creates a `tg_cleaner_pro.session` file. Do not delete this unless you want to log in again.

## ⚠️ Disclaimer
This tool is provided for educational and personal management purposes. Mass-deleting chats can be flagged by Telegram if done too frequently. The developers are not responsible for any accidental loss of data. Use the **Whitelist** feature diligently.

---
*Clean your digital space, clear your mind.*