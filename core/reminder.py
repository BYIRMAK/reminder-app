class Reminder:
    def __init__(self, db):
        self.db = db

    def create(self, title, description, datetime, category, tags, repeat, priority, active):
        self.db.add_reminder(title, description, datetime, category, tags, repeat, priority, active)

    def update(self, reminder_id, title, description, datetime, category, tags, repeat, priority, active):
        self.db.update_reminder(reminder_id, title, description, datetime, category, tags, repeat, priority, active)

    def delete(self, reminder_id):
        self.db.delete_reminder(reminder_id)

    def get_all(self):
        return self.db.get_all_reminders()

    def get_by_id(self, reminder_id):
        return self.db.get_reminder(reminder_id)
