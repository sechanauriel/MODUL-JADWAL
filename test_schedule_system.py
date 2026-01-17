"""
Unit Tests for Schedule Management System
Tests all core functionality: CRUD, Conflict Detection, Observer Pattern
"""

import unittest
from datetime import datetime, time
from schedule_system import *


class TestTimeSlot(unittest.TestCase):
    """Test TimeSlot class"""

    def test_time_slot_overlap_yes(self):
        """Test that overlapping time slots are detected"""
        slot1 = TimeSlot(time(8, 0), time(10, 0))
        slot2 = TimeSlot(time(9, 0), time(11, 0))
        self.assertTrue(slot1.overlaps_with(slot2))

    def test_time_slot_overlap_no(self):
        """Test that non-overlapping time slots are not detected as overlapping"""
        slot1 = TimeSlot(time(8, 0), time(10, 0))
        slot2 = TimeSlot(time(10, 0), time(12, 0))
        self.assertFalse(slot1.overlaps_with(slot2))

    def test_time_slot_same(self):
        """Test identical time slots"""
        slot1 = TimeSlot(time(8, 0), time(10, 0))
        slot2 = TimeSlot(time(8, 0), time(10, 0))
        self.assertTrue(slot1.overlaps_with(slot2))


class TestRoom(unittest.TestCase):
    """Test Room class"""

    def setUp(self):
        self.room = Room("R001", "Room A", 40)

    def test_room_capacity_ok(self):
        """Test room can accommodate students within capacity"""
        self.assertTrue(self.room.can_accommodate(30))
        self.assertTrue(self.room.can_accommodate(40))

    def test_room_capacity_exceeded(self):
        """Test room cannot accommodate students exceeding capacity"""
        self.assertFalse(self.room.can_accommodate(41))
        self.assertFalse(self.room.can_accommodate(100))

    def test_room_str(self):
        """Test room string representation"""
        self.assertEqual(str(self.room), "Room A (Cap: 40)")


class TestConflictDetection(unittest.TestCase):
    """Test Conflict Detection Engine"""

    def setUp(self):
        """Setup test fixtures"""
        self.engine = ConflictDetectionEngine()
        self.room1 = Room("R001", "Room A", 40)
        self.room2 = Room("R002", "Room B", 35)

    def test_no_conflicts(self):
        """Test schedules with no conflicts"""
        schedule1 = Schedule(
            "SCH001", "Course A", "A101", "Lecturer A",
            DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
            self.room1, 30
        )
        schedule2 = Schedule(
            "SCH002", "Course B", "B101", "Lecturer B",
            DayOfWeek.TUESDAY, TimeSlot(time(8, 0), time(10, 0)),
            self.room2, 30
        )

        conflicts = self.engine.detect_schedule_conflicts([schedule1, schedule2])
        self.assertEqual(len(conflicts), 0)

    def test_room_conflict(self):
        """Test room conflict detection"""
        schedule1 = Schedule(
            "SCH001", "Course A", "A101", "Lecturer A",
            DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
            self.room1, 30
        )
        schedule2 = Schedule(
            "SCH002", "Course B", "B101", "Lecturer B",
            DayOfWeek.MONDAY, TimeSlot(time(9, 0), time(11, 0)),
            self.room1, 30  # Same room
        )

        conflicts = self.engine.detect_schedule_conflicts([schedule1, schedule2])
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0].conflict_type, ConflictType.ROOM_CONFLICT)

    def test_lecturer_conflict(self):
        """Test lecturer conflict detection"""
        schedule1 = Schedule(
            "SCH001", "Course A", "A101", "Dr. Lecturer",
            DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
            self.room1, 30
        )
        schedule2 = Schedule(
            "SCH002", "Course B", "B101", "Dr. Lecturer",  # Same lecturer
            DayOfWeek.MONDAY, TimeSlot(time(9, 0), time(11, 0)),
            self.room2, 30
        )

        conflicts = self.engine.detect_schedule_conflicts([schedule1, schedule2])
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0].conflict_type, ConflictType.LECTURER_CONFLICT)

    def test_capacity_exceeded(self):
        """Test capacity exceeded detection"""
        room = Room("R003", "Small Room", 20)
        schedule = Schedule(
            "SCH001", "Course A", "A101", "Lecturer A",
            DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
            room, 50  # Exceeds capacity
        )

        conflicts = self.engine.detect_schedule_conflicts([schedule])
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0].conflict_type, ConflictType.CAPACITY_EXCEEDED)

    def test_case_insensitive_lecturer_name(self):
        """Test that lecturer names are compared case-insensitively"""
        schedule1 = Schedule(
            "SCH001", "Course A", "A101", "Dr. John Smith",
            DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
            self.room1, 30
        )
        schedule2 = Schedule(
            "SCH002", "Course B", "B101", "dr. JOHN SMITH",  # Different case
            DayOfWeek.MONDAY, TimeSlot(time(9, 0), time(11, 0)),
            self.room2, 30
        )

        conflicts = self.engine.detect_schedule_conflicts([schedule1, schedule2])
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0].conflict_type, ConflictType.LECTURER_CONFLICT)


class TestSchedulingService(unittest.TestCase):
    """Test SchedulingService"""

    def setUp(self):
        """Setup test fixtures"""
        self.service = SchedulingService()
        self.room1 = Room("R001", "Room A", 40)
        self.room2 = Room("R002", "Room B", 35)
        self.service.add_room(self.room1)
        self.service.add_room(self.room2)

    def test_create_schedule_success(self):
        """Test successful schedule creation"""
        schedule = Schedule(
            "SCH001", "Course A", "A101", "Lecturer A",
            DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
            self.room1, 30
        )

        result = self.service.create_schedule(schedule)
        self.assertTrue(result)
        self.assertEqual(len(self.service.list_schedules()), 1)
        self.assertIsNotNone(self.service.get_schedule("SCH001"))

    def test_create_duplicate_schedule(self):
        """Test creating duplicate schedule (should fail)"""
        schedule = Schedule(
            "SCH001", "Course A", "A101", "Lecturer A",
            DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
            self.room1, 30
        )

        result1 = self.service.create_schedule(schedule)
        result2 = self.service.create_schedule(schedule)

        self.assertTrue(result1)
        self.assertFalse(result2)

    def test_update_schedule(self):
        """Test schedule update"""
        schedule = Schedule(
            "SCH001", "Course A", "A101", "Lecturer A",
            DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
            self.room1, 30
        )
        self.service.create_schedule(schedule)

        updated = Schedule(
            "SCH001", "Course A", "A101", "Lecturer A",
            DayOfWeek.TUESDAY, TimeSlot(time(10, 0), time(12, 0)),
            self.room2, 35
        )

        result = self.service.update_schedule("SCH001", updated)
        self.assertTrue(result)

        retrieved = self.service.get_schedule("SCH001")
        self.assertEqual(retrieved.day, DayOfWeek.TUESDAY)

    def test_delete_schedule(self):
        """Test schedule deletion"""
        schedule = Schedule(
            "SCH001", "Course A", "A101", "Lecturer A",
            DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
            self.room1, 30
        )
        self.service.create_schedule(schedule)

        result = self.service.delete_schedule("SCH001")
        self.assertTrue(result)
        self.assertEqual(len(self.service.list_schedules()), 0)

    def test_room_management(self):
        """Test room management"""
        self.assertEqual(len(self.service.list_rooms()), 2)
        
        room3 = Room("R003", "Room C", 50)
        self.service.add_room(room3)
        self.assertEqual(len(self.service.list_rooms()), 3)

        retrieved = self.service.get_room("R001")
        self.assertEqual(retrieved.room_name, "Room A")

    def test_get_schedules_by_lecturer(self):
        """Test querying schedules by lecturer"""
        schedule1 = Schedule(
            "SCH001", "Course A", "A101", "Dr. Smith",
            DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
            self.room1, 30
        )
        schedule2 = Schedule(
            "SCH002", "Course B", "B101", "Dr. Smith",
            DayOfWeek.TUESDAY, TimeSlot(time(10, 0), time(12, 0)),
            self.room2, 30
        )
        schedule3 = Schedule(
            "SCH003", "Course C", "C101", "Dr. Jones",
            DayOfWeek.WEDNESDAY, TimeSlot(time(8, 0), time(10, 0)),
            self.room1, 30
        )

        self.service.create_schedule(schedule1)
        self.service.create_schedule(schedule2)
        self.service.create_schedule(schedule3)

        smith_schedules = self.service.get_schedules_by_lecturer("Dr. Smith")
        self.assertEqual(len(smith_schedules), 2)

    def test_get_schedules_by_room(self):
        """Test querying schedules by room"""
        schedule1 = Schedule(
            "SCH001", "Course A", "A101", "Lecturer A",
            DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
            self.room1, 30
        )
        schedule2 = Schedule(
            "SCH002", "Course B", "B101", "Lecturer B",
            DayOfWeek.MONDAY, TimeSlot(time(13, 0), time(15, 0)),
            self.room1, 30
        )
        schedule3 = Schedule(
            "SCH003", "Course C", "C101", "Lecturer C",
            DayOfWeek.TUESDAY, TimeSlot(time(8, 0), time(10, 0)),
            self.room2, 30
        )

        self.service.create_schedule(schedule1)
        self.service.create_schedule(schedule2)
        self.service.create_schedule(schedule3)

        room1_schedules = self.service.get_schedules_by_room("R001")
        self.assertEqual(len(room1_schedules), 2)

    def test_get_schedules_by_day(self):
        """Test querying schedules by day"""
        schedule1 = Schedule(
            "SCH001", "Course A", "A101", "Lecturer A",
            DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
            self.room1, 30
        )
        schedule2 = Schedule(
            "SCH002", "Course B", "B101", "Lecturer B",
            DayOfWeek.TUESDAY, TimeSlot(time(8, 0), time(10, 0)),
            self.room2, 30
        )

        self.service.create_schedule(schedule1)
        self.service.create_schedule(schedule2)

        monday_schedules = self.service.get_schedules_by_day(DayOfWeek.MONDAY)
        self.assertEqual(len(monday_schedules), 1)


