rsvp_data = {}

def handle_rsvp(bot, message, events_data):
    chat_id = message.chat.id
    try:
        _, event_id, response = message.text.split()
        response = response.lower()
        if response not in ['yes', 'no', 'maybe']:
            bot.send_message(chat_id, "❌ Invalid response. Use yes, no, or maybe.")
            return
        if 'events' not in events_data or event_id not in events_data['events']:
            bot.send_message(chat_id, "❌ Invalid event ID.")
            return
        event = events_data['events'][event_id]
        event_creator_chat_id = event['chat_id']
        rsvp_data.setdefault(event_id, {})[chat_id] = response
        bot.send_message(chat_id, f"✅ Your RSVP '{response}' for event {event_id} is recorded.")
        bot.send_message(event_creator_chat_id, f"📬 {message.from_user.first_name} responded '{response}' to your event \"{event['name']}\".")
    except ValueError:
        bot.send_message(chat_id, "❌ Invalid format. Use /rsvp <event_id> <yes|no|maybe>.")
