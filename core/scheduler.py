import threading
import time

class Scheduler:
    def __init__(self):
        self.reminders = []

    def add_reminder(self, reminder):
        self.reminders.append(reminder)
        threading.Thread(target=self.schedule_reminder, args=(reminder,)).start()

    def schedule_reminder(self, reminder):
        time_to_wait = (reminder.datetime - datetime.now()).total_seconds()
        time.sleep(max(0, time_to_wait))
        reminder.notify()