class TestObserverPattern(unittest.TestCase):
    """Test Observer Pattern Implementation"""

    def setUp(self):
        """Setup test fixtures"""
        self.subject = ScheduleSubject()

    def test_attach_observer(self):
        """Test attaching observers"""
        observer1 = StudentObserver("STU001", "John", "john@email.com")
        observer2 = LecturerObserver("LEC001", "Dr. Smith", "smith@email.com")

        self.subject.attach(observer1)
        self.subject.attach(observer2)

        self.assertEqual(len(self.subject._observers), 2)

    def test_detach_observer(self):
        """Test detaching observers"""
        observer = StudentObserver("STU001", "John", "john@email.com")

        self.subject.attach(observer)
        self.assertEqual(len(self.subject._observers), 1)

        self.subject.detach(observer)
        self.assertEqual(len(self.subject._observers), 0)

    def test_notify_observers(self):
        """Test notifying observers (basic test)"""
        observer = StudentObserver("STU001", "John", "john@email.com")
        self.subject.attach(observer)

        # This should not raise any exceptions
        data = {
            'course_name': 'Test Course',
            'description': 'Test Description'
        }
        self.subject.notify(EventType.SCHEDULE_CREATED, data)

    def test_duplicate_observer_not_attached_twice(self):
        """Test that the same observer is not attached twice"""
        observer = StudentObserver("STU001", "John", "john@email.com")

        self.subject.attach(observer)
        self.subject.attach(observer)

        self.assertEqual(len(self.subject._observers), 1)


class TestSchedulingSuggestionEngine(unittest.TestCase):
    """Test Scheduling Suggestion Engine"""

    def setUp(self):
        """Setup test fixtures"""
        self.service = SchedulingService()
        self.engine = SchedulingSuggestionEngine(self.service)
        
        self.room1 = Room("R001", "Room A", 40)
        self.room2 = Room("R002", "Room B", 50)
        self.service.add_room(self.room1)
        self.service.add_room(self.room2)

    def test_suggest_alternatives(self):
        """Test generating alternative schedule suggestions"""
        schedule = Schedule(
            "SCH001", "Course A", "A101", "Dr. Smith",
            DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
            self.room1, 30
        )

        available_slots = [
            (DayOfWeek.TUESDAY, TimeSlot(time(8, 0), time(10, 0)), self.room2),
            (DayOfWeek.WEDNESDAY, TimeSlot(time(10, 0), time(12, 0)), self.room1),
            (DayOfWeek.THURSDAY, TimeSlot(time(8, 0), time(10, 0)), self.room2),
        ]

        suggestions = self.engine.suggest_alternatives(schedule, available_slots, num_suggestions=2)

        self.assertEqual(len(suggestions), 2)
        self.assertIn('day', suggestions[0])
        self.assertIn('time_slot', suggestions[0])
        self.assertIn('room', suggestions[0])


class TestIntegration(unittest.TestCase):
    """Integration tests"""

    def test_full_workflow(self):
        """Test complete workflow: Create, Detect Conflict, Resolve"""
        service = SchedulingService()
        dashboard = DashboardService(service)

        # Add rooms
        room1 = Room("R001", "Room A", 40)
        room2 = Room("R002", "Room B", 35)
        service.add_room(room1)
        service.add_room(room2)

        # Create schedules
        schedule1 = Schedule(
            "SCH001", "Kalkulus", "MTH101", "Dr. Smith",
            DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
            room1, 35
        )
        schedule2 = Schedule(
            "SCH002", "Fisika", "PHY101", "Prof. Jones",
            DayOfWeek.TUESDAY, TimeSlot(time(10, 0), time(12, 0)),
            room2, 30
        )

        service.create_schedule(schedule1)
        service.create_schedule(schedule2)

        self.assertEqual(len(service.list_schedules()), 2)
        self.assertEqual(len(service.get_conflicts()), 0)

        # Create conflicting schedule
        schedule3 = Schedule(
            "SCH003", "Algoritma", "CS201", "Dr. Smith",  # Same lecturer as schedule1
            DayOfWeek.MONDAY, TimeSlot(time(9, 0), time(11, 0)),  # Overlaps with schedule1
            room1, 30
        )
        service.create_schedule(schedule3)

        # Should detect conflict
        self.assertGreater(len(service.get_conflicts()), 0)

        # Dashboard should show conflict
        summary = dashboard.get_dashboard_summary()
        self.assertGreater(summary['total_conflicts'], 0)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    run_tests()
