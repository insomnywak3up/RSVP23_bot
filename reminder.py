import threading
import time
from datetime import datetime

def schedule_reminder(bot, chat_id, event_name, event_time):
    def remind():
        try:
            # Расчет времени до напоминания (за 1 час до события)
            wait_time = (event_time - datetime.now()).total_seconds() - 3600
            print(f"Calculated wait_time for event '{event_name}': {wait_time} seconds")

            if wait_time > 0:
                time.sleep(wait_time)
                bot.send_message(chat_id, f"⏰ Reminder: '{event_name}' starts in 1 hour!")
            else:
                # Если до события меньше часа, отправляем напоминание сразу
                bot.send_message(chat_id, f"⚠️ Reminder: It's less than an hour until '{event_name}' starts!")
        except Exception as e:
            # Отладка ошибок
            print(f"Error in reminder thread for event '{event_name}': {e}")

    # Запуск напоминания в отдельном потоке
    thread = threading.Thread(target=remind, daemon=True)  # daemon=True для автоматического завершения
    thread.start()
