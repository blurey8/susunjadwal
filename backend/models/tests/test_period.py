import random

import pytest
from mongoengine import ValidationError

from models.major import Major
from models.period import ScheduleItem, Class, Course, Period
from .test_utils import TestBase


class TestScheduleItem(TestBase):
    def test_serialization_contains_required_keys(self):
        schedule_item = ScheduleItem(
            day="Monday",
            start="Start",
            end="End",
            room="Canteen",
        )

        serialized_schedule_item = schedule_item.serialize()
        self.assert_serialization_contains_keys(
            keys=["day", "start", "end", "room"],
            serialized_object=serialized_schedule_item,
        )

    def test_serialization_values(self):
        schedule_item = ScheduleItem(
            day="Monday",
            start="Start",
            end="End",
            room="Canteen",
        )

        serialized_schedule_item = schedule_item.serialize()

        assert serialized_schedule_item["day"] == schedule_item.day
        assert serialized_schedule_item["start"] == schedule_item.start
        assert serialized_schedule_item["end"] == schedule_item.end
        assert serialized_schedule_item["room"] == schedule_item.room

    def test_schedule_item_fields_validation(self):
        test_cases = [
            {"day": "Monday" * 10, "start": "Start", "end": "End", "room": "Room"},
            {"day": "Monday" * 10, "start": "Start" * 5, "end": "End", "room": "Room"},
            {
                "day": "Monday" * 10,
                "start": "Start" * 5,
                "end": "End" * 10,
                "room": "Room",
            },
            {
                "day": "Monday" * 10,
                "start": "Start" * 5,
                "end": "End" * 10,
                "room": "Room" * 20,
            },
        ]

        for case in test_cases:
            with pytest.raises(ValidationError):
                ScheduleItem(
                    day=case["day"],
                    start=case["start"],
                    end=case["end"],
                    room=case["room"],
                ).validate()


class TestClass(TestBase):
    @classmethod
    def generate_random_schedule_item(cls):
        return ScheduleItem(
            day=cls.get_random_string(16),
            start=cls.get_random_string(16),
            end=cls.get_random_string(16),
            room=cls.get_random_string(64),
        )

    def test_serialize_contains_required_keys(self):
        class_item = Class(
            name="Class",
            schedule_items=[self.generate_random_schedule_item()],
            lecturer=["John", "Troy"],
        )

        serialized_class_item = class_item.serialize()

        self.assert_serialization_contains_keys(
            keys=["name", "lecturer", "schedule_items"],
            serialized_object=serialized_class_item,
        )

    def test_serialize_with_empty_schedules(self):
        class_item = Class(
            name="Class",
            schedule_items=[],
            lecturer=["John", "Troy"],
        )

        serialized_class = class_item.serialize()

        assert serialized_class["name"] == class_item.name
        assert serialized_class["schedule_items"] == []
        assert serialized_class["lecturer"] == class_item.lecturer

    def test_serialize_with_schedules(self):
        class_item = Class(
            name="Class",
            schedule_items=[self.generate_random_schedule_item() for _ in range(10)],
            lecturer=["John", "Troy"],
        )

        serialized_class = class_item.serialize()

        assert serialized_class["name"] == class_item.name
        assert len(serialized_class["schedule_items"]) == len(class_item.schedule_items)
        for i in range(len(serialized_class["schedule_items"])):
            assert (
                serialized_class["schedule_items"][i]
                == class_item.schedule_items[i].serialize()
            )
        assert serialized_class["lecturer"] == class_item.lecturer

    def test_class_fields_validation(self):
        test_cases = [
            {
                "name": "Name" * 40,
                "schedule_items": [self.generate_random_schedule_item()],
                "lecturer": ["Smith"],
            },
            {"name": "Name" * 40, "schedule_items": 1, "lecturer": ["Smith"]},
            {"name": "Name" * 40, "schedule_items": 1, "lecturer": 2},
        ]

        for case in test_cases:
            with pytest.raises(ValidationError):
                Class(
                    name=case["name"],
                    schedule_items=case["schedule_items"],
                    lecturer=case["lecturer"],
                ).validate()


class TestCourse(TestBase):
    @classmethod
    def generate_random_class_item(cls):
        return Class(
            name=cls.get_random_string(128),
            schedule_items=[
                ScheduleItem(
                    day=cls.get_random_string(10),
                    start=cls.get_random_string(10),
                    end=cls.get_random_string(10),
                    room=cls.get_random_string(50),
                )
                for _ in range(10)
            ],
            lecturer=[cls.get_random_string(5) for _ in range(10)],
        )

    def test_serialization_contains_required_keys(self):
        course = Course(
            name="Course",
            credit=4,
            term=1,
            classes=[self.generate_random_class_item()],
        )

        serialized_course = course.serialize()

        self.assert_serialization_contains_keys(
            keys=["name", "credit", "term", "classes"],
            serialized_object=serialized_course,
        )

    def test_serialization_with_empty_classes(self):
        course = Course(
            name="Course",
            credit=4,
            term=1,
            classes=[],
        )

        serialized_course = course.serialize()

        assert serialized_course["name"] == course.name
        assert serialized_course["credit"] == course.credit
        assert serialized_course["term"] == course.term
        assert serialized_course["classes"] == []

    def test_serialization_with_classes(self):
        course = Course(
            name="Course",
            credit=4,
            term=1,
            classes=[self.generate_random_class_item() for _ in range(5)],
        )

        serialized_course = course.serialize()

        assert serialized_course["name"] == course.name
        assert serialized_course["credit"] == course.credit
        assert serialized_course["term"] == course.term
        for i in range(len(serialized_course["classes"])):
            assert serialized_course["classes"][i] == course["classes"][i].serialize()

    def test_course_fields_validation(self):
        test_cases = [
            {
                "name": "Name" * 40,
                "credit": 3,
                "term": 2,
                "classes": [self.generate_random_class_item()],
            },
            {
                "name": "Name" * 40,
                "credit": "3",
                "term": 2,
                "classes": [self.generate_random_class_item()],
            },
            {
                "name": "Name" * 40,
                "credit": "3",
                "term": "2",
                "classes": [self.generate_random_class_item()],
            },
            {"name": "Name" * 40, "credit": "3", "term": "2", "classes": 1},
        ]

        for case in test_cases:
            with pytest.raises(ValidationError):
                Course(
                    name=case["name"],
                    credit=case["credit"],
                    term=case["term"],
                    classes=case["classes"],
                ).validate()


class TestPeriod(TestBase):
    @classmethod
    def generate_random_major_item(cls):
        return Major(
            name=cls.get_random_string(256),
            kd_org=cls.get_random_string(16),
        )

    @classmethod
    def generate_random_class_item(cls):
        return Class(
            name=cls.get_random_string(128),
            schedule_items=[
                ScheduleItem(
                    day=cls.get_random_string(6),
                    start=cls.get_random_string(6),
                    end=cls.get_random_string(6),
                    room=cls.get_random_string(4),
                )
            ],
            lecturer=[cls.get_random_string(5)],
        )

    @classmethod
    def generate_random_course_item(cls):
        return Course(
            name=cls.get_random_string(128),
            credit=random.randint(0, 10),
            term=random.randint(0, 10),
            classes=[cls.generate_random_class_item() for _ in range(5)],
        )

    def test_period_creation(self):
        period = Period.objects().create(
            major_id=self.generate_random_major_item().save(),
            name="Period",
            is_detail=True,
            courses=[self.generate_random_course_item()],
        )

        periods = Period.objects
        assert len(periods) == 1

        fetched_period = periods().first()
        assert fetched_period.major_id == period.major_id
        assert fetched_period.name == "Period"
        assert fetched_period.is_detail
        assert fetched_period.courses == period.courses

        fetched_period.delete()

    def test_period_update(self):
        period = Period.objects().create(
            major_id=self.generate_random_major_item().save(),
            name="Period Name Old",
            is_detail=True,
            courses=[self.generate_random_course_item()],
        )

        new_major = self.generate_random_major_item().save()
        period.major_id = new_major
        period.name = "New Name"
        period.is_detail = False
        period.courses = []
        period.save()
        period.reload()

        assert period.major_id == new_major
        assert period.name == "New Name"
        assert not period.is_detail
        assert period.courses == []

        period.delete()

    def test_period_deletion(self):
        period = Period.objects().create(
            major_id=self.generate_random_major_item().save(),
            name="Period Name Old",
            is_detail=True,
            courses=[self.generate_random_course_item()],
        )

        assert len(Period.objects) == 1
        assert period in Period.objects

        period.delete()
        assert len(Period.objects) == 0
        assert period not in Period.objects

    def test_serialization_contains_required_keys(self):
        period = Period(
            major_id=None,
            name="Period A",
            is_detail=True,
            courses=[],
        )

        serialized_period = period.serialize()

        self.assert_serialization_contains_keys(
            keys=["name", "is_detail", "courses"], serialized_object=serialized_period
        )

    def test_serialize_with_empty_courses(self):
        period = Period(
            major_id=None,
            name="Period B",
            is_detail=True,
            courses=[],
        )

        serialized_period = period.serialize()

        assert serialized_period["name"] == period.name
        assert serialized_period["is_detail"] == period.is_detail
        assert serialized_period["courses"] == []

    def test_serialize_with_courses(self):
        period = Period(
            major_id=None,
            name="Period C",
            is_detail=True,
            courses=[self.generate_random_course_item() for _ in range(5)],
        )

        serialized_period = period.serialize()

        assert serialized_period["name"] == period.name
        assert serialized_period["is_detail"] == period.is_detail
        for i in range(len(serialized_period["courses"])):
            assert serialized_period["courses"][i] == period.courses[i].serialize()

    def test_period_fields_validation(self):
        course = self.generate_random_course_item()
        test_cases = [
            {"major_id": course, "name": "Name", "courses": [course]},
            {"major_id": course, "name": "Name" * 10, "courses": [course]},
            {"major_id": course, "name": "Name" * 10, "courses": [course]},
            {"major_id": course, "name": "Name" * 10, "courses": "Courses"},
        ]

        for case in test_cases:
            with pytest.raises(ValidationError):
                Period(
                    major_id=case["major_id"],
                    name=case["name"],
                    courses=case["courses"],
                ).save()
