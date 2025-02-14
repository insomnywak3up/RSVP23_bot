def list_events(chat_id, events_data):
    """Lists events for a specific chat ID."""
    if chat_id not in events_data:
        return []
    user_events = []
    for event_id, event in events_data['events'].items():
        if event['chat_id'] == chat_id:
            user_events.append(event)
    return user_events

def cancel_event(chat_id, event_id, events_data):
    """Cancels an event by ID if the chat ID matches the event creator."""
    if 'events' in events_data and event_id in events_data['events']:
        event = events_data['events'][event_id]
        if event['chat_id'] == chat_id:
            del events_data['events'][event_id]
            return True
    return False

def edit_event(chat_id, event_id, new_date, new_time, events_data):
    """Edits an event's date and time if the chat ID matches the event creator."""
    if 'events' in events_data and event_id in events_data['events']:
        event = events_data['events'][event_id]
        if event['chat_id'] == chat_id:
            event['date'] = new_date
            event['time'] = new_time
            return True
    return False
