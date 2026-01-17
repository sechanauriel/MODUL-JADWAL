"""
Schedule Management System with Conflict Detection and Observer Pattern
Module 7-8: Jadwal & Ruangan (Schedule & Room)

Sistem penjadwalan kuliah dengan deteksi otomatis bentrok jadwal dan notifikasi Observer pattern.
"""

from datetime import datetime, time, timedelta
from typing import List, Dict, Set, Tuple, Optional
from enum import Enum
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import json
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# DATA MODELS
# ============================================================================

class DayOfWeek(Enum):
    """Days of the week"""
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class EventType(Enum):
    """Types of schedule change events"""
    SCHEDULE_CREATED = "SCHEDULE_CREATED"
    SCHEDULE_UPDATED = "SCHEDULE_UPDATED"
    SCHEDULE_DELETED = "SCHEDULE_DELETED"
    CONFLICT_DETECTED = "CONFLICT_DETECTED"
    SCHEDULE_RESOLVED = "SCHEDULE_RESOLVED"


class ConflictType(Enum):
    """Types of schedule conflicts"""
    ROOM_CONFLICT = "room_conflict"
    LECTURER_CONFLICT = "lecturer_conflict"
    TIME_OVERLAP = "time_overlap"
    CAPACITY_EXCEEDED = "capacity_exceeded"


@dataclass
class TimeSlot:
    """Represents a time slot (start_time and end_time)"""
    start_time: time
    end_time: time

    def overlaps_with(self, other: 'TimeSlot') -> bool:
        """Check if this time slot overlaps with another"""
        return self.start_time < other.end_time and other.start_time < self.end_time

    def __str__(self) -> str:
        return f"{self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}"


@dataclass
class Room:
    """Represents a classroom/room"""
    room_id: str
    room_name: str
    capacity: int
    building: str = "Main Building"

    def can_accommodate(self, num_students: int) -> bool:
        """Check if room can accommodate the number of students"""
        return num_students <= self.capacity

    def __str__(self) -> str:
        return f"{self.room_name} (Cap: {self.capacity})"


@dataclass
class Schedule:
    """Represents a course schedule"""
    schedule_id: str
    course_name: str
    course_code: str
    lecturer_name: str
    day: DayOfWeek
    time_slot: TimeSlot
    room: Room
    num_students: int
    krs_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """Convert schedule to dictionary"""
        return {
            'schedule_id': self.schedule_id,
            'course_name': self.course_name,
            'course_code': self.course_code,
            'lecturer_name': self.lecturer_name,
            'day': self.day.name,
            'time_slot': str(self.time_slot),
            'room': str(self.room),
            'num_students': self.num_students,
            'krs_id': self.krs_id
        }

    def __str__(self) -> str:
        return (f"{self.course_name} ({self.course_code}) - "
                f"{self.day.name} {self.time_slot} @ {self.room.room_name} - "
                f"By {self.lecturer_name}")


@dataclass
class ScheduleConflict:
    """Represents a schedule conflict"""
    conflict_type: ConflictType
    schedule_1: Schedule
    schedule_2: Optional[Schedule] = None
    description: str = ""
    severity: str = "high"  # high, medium, low

    def to_dict(self) -> Dict:
        """Convert conflict to dictionary"""
        result = {
            'conflict_type': self.conflict_type.value,
            'schedule_1': self.schedule_1.to_dict(),
            'description': self.description,
            'severity': self.severity
        }
        if self.schedule_2:
            result['schedule_2'] = self.schedule_2.to_dict()
        return result

    def __str__(self) -> str:
        return f"[{self.conflict_type.value}] {self.description}"


# ============================================================================
# OBSERVER PATTERN - NOTIFICATION SYSTEM
# ============================================================================

class Observer(ABC):
    """Abstract Observer class"""

    @abstractmethod
    def update(self, event_type: EventType, data: Dict) -> None:
        """Update observer with event notification"""
        pass


class StudentObserver(Observer):
    """Observer for students"""

    def __init__(self, student_id: str, student_name: str, email: str):
        self.student_id = student_id
        self.student_name = student_name
        self.email = email

    def update(self, event_type: EventType, data: Dict) -> None:
        """Notify student of schedule changes"""
        message = self._format_message(event_type, data)
        logger.info(f"📧 STUDENT NOTIFICATION ({self.student_name}): {message}")
        logger.info(f"   Email: {self.email}")

    def _format_message(self, event_type: EventType, data: Dict) -> str:
        """Format notification message"""
        if event_type == EventType.SCHEDULE_CREATED:
            return f"New schedule created: {data.get('course_name')}"
        elif event_type == EventType.SCHEDULE_UPDATED:
            return f"Schedule updated for: {data.get('course_name')}"
        elif event_type == EventType.SCHEDULE_DELETED:
            return f"Schedule deleted: {data.get('course_name')}"
        elif event_type == EventType.CONFLICT_DETECTED:
            return f"Schedule conflict detected: {data.get('description')}"
        elif event_type == EventType.SCHEDULE_RESOLVED:
            return f"Schedule conflict resolved: {data.get('description')}"
        return f"Schedule event: {event_type.value}"


class LecturerObserver(Observer):
    """Observer for lecturers"""

    def __init__(self, lecturer_id: str, lecturer_name: str, email: str):
        self.lecturer_id = lecturer_id
        self.lecturer_name = lecturer_name
        self.email = email

    def update(self, event_type: EventType, data: Dict) -> None:
        """Notify lecturer of schedule changes"""
        message = self._format_message(event_type, data)
        logger.info(f"👨‍🏫 LECTURER NOTIFICATION ({self.lecturer_name}): {message}")
        logger.info(f"   Email: {self.email}")

    def _format_message(self, event_type: EventType, data: Dict) -> str:
        """Format notification message"""
        if event_type == EventType.SCHEDULE_CREATED:
            return f"You have a new class: {data.get('course_name')}"
        elif event_type == EventType.SCHEDULE_UPDATED:
            return f"Your class schedule has been updated: {data.get('course_name')}"
        elif event_type == EventType.SCHEDULE_DELETED:
            return f"Your class has been cancelled: {data.get('course_name')}"
        elif event_type == EventType.CONFLICT_DETECTED:
            return f"ALERT: Schedule conflict detected: {data.get('description')}"
        elif event_type == EventType.SCHEDULE_RESOLVED:
            return f"Schedule conflict has been resolved: {data.get('description')}"
        return f"Schedule event: {event_type.value}"


class AdminObserver(Observer):
    """Observer for academic administrators"""

    def __init__(self, admin_id: str, admin_name: str, email: str):
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.email = email

    def update(self, event_type: EventType, data: Dict) -> None:
        """Notify admin of schedule changes"""
        message = self._format_message(event_type, data)
        logger.info(f"👨‍💼 ADMIN NOTIFICATION ({self.admin_name}): {message}")
        logger.info(f"   Email: {self.email}")

    def _format_message(self, event_type: EventType, data: Dict) -> str:
        """Format notification message"""
        if event_type == EventType.SCHEDULE_CREATED:
            return f"New schedule created: {data.get('course_name')}"
        elif event_type == EventType.SCHEDULE_UPDATED:
            return f"Schedule updated: {data.get('course_name')}"
        elif event_type == EventType.SCHEDULE_DELETED:
            return f"Schedule deleted: {data.get('course_name')}"
        elif event_type == EventType.CONFLICT_DETECTED:
            conflict_details = data.get('description')
            return f"⚠️  CONFLICT ALERT: {conflict_details}"
        elif event_type == EventType.SCHEDULE_RESOLVED:
            return f"Conflict resolved: {data.get('description')}"
        return f"Schedule event: {event_type.value}"


class ScheduleSubject:
    """Publisher/Subject for schedule notifications (Observable)"""

    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Attach an observer"""
        if observer not in self._observers:
            self._observers.append(observer)
            logger.debug(f"Observer attached: {observer.__class__.__name__}")

    def detach(self, observer: Observer) -> None:
        """Detach an observer"""
        if observer in self._observers:
            self._observers.remove(observer)
            logger.debug(f"Observer detached: {observer.__class__.__name__}")

    def notify(self, event_type: EventType, data: Dict) -> None:
        """Notify all observers of an event"""
        logger.debug(f"Notifying {len(self._observers)} observers of event: {event_type.value}")
        for observer in self._observers:
            observer.update(event_type, data)


# ============================================================================
# CONFLICT DETECTION ENGINE
# ============================================================================

class ConflictDetectionEngine:
    """Engine for detecting schedule conflicts (3-dimensional conflict detection)"""

    @staticmethod
    def detect_schedule_conflicts(schedules: List[Schedule]) -> List[ScheduleConflict]:
        """
        Detect all conflicts in a list of schedules.
        
        3D Conflict Detection:
        1. Room Conflict: Same day, overlapping time, same room
        2. Lecturer Conflict: Same day, overlapping time, same lecturer
        3. Capacity Exceeded: Number of students > room capacity
        
        Time Complexity: O(n²) for schedule comparison, O(n log n) with interval trees
        """
        conflicts: List[ScheduleConflict] = []

        # Check for capacity violations first (O(n))
        for schedule in schedules:
            if not schedule.room.can_accommodate(schedule.num_students):
                conflict = ScheduleConflict(
                    conflict_type=ConflictType.CAPACITY_EXCEEDED,
                    schedule_1=schedule,
                    description=f"{schedule.course_name}: {schedule.num_students} students "
                               f"exceed room capacity of {schedule.room.capacity}",
                    severity="high"
                )
                conflicts.append(conflict)

        # Check for room and lecturer conflicts (O(n²))
        for i, sched1 in enumerate(schedules):
            for sched2 in schedules[i+1:]:
                # Only check schedules on the same day
                if sched1.day != sched2.day:
                    continue

                # Check for time overlap
                if not sched1.time_slot.overlaps_with(sched2.time_slot):
                    continue

                # Same room conflict
                if sched1.room.room_id == sched2.room.room_id:
                    conflict = ScheduleConflict(
                        conflict_type=ConflictType.ROOM_CONFLICT,
                        schedule_1=sched1,
                        schedule_2=sched2,
                        description=f"Room '{sched1.room.room_name}' double-booked: "
                                   f"{sched1.course_name} vs {sched2.course_name}",
                        severity="critical"
                    )
                    conflicts.append(conflict)

                # Same lecturer conflict
                if sched1.lecturer_name.lower() == sched2.lecturer_name.lower():
                    conflict = ScheduleConflict(
                        conflict_type=ConflictType.LECTURER_CONFLICT,
                        schedule_1=sched1,
                        schedule_2=sched2,
                        description=f"Lecturer '{sched1.lecturer_name}' double-booked: "
                                   f"{sched1.course_name} ({sched1.day.name} {sched1.time_slot}) vs "
                                   f"{sched2.course_name} ({sched2.day.name} {sched2.time_slot})",
                        severity="critical"
                    )
                    conflicts.append(conflict)

        return conflicts

    @staticmethod
    def get_conflict_summary(conflicts: List[ScheduleConflict]) -> Dict:
        """Get summary of conflicts"""
        summary = {
            'total_conflicts': len(conflicts),
            'by_type': defaultdict(int),
            'by_severity': defaultdict(int),
            'affected_schedules': set()
        }

        for conflict in conflicts:
            summary['by_type'][conflict.conflict_type.value] += 1
            summary['by_severity'][conflict.severity] += 1
            summary['affected_schedules'].add(conflict.schedule_1.schedule_id)
            if conflict.schedule_2:
                summary['affected_schedules'].add(conflict.schedule_2.schedule_id)

        summary['affected_schedules'] = list(summary['affected_schedules'])
        summary['by_type'] = dict(summary['by_type'])
        summary['by_severity'] = dict(summary['by_severity'])

        return summary


# ============================================================================
# SCHEDULING SERVICE
# ============================================================================

class SchedulingService(ScheduleSubject):
    """Main scheduling service with CRUD operations and conflict detection"""

    def __init__(self):
        super().__init__()
        self.schedules: Dict[str, Schedule] = {}
        self.rooms: Dict[str, Room] = {}
        self.conflicts: List[ScheduleConflict] = []
        self.conflict_detection = ConflictDetectionEngine()

    # Room Management
    def add_room(self, room: Room) -> bool:
        """Add a new room"""
        if room.room_id in self.rooms:
            logger.warning(f"Room {room.room_id} already exists")
            return False
        self.rooms[room.room_id] = room
        logger.info(f"✅ Room added: {room}")
        return True

    def get_room(self, room_id: str) -> Optional[Room]:
        """Get room by ID"""
        return self.rooms.get(room_id)

    def list_rooms(self) -> List[Room]:
        """List all rooms"""
        return list(self.rooms.values())

    # Schedule CRUD Operations
    def create_schedule(self, schedule: Schedule) -> bool:
        """Create a new schedule"""
        if schedule.schedule_id in self.schedules:
            logger.warning(f"Schedule {schedule.schedule_id} already exists")
            return False

        # Validate room exists and has capacity
        if not self._validate_schedule(schedule):
            return False

        self.schedules[schedule.schedule_id] = schedule
        logger.info(f"✅ Schedule created: {schedule}")

        # Check for conflicts
        self._detect_and_notify_conflicts()

        # Notify observers
        self.notify(EventType.SCHEDULE_CREATED, schedule.to_dict())
        return True

    def update_schedule(self, schedule_id: str, updated_schedule: Schedule) -> bool:
        """Update an existing schedule"""
        if schedule_id not in self.schedules:
            logger.warning(f"Schedule {schedule_id} not found")
            return False

        if not self._validate_schedule(updated_schedule):
            return False

        old_schedule = self.schedules[schedule_id]
        updated_schedule.created_at = old_schedule.created_at
        updated_schedule.updated_at = datetime.now()
        self.schedules[schedule_id] = updated_schedule

        logger.info(f"✅ Schedule updated: {updated_schedule}")

        # Check for conflicts
        self._detect_and_notify_conflicts()

        # Notify observers
        self.notify(EventType.SCHEDULE_UPDATED, updated_schedule.to_dict())
        return True

    def delete_schedule(self, schedule_id: str) -> bool:
        """Delete a schedule"""
        if schedule_id not in self.schedules:
            logger.warning(f"Schedule {schedule_id} not found")
            return False

        schedule = self.schedules.pop(schedule_id)
        logger.info(f"✅ Schedule deleted: {schedule}")

        # Check for conflicts (in case deletion resolved conflicts)
        self._detect_and_notify_conflicts()

        # Notify observers
        self.notify(EventType.SCHEDULE_DELETED, schedule.to_dict())

        # Invalidate KRS if schedule had one
        if schedule.krs_id:
            self._invalidate_krs(schedule.krs_id, schedule)

        return True

    def get_schedule(self, schedule_id: str) -> Optional[Schedule]:
        """Get schedule by ID"""
        return self.schedules.get(schedule_id)

    def list_schedules(self) -> List[Schedule]:
        """List all schedules"""
        return list(self.schedules.values())

    def get_schedules_by_lecturer(self, lecturer_name: str) -> List[Schedule]:
        """Get all schedules for a specific lecturer"""
        return [s for s in self.schedules.values()
                if s.lecturer_name.lower() == lecturer_name.lower()]

    def get_schedules_by_room(self, room_id: str) -> List[Schedule]:
        """Get all schedules for a specific room"""
        return [s for s in self.schedules.values()
                if s.room.room_id == room_id]

    def get_schedules_by_day(self, day: DayOfWeek) -> List[Schedule]:
        """Get all schedules on a specific day"""
        return [s for s in self.schedules.values() if s.day == day]

    # Validation
    def _validate_schedule(self, schedule: Schedule) -> bool:
        """Validate schedule before creation/update"""
        # Check if room exists
        if schedule.room.room_id not in self.rooms:
            logger.error(f"Room {schedule.room.room_id} not found")
            return False

        # Check capacity
        if not schedule.room.can_accommodate(schedule.num_students):
            logger.error(f"Room capacity exceeded: {schedule.num_students} > {schedule.room.capacity}")
            return False

        return True

    # Conflict Management
    def _detect_and_notify_conflicts(self) -> None:
        """Detect conflicts in current schedules and notify observers"""
        self.conflicts = self.conflict_detection.detect_schedule_conflicts(
            list(self.schedules.values())
        )

        if self.conflicts:
            logger.warning(f"⚠️  {len(self.conflicts)} conflict(s) detected!")
            for conflict in self.conflicts:
                logger.warning(f"   - {conflict}")
                self.notify(EventType.CONFLICT_DETECTED, conflict.to_dict())

    def get_conflicts(self) -> List[ScheduleConflict]:
        """Get all current conflicts"""
        return self.conflicts

    def get_conflicts_for_schedule(self, schedule_id: str) -> List[ScheduleConflict]:
        """Get conflicts involving a specific schedule"""
        return [c for c in self.conflicts
                if c.schedule_1.schedule_id == schedule_id or
                   (c.schedule_2 and c.schedule_2.schedule_id == schedule_id)]

    # KRS Integration
    def _invalidate_krs(self, krs_id: str, schedule: Schedule) -> None:
        """Invalidate KRS when schedule changes"""
        logger.warning(f"🚨 KRS {krs_id} invalidated due to schedule change: {schedule.course_name}")
        data = {
            'krs_id': krs_id,
            'course_name': schedule.course_name,
            'reason': 'Schedule changed'
        }
        # In a real system, this would call an API to invalidate KRS

    def get_conflict_summary(self) -> Dict:
        """Get conflict summary"""
        return self.conflict_detection.get_conflict_summary(self.conflicts)


# ============================================================================
# SCHEDULING SUGGESTION ENGINE (AI-Powered Alternative Suggestions)
# ============================================================================

class SchedulingSuggestionEngine:
    """Generates alternative schedule suggestions to resolve conflicts"""

    def __init__(self, scheduling_service: SchedulingService):
        self.service = scheduling_service

    def suggest_alternatives(self, conflicted_schedule: Schedule,
                           available_slots: List[Tuple[DayOfWeek, TimeSlot, Room]],
                           num_suggestions: int = 3) -> List[Dict]:
        """
        Suggest alternative schedules for a conflicted course.
        
        Criteria:
        1. Room capacity >= number of students
        2. No conflict with lecturer's other schedules
        3. Minimal disruption (prefer morning/afternoon over evening)
        """
        suggestions = []

        # Filter available slots by capacity
        valid_slots = [
            (day, time_slot, room) for day, time_slot, room in available_slots
            if room.can_accommodate(conflicted_schedule.num_students)
        ]

        # Rank slots by preference
        ranked_slots = self._rank_slots(conflicted_schedule, valid_slots)

        # Generate suggestions
        for i, (day, time_slot, room) in enumerate(ranked_slots[:num_suggestions]):
            # Check if this slot conflicts with lecturer's other schedules
            lecturer_schedules = self.service.get_schedules_by_lecturer(
                conflicted_schedule.lecturer_name
            )

            has_lecturer_conflict = any(
                s.schedule_id != conflicted_schedule.schedule_id and
                s.day == day and
                s.time_slot.overlaps_with(time_slot)
                for s in lecturer_schedules
            )

            reason = []
            reason.append(f"Room capacity: {room.capacity} (need: {conflicted_schedule.num_students})")

            if has_lecturer_conflict:
                reason.append("⚠️  Conflicts with lecturer schedule")
            else:
                reason.append("✅ No lecturer conflict")

            disruption_score = self._calculate_disruption(conflicted_schedule, day, time_slot)
            reason.append(f"Disruption score: {disruption_score}/10")

            suggestion = {
                'day': day.name,
                'time_slot': str(time_slot),
                'room': f"{room.room_name} ({room.room_id})",
                'room_capacity': room.capacity,
                'lecturer_conflict': has_lecturer_conflict,
                'disruption_score': disruption_score,
                'reason': '; '.join(reason)
            }
            suggestions.append(suggestion)

        return suggestions

    def _rank_slots(self, schedule: Schedule,
                    valid_slots: List[Tuple[DayOfWeek, TimeSlot, Room]]) -> List[Tuple[DayOfWeek, TimeSlot, Room]]:
        """Rank available slots by preference"""

        def preference_score(item):
            day, time_slot, room = item

            # Prefer morning (08:00-12:00) over afternoon (12:00-17:00)
            hour = time_slot.start_time.hour
            time_preference = 0
            if 8 <= hour < 12:
                time_preference = 10
            elif 12 <= hour < 17:
                time_preference = 8
            else:
                time_preference = 3

            # Prefer days close to original day
            day_distance = abs(day.value - schedule.day.value)
            day_preference = 10 - day_distance

            # Total score
            return time_preference + day_preference

        return sorted(valid_slots, key=preference_score, reverse=True)

    def _calculate_disruption(self, original: Schedule, new_day: DayOfWeek,
                             new_time: TimeSlot) -> int:
        """Calculate disruption score (0-10, lower is better)"""
        disruption = 0

        # Day change penalty
        if original.day != new_day:
            disruption += 2

        # Time change penalty
        hour_diff = abs(original.time_slot.start_time.hour - new_time.start_time.hour)
        if hour_diff > 3:
            disruption += 4
        elif hour_diff > 0:
            disruption += 2

        # Evening class penalty
        if new_time.start_time.hour >= 17:
            disruption += 2

        return min(disruption, 10)


# ============================================================================
# DASHBOARD & REPORTING
# ============================================================================

class DashboardService:
    """Service for dashboard and reporting"""

    def __init__(self, scheduling_service: SchedulingService):
        self.service = scheduling_service

    def get_dashboard_summary(self) -> Dict:
        """Get overall dashboard summary"""
        schedules = self.service.list_schedules()
        conflicts = self.service.get_conflicts()

        return {
            'total_schedules': len(schedules),
            'total_rooms': len(self.service.list_rooms()),
            'total_conflicts': len(conflicts),
            'conflict_summary': self.service.get_conflict_summary(),
            'schedules_by_day': self._count_schedules_by_day(schedules),
            'room_utilization': self._calculate_room_utilization(schedules)
        }

    def _count_schedules_by_day(self, schedules: List[Schedule]) -> Dict[str, int]:
        """Count schedules by day of week"""
        counts = {day.name: 0 for day in DayOfWeek}
        for schedule in schedules:
            counts[schedule.day.name] += 1
        return counts

    def _calculate_room_utilization(self, schedules: List[Schedule]) -> Dict[str, Dict]:
        """Calculate room utilization percentage"""
        room_stats = {}

        for room in self.service.list_rooms():
            room_schedules = self.service.get_schedules_by_room(room.room_id)
            room_stats[room.room_name] = {
                'total_slots': 10 * 5,  # Assuming 10 time slots, 5 days
                'used_slots': len(room_schedules),
                'utilization_percent': round((len(room_schedules) / (10 * 5)) * 100, 2)
            }

        return room_stats

    def get_conflict_report(self) -> Dict:
        """Get detailed conflict report"""
        conflicts = self.service.get_conflicts()

        report = {
            'timestamp': datetime.now().isoformat(),
            'total_conflicts': len(conflicts),
            'conflicts': [c.to_dict() for c in conflicts],
            'summary': self.service.get_conflict_summary()
        }

        return report

    def export_conflict_report_json(self, filename: str) -> bool:
        """Export conflict report to JSON file"""
        try:
            report = self.get_conflict_report()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"✅ Conflict report exported to {filename}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to export conflict report: {e}")
            return False

    def print_schedule_table(self) -> None:
        """Print all schedules in a table format"""
        schedules = self.service.list_schedules()

        if not schedules:
            print("No schedules found.")
            return

        print("\n" + "=" * 120)
        print("SCHEDULE TABLE".center(120))
        print("=" * 120)
        print(f"{'Course':<20} {'Code':<8} {'Lecturer':<15} {'Day':<10} {'Time':<12} {'Room':<12} {'Students':<10}")
        print("-" * 120)

        for schedule in sorted(schedules, key=lambda s: (s.day.value, s.time_slot.start_time)):
            print(f"{schedule.course_name:<20} {schedule.course_code:<8} {schedule.lecturer_name:<15} "
                  f"{schedule.day.name:<10} {str(schedule.time_slot):<12} {schedule.room.room_name:<12} "
                  f"{schedule.num_students:<10}")

        print("=" * 120 + "\n")

    def print_conflicts(self) -> None:
        """Print all conflicts"""
        conflicts = self.service.get_conflicts()

        if not conflicts:
            print("✅ No conflicts found!")
            return

        print("\n" + "=" * 120)
        print("SCHEDULE CONFLICTS".center(120))
        print("=" * 120)

        for i, conflict in enumerate(conflicts, 1):
            print(f"\n{i}. [{conflict.conflict_type.value.upper()}] - Severity: {conflict.severity}")
            print(f"   Description: {conflict.description}")
            print(f"   Schedule 1: {conflict.schedule_1}")
            if conflict.schedule_2:
                print(f"   Schedule 2: {conflict.schedule_2}")

        print("\n" + "=" * 120 + "\n")

    def print_room_schedule(self, room_id: str) -> None:
        """Print schedule for a specific room"""
        room = self.service.get_room(room_id)
        if not room:
            print(f"Room {room_id} not found.")
            return

        schedules = self.service.get_schedules_by_room(room_id)

        print(f"\n{'='*100}")
        print(f"ROOM SCHEDULE: {room} - Capacity: {room.capacity}".center(100))
        print(f"{'='*100}")

        if not schedules:
            print("No schedules for this room.")
        else:
            print(f"{'Day':<12} {'Time':<12} {'Course':<25} {'Lecturer':<15} {'Students':<10}")
            print("-" * 100)
            for schedule in sorted(schedules, key=lambda s: (s.day.value, s.time_slot.start_time)):
                print(f"{schedule.day.name:<12} {str(schedule.time_slot):<12} {schedule.course_name:<25} "
                      f"{schedule.lecturer_name:<15} {schedule.num_students:<10}")

        print(f"{'='*100}\n")
