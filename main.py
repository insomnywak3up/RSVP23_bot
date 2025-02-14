from bot import get_bot
if __name__ == "__main__":
    bot = get_bot()  # Get the bot instance from bot.py
    print("Bot is running...")
    bot.polling(none_stop=True)