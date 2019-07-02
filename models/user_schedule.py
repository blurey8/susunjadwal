import mongoengine as mongo
from datetime import datetime


class ScheduleItem(mongo.EmbeddedDocument):
    name = mongo.StringField()
    day = mongo.StringField()
    room = mongo.StringField()
    start = mongo.StringField()
    end = mongo.StringField()

    def serialize(self):
        return {
            "name": self.name,
            "day": self.day,
            "room": self.room,
            "start": self.start,
            "end": self.end
        }


class UserSchedule(mongo.Document):
    user_id = mongo.ReferenceField("User")
    schedule_items = mongo.ListField(mongo.EmbeddedDocumentField(ScheduleItem))
    deleted = mongo.BooleanField(default=False)
    created_at = mongo.DateTimeField(default=datetime.now)

    def add_schedule_item(self, **kwargs):
        data = ScheduleItem(**kwargs)
        self.schedule_items.append(data)
        return data

    def __get_schedule_items(self):
        data = []
        for item in self.schedule_items:
            data.append(item.serialize())
        return data

    def serialize(self):
        return {
            "id": str(self.id),
            "created_at": self.created_at,
            "schedule_items": self.__get_schedule_items()
        }