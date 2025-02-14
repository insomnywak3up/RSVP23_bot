# RSVP Bot

A Telegram bot designed to help users manage events by allowing them to create, view, edit, and cancel events. Users can also invite participants and confirm their attendance (RSVP).

## Features

- **Event Creation**: Users can create events by providing the name, date, and time.
- **View Events**: List all the events the user has created.
- **Edit Events**: Modify the date and time of an existing event.
- **Cancel Events**: Cancel an event that was created.
- **RSVP**: Confirm attendance or mark as unavailable for an event.
- **Invitations**: Send event invitations to participants with a Google Calendar link.
- **Reminders**: Automatic reminders for upcoming events.

## Requirements

- Python 3.7+
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [Google Calendar API](https://developers.google.com/calendar)
- A Telegram bot token (get yours from [BotFather](https://core.telegram.org/bots#botfather))

## Commands:
/start: Greets the user and provides information about the available commands.
/createevent: Begins the event creation process.
/myevents: Displays a list of the user's upcoming events.
/cancel <event_id>: Cancels an event by its ID.
/edit <event_id>: Edits the date and/or time of an event.
/invite: Sends invitations to participants via the Google Calendar link.
/rsvp <event_id> <yes/no/maybe>: Confirms attendance for an event.



## File Structure
bot.py: The main file that runs the bot.
config.py: Contains the bot token.
reminder.py: Handles event reminders.
rsvp.py: Manages the RSVP functionality.
invite.py: Manages event invitations.
events.py: Handles event creation, editing, and cancellation.

