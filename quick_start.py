"""
QUICK START GUIDE - Schedule Management System

Panduan cepat untuk memulai menggunakan sistem penjadwalan.
"""

# ============================================================================
# QUICK START 1: Basic Setup & CRUD
# ============================================================================

print("=" * 80)
print("QUICK START 1: BASIC SETUP & CRUD")
print("=" * 80)

from schedule_system import *
from datetime import time

# 1. Initialize service
print("\n1️⃣  Initialize Service")
service = SchedulingService()

# 2. Add rooms
print("2️⃣  Add Rooms")
room_a = Room("R001", "Ruang A101", 40, "Building A")
room_b = Room("R002", "Ruang B201", 50, "Building B")
service.add_room(room_a)
service.add_room(room_b)

# 3. Create schedules
print("3️⃣  Create Schedules")
schedule1 = Schedule(
    schedule_id="SCH001",
    course_name="Kalkulus I",
    course_code="MTH101",
    lecturer_name="Dr. Bambang Susanto",
    day=DayOfWeek.MONDAY,
    time_slot=TimeSlot(time(8, 0), time(10, 0)),
    room=room_a,
    num_students=35
)

schedule2 = Schedule(
    schedule_id="SCH002",
    course_name="Fisika Dasar",
    course_code="PHY101",
    lecturer_name="Prof. Ratna Juwita",
    day=DayOfWeek.TUESDAY,
    time_slot=TimeSlot(time(10, 0), time(12, 0)),
    room=room_b,
    num_students=45
)

service.create_schedule(schedule1)
service.create_schedule(schedule2)

print(f"✅ Total schedules: {len(service.list_schedules())}")

# 4. Read schedule
print("\n4️⃣  Read Schedule")
retrieved = service.get_schedule("SCH001")
print(f"✅ Retrieved: {retrieved}")

# 5. Update schedule
print("\n5️⃣  Update Schedule")
updated_schedule = Schedule(
    schedule_id="SCH001",
    course_name="Kalkulus I",
    course_code="MTH101",
    lecturer_name="Dr. Bambang Susanto",
    day=DayOfWeek.WEDNESDAY,  # Changed day
    time_slot=TimeSlot(time(9, 0), time(11, 0)),  # Changed time
    room=room_a,
    num_students=35
)
service.update_schedule("SCH001", updated_schedule)
print(f"✅ Updated: {service.get_schedule('SCH001')}")

# 6. Delete schedule
print("\n6️⃣  Delete Schedule")
service.delete_schedule("SCH002")
print(f"✅ Remaining schedules: {len(service.list_schedules())}")


# ============================================================================
# QUICK START 2: CONFLICT DETECTION
# ============================================================================

print("\n\n" + "=" * 80)
print("QUICK START 2: CONFLICT DETECTION")
print("=" * 80)

# Create new service for conflict demo
conflict_service = SchedulingService()
conflict_service.add_room(Room("R001", "Ruang A", 40))
conflict_service.add_room(Room("R002", "Ruang B", 50))

print("\n🔨 Creating conflicting schedules...\n")

# Conflict 1: Room conflict
room_conflict1 = Schedule(
    "SCH_RC1", "Kalkulus I", "MTH101", "Dr. Smith",
    DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
    conflict_service.get_room("R001"), 35
)

room_conflict2 = Schedule(
    "SCH_RC2", "Aljabar", "MTH102", "Prof. Jones",
    DayOfWeek.MONDAY, TimeSlot(time(9, 0), time(11, 0)),  # Overlaps!
    conflict_service.get_room("R001"), 30  # Same room!
)

conflict_service.create_schedule(room_conflict1)
conflict_service.create_schedule(room_conflict2)

# Conflict 2: Lecturer conflict
lecturer_conflict1 = Schedule(
    "SCH_LC1", "Programming", "CS101", "Dr. Smith",
    DayOfWeek.WEDNESDAY, TimeSlot(time(13, 0), time(15, 0)),
    conflict_service.get_room("R002"), 28
)

lecturer_conflict2 = Schedule(
    "SCH_LC2", "Data Structures", "CS102", "Dr. Smith",  # Same lecturer!
    DayOfWeek.WEDNESDAY, TimeSlot(time(14, 0), time(16, 0)),  # Overlaps!
    conflict_service.get_room("R001"), 25
)

conflict_service.create_schedule(lecturer_conflict1)
conflict_service.create_schedule(lecturer_conflict2)

# Display conflicts
print("\n📊 DETECTED CONFLICTS:")
conflicts = conflict_service.get_conflicts()
for i, conflict in enumerate(conflicts, 1):
    print(f"\n{i}. [{conflict.conflict_type.value.upper()}]")
    print(f"   {conflict.description}")

print(f"\n✅ Total conflicts: {len(conflicts)}")


# ============================================================================
# QUICK START 3: OBSERVER PATTERN
# ============================================================================

print("\n\n" + "=" * 80)
print("QUICK START 3: OBSERVER PATTERN (NOTIFICATIONS)")
print("=" * 80)

# Create new service with observers
observer_service = SchedulingService()
observer_service.add_room(Room("R001", "Ruang A", 40))

print("\n📢 Registering Observers:\n")

# Create and register observers
student = StudentObserver("STU001", "Andi Wijaya", "andi@student.univ.edu")
lecturer = LecturerObserver("LEC001", "Dr. Bambang", "bambang@univ.edu")
admin = AdminObserver("ADMIN001", "Hendra", "hendra@univ.edu")

observer_service.attach(student)
observer_service.attach(lecturer)
observer_service.attach(admin)

print(f"✅ {len(observer_service._observers)} observers registered\n")

print("📝 Creating schedule (will trigger notifications):\n")

schedule = Schedule(
    "SCH001", "Kalkulus I", "MTH101", "Dr. Bambang",
    DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
    observer_service.get_room("R001"), 35
)

observer_service.create_schedule(schedule)

print("\n✅ See notification logs above ☝️")


# ============================================================================
# QUICK START 4: QUERIES
# ============================================================================

print("\n\n" + "=" * 80)
print("QUICK START 4: ADVANCED QUERIES")
print("=" * 80)

# Use conflict_service from earlier demo
print("\n🔍 Query Operations:\n")

# By lecturer
print("1️⃣  Get all schedules for Dr. Smith:")
dr_smith_schedules = conflict_service.get_schedules_by_lecturer("Dr. Smith")
for s in dr_smith_schedules:
    print(f"   - {s.course_name} ({s.day.name} {s.time_slot})")

# By room
print("\n2️⃣  Get all schedules in Ruang A:")
room_schedules = conflict_service.get_schedules_by_room("R001")
for s in room_schedules:
    print(f"   - {s.course_name} ({s.day.name} {s.time_slot})")

# By day
print("\n3️⃣  Get all schedules on MONDAY:")
monday_schedules = conflict_service.get_schedules_by_day(DayOfWeek.MONDAY)
for s in monday_schedules:
    print(f"   - {s.course_name} at {s.time_slot} by {s.lecturer_name}")

print("\n✅ Query operations completed")


# ============================================================================
# QUICK START 5: SUGGESTIONS & RESOLUTION
# ============================================================================

print("\n\n" + "=" * 80)
print("QUICK START 5: CONFLICT RESOLUTION SUGGESTIONS")
print("=" * 80)

suggestion_engine = SchedulingSuggestionEngine(conflict_service)

# Get a conflicted schedule
conflicted_schedule = conflict_service.get_schedule("SCH_RC1")

print(f"\n🎯 Resolving conflict for: {conflicted_schedule.course_name}")
print(f"   Current: {conflicted_schedule.day.name} {conflicted_schedule.time_slot}")
print(f"   Room: {conflicted_schedule.room.room_name}\n")

# Available alternatives
available = [
    (DayOfWeek.TUESDAY, TimeSlot(time(8, 0), time(10, 0)), conflict_service.get_room("R001")),
    (DayOfWeek.TUESDAY, TimeSlot(time(10, 0), time(12, 0)), conflict_service.get_room("R002")),
    (DayOfWeek.THURSDAY, TimeSlot(time(8, 0), time(10, 0)), conflict_service.get_room("R001")),
]

suggestions = suggestion_engine.suggest_alternatives(
    conflicted_schedule,
    available,
    num_suggestions=3
)

print("💡 SUGGESTED ALTERNATIVES:\n")
for i, sug in enumerate(suggestions, 1):
    print(f"Option {i}:")
    print(f"  Day: {sug['day']}")
    print(f"  Time: {sug['time_slot']}")
    print(f"  Room: {sug['room']}")
    print(f"  Disruption Score: {sug['disruption_score']}/10")
    print(f"  Status: {'✅' if not sug['lecturer_conflict'] else '❌'} Lecturer Available\n")


# ============================================================================
# QUICK START 6: DASHBOARD & REPORTS
# ============================================================================

print("\n" + "=" * 80)
print("QUICK START 6: DASHBOARD & REPORTS")
print("=" * 80)

dashboard = DashboardService(conflict_service)

print("\n📊 DASHBOARD SUMMARY:\n")
summary = dashboard.get_dashboard_summary()
print(f"Total Schedules: {summary['total_schedules']}")
print(f"Total Rooms: {summary['total_rooms']}")
print(f"Total Conflicts: {summary['total_conflicts']}")

print("\n📈 Schedules by Day:")
for day, count in summary['schedules_by_day'].items():
    print(f"  {day}: {count}")

print("\n🏢 Room Utilization:")
for room, stats in summary['room_utilization'].items():
    print(f"  {room}: {stats['utilization_percent']}% utilization")

# Export report
print("\n💾 Exporting conflict report...")
dashboard.export_conflict_report_json("quick_start_report.json")
print("✅ Report exported to: quick_start_report.json")


# ============================================================================
# SUMMARY
# ============================================================================

print("\n\n" + "=" * 80)
print("✅ QUICK START GUIDE COMPLETED")
print("=" * 80)

print("""
Key Features Demonstrated:
  1. ✅ CRUD Operations (Create, Read, Update, Delete)
  2. ✅ Conflict Detection (Room, Lecturer, Capacity)
  3. ✅ Observer Pattern (Pub-Sub Notifications)
  4. ✅ Query Operations (by Lecturer, Room, Day)
  5. ✅ Suggestion Engine (AI-powered alternatives)
  6. ✅ Dashboard & Reports

Next Steps:
  - Run 'python demo.py' for interactive demonstration
  - Run 'python test_schedule_system.py' for unit tests
  - Check 'README.md' for complete documentation
  - Review 'schedule_system.py' for implementation details

Generated Files:
  - quick_start_report.json: Conflict report

""")
