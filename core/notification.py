from plyer import notification
import time

class NotificationManager:
    def __init__(self):
        pass

    def notify(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_name='Reminder App'
        )

    def schedule_notification(self, reminder):
        time_to_wait = (reminder.datetime - datetime.now()).total_seconds()
        time.sleep(time_to_wait)
        self.notify(reminder.title, reminder.message)
