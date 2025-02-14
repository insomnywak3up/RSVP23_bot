import telebot
from datetime import datetime
from reminder import schedule_reminder  # Import reminders
from config import BOT_TOKEN  # Bot token
from rsvp import handle_rsvp  # RSVP handler
from invite import generate_event_link, generate_event_id_and_store, invite_participants  # Invitation functions
from events import list_events, cancel_event, edit_event  # Event listing, cancellation, and editing

class RSVPBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.events_data = {'events': {}}  # Initialize with 'events' key
        self.setup_handlers()

    def setup_handlers(self):
        # Set up the command handlers
        self.bot.message_handler(commands=['start'])(self.welcome)
        self.bot.message_handler(commands=['createevent'])(self.create_event)
        self.bot.message_handler(commands=['myevents'])(self.my_events_command)
        self.bot.message_handler(commands=['cancel'])(self.cancel_event_command)
        self.bot.message_handler(commands=['edit'])(self.edit_event_command)
        self.bot.message_handler(commands=['invite'])(self.invite_command)
        self.bot.message_handler(commands=['rsvp'])(self.rsvp_command)

    def welcome(self, message):
        """Sends a welcome message with bot instructions."""
        self.bot.send_message(
            message.chat.id,
            f"👋 Hello, {message.from_user.first_name}! I am the <b>RSVP</b> bot to help you manage events.\n\n"
            "📅 <b>Features:</b> \n"
            "✔️ Create an event (/createevent)\n"
            "✔️ View my events (/myevents)\n"
            "✔️ Confirm attendance (/rsvp ID yes/no/maybe)\n"
            "✔️ Cancel an event (/cancel ID)\n"
            "✔️ Edit an event's date and time (/edit ID)\n"
            "🚀 <em>Start with /createevent!</em>",
            parse_mode='html'
        )

    def create_event(self, message):
        """Starts the event creation process."""
        chat_id = message.chat.id
        self.events_data[chat_id] = {}  # Initialize data for the event
        self.bot.send_message(chat_id, "📋 What is the name of the event?")
        self.bot.register_next_step_handler(message, self.set_event_name)

    def set_event_name(self, message):
        """Saves the event name and asks for the date."""
        chat_id = message.chat.id
        self.events_data[chat_id]['name'] = message.text
        self.bot.send_message(chat_id, "📅 Enter the date of the event (format: YYYY-MM-DD):")
        self.bot.register_next_step_handler(message, self.set_event_date)

    def set_event_date(self, message):
        """Saves the event date and asks for the time."""
        chat_id = message.chat.id
        try:
            date = datetime.strptime(message.text, "%Y-%m-%d").date()
            self.events_data[chat_id]['date'] = date
            self.bot.send_message(chat_id, "⏰ Enter the time of the event (format: HH:MM):")
            self.bot.register_next_step_handler(message, self.set_event_time)
        except ValueError:
            self.bot.send_message(chat_id, "❌ Invalid date format. Use YYYY-MM-DD.")
            self.bot.register_next_step_handler(message, self.set_event_date)

    def set_event_time(self, message):
        """Saves the event time and creates a link to Google Calendar."""
        chat_id = message.chat.id
        try:
            time = datetime.strptime(message.text, "%H:%M").time()
            self.events_data[chat_id]['time'] = time

            event_name = self.events_data[chat_id]['name']
            event_date = self.events_data[chat_id]['date']
            event_time = self.events_data[chat_id]['time']
            event_start_time = datetime.combine(event_date, event_time)

            # Generate event ID
            event_id = generate_event_id_and_store(chat_id, self.events_data)

            # Schedule reminder
            schedule_reminder(chat_id, event_name, event_start_time, self.bot)

            # Generate event link
            event_link = generate_event_link(event_name, event_start_time)

            # Send event creation confirmation to the user
            self.bot.send_message(
                chat_id,
                f"✅ Event \"{event_name}\" created!\n"
                f"📆 {event_date} at {event_time}\n"
                f"🔔 Reminder set!\n"
                f"📋 Event ID: {event_id}\n"
                f"🌍 <a href='{event_link}'>View in Google Calendar</a>",
                parse_mode="HTML"
            )
        except ValueError:
            self.bot.send_message(chat_id, "❌ Invalid time format. Use HH:MM.")
            self.bot.register_next_step_handler(message, self.set_event_time)

    def my_events_command(self, message):
        """Handles the 'myevents' command to show upcoming events."""
        chat_id = message.chat.id
        events = list_events(chat_id, self.events_data)
        if not events:
            self.bot.send_message(chat_id, "❌ No upcoming events found.")
        else:
            message_text = "📅 Your upcoming events:\n"
            for event in events:
                message_text += f"ID: {event['id']}\n"
                message_text += f"Name: {event['name']}\n"
                message_text += f"Date: {event['date']}\n"
                message_text += f"Time: {event['time']}\n"
                message_text += "----------------------\n"
            self.bot.send_message(chat_id, message_text)

    def cancel_event_command(self, message):
        """Handles the 'cancel' command to cancel an event."""
        chat_id = message.chat.id
        try:
            _, event_id = message.text.split()
            result = cancel_event(chat_id, event_id, self.events_data)
            if result:
                self.bot.send_message(chat_id, f"✅ Event {event_id} has been canceled.")
            else:
                self.bot.send_message(chat_id, "❌ Invalid event ID or you don't have permission to cancel this event.")
        except ValueError:
            self.bot.send_message(chat_id, "❌ Invalid format. Use /cancel <event_id>.")

    def edit_event_command(self, message):
        """Handles the 'edit' command to edit event details."""
        chat_id = message.chat.id
        try:
            _, event_id = message.text.split()
            if event_id in self.events_data['events'] and self.events_data['events'][event_id]['chat_id'] == chat_id:
                self.bot.send_message(chat_id, "📅 Enter the new date of the event (format: YYYY-MM-DD):")
                self.bot.register_next_step_handler(message, self.set_new_event_date, event_id)
            else:
                self.bot.send_message(chat_id, "❌ Invalid event ID or you don't have permission to edit this event.")
        except ValueError:
            self.bot.send_message(chat_id, "❌ Invalid format. Use /edit <event_id>.")

    def set_new_event_date(self, message, event_id):
        """Saves the new event date and asks for the new time."""
        chat_id = message.chat.id
        try:
            date = datetime.strptime(message.text, "%Y-%m-%d").date()
            self.events_data['events'][event_id]['date'] = date
            self.bot.send_message(chat_id, "⏰ Enter the new time of the event (format: HH:MM):")
            self.bot.register_next_step_handler(message, self.set_new_event_time, event_id)
        except ValueError:
            self.bot.send_message(chat_id, "❌ Invalid date format. Use YYYY-MM-DD.")
            self.bot.register_next_step_handler(message, self.set_new_event_date, event_id)

    def set_new_event_time(self, message, event_id):
        """Saves the new event time and updates the event."""
        chat_id = message.chat.id
        try:
            time = datetime.strptime(message.text, "%H:%M").time()
            self.events_data['events'][event_id]['time'] = time

            event = self.events_data['events'][event_id]
            event_name = event['name']
            event_date = event['date']
            event_time = event['time']
            event_start_time = datetime.combine(event_date, event_time)

            # Generate new event link
            event_link = generate_event_link(event_name, event_start_time)

            # Update reminder
            schedule_reminder(chat_id, event_name, event_start_time, self.bot)

            # Send updated event details to the user
            self.bot.send_message(
                chat_id,
                f"✅ Event \"{event_name}\" updated!\n"
                f"📆 New date: {event_date} at {event_time}\n"
                f"🔔 Reminder updated!\n"
                f"🌍 <a href='{event_link}'>View in Google Calendar</a>",
                parse_mode="HTML"
            )
        except ValueError:
            self.bot.send_message(chat_id, "❌ Invalid time format. Use HH:MM.")
            self.bot.register_next_step_handler(message, self.set_new_event_time, event_id)

    def invite_command(self, message):
        """Handles the 'invite' command to invite participants."""
        invite_participants(self.bot, message, self.events_data)

    def rsvp_command(self, message):
        """Handles the 'rsvp' command to confirm attendance."""
        handle_rsvp(self.bot, message, self.events_data)

    def run(self):
        """Runs the bot."""
        print("Bot is running...")
        self.bot.infinity_polling()

def get_bot():
    return RSVPBot(BOT_TOKEN).bot

if __name__ == "__main__":
    rsvp_bot = RSVPBot(BOT_TOKEN)
    rsvp_bot.run()
