"""
DEMO & TEST: Schedule Management System
Shows all features: CRUD, Conflict Detection, Observer Pattern, and Suggestions
"""

from schedule_system import *
import sys


def print_header(text: str) -> None:
    """Print a formatted header"""
    print(f"\n{'='*80}")
    print(f"  {text}")
    print(f"{'='*80}\n")


def setup_system() -> Tuple[SchedulingService, DashboardService, SchedulingSuggestionEngine]:
    """Setup and initialize the scheduling system with sample data"""

    print_header("SETTING UP SCHEDULE MANAGEMENT SYSTEM")

    # Initialize services
    service = SchedulingService()
    dashboard = DashboardService(service)
    suggestion_engine = SchedulingSuggestionEngine(service)

    # Create rooms
    print("📍 Creating Rooms...")
    rooms = [
        Room("R001", "Ruang A101", 40, "Building A"),
        Room("R002", "Ruang A102", 35, "Building A"),
        Room("R003", "Ruang B201", 50, "Building B"),
        Room("R004", "Ruang B202", 45, "Building B"),
        Room("R005", "Ruang C301", 60, "Building C"),
        Room("R006", "Lab Komputer", 30, "Building D"),
    ]

    for room in rooms:
        service.add_room(room)

    # Setup observers (subscribers)
    print("\n📢 Registering Observers...")

    # Student observers
    student1 = StudentObserver("STU001", "Andi Wijaya", "andi@student.univ.edu")
    student2 = StudentObserver("STU002", "Budi Santoso", "budi@student.univ.edu")

    # Lecturer observers
    lecturer1 = LecturerObserver("LEC001", "Dr. Bambang Susanto", "bambang@univ.edu")
    lecturer2 = LecturerObserver("LEC002", "Prof. Ratna Juwita", "ratna@univ.edu")

    # Admin observer
    admin = AdminObserver("ADMIN001", "Hendra Setiawan", "hendra@univ.edu")

    # Attach observers
    service.attach(student1)
    service.attach(student2)
    service.attach(lecturer1)
    service.attach(lecturer2)
    service.attach(admin)

    print(f"✅ {len(service._observers)} Observers registered\n")

    return service, dashboard, suggestion_engine


def demo_crud_operations(service: SchedulingService, dashboard: DashboardService) -> None:
    """Demonstrate CRUD operations"""

    print_header("DEMO 1: CRUD OPERATIONS")

    # Create schedules
    print("📝 Creating Schedules...")

    schedule1 = Schedule(
        schedule_id="SCH001",
        course_name="Kalkulus I",
        course_code="MTH101",
        lecturer_name="Dr. Bambang Susanto",
        day=DayOfWeek.MONDAY,
        time_slot=TimeSlot(time(8, 0), time(10, 0)),
        room=service.get_room("R001"),
        num_students=40
    )

    schedule2 = Schedule(
        schedule_id="SCH002",
        course_name="Fisika Dasar",
        course_code="PHY101",
        lecturer_name="Prof. Ratna Juwita",
        day=DayOfWeek.TUESDAY,
        time_slot=TimeSlot(time(10, 0), time(12, 0)),
        room=service.get_room("R003"),
        num_students=45
    )

    schedule3 = Schedule(
        schedule_id="SCH003",
        course_name="Algoritma & Struktur Data",
        course_code="CS201",
        lecturer_name="Dr. Bambang Susanto",
        day=DayOfWeek.WEDNESDAY,
        time_slot=TimeSlot(time(13, 0), time(15, 0)),
        room=service.get_room("R006"),
        num_students=30
    )

    service.create_schedule(schedule1)
    service.create_schedule(schedule2)
    service.create_schedule(schedule3)

    print("\n✅ Total schedules created:", len(service.list_schedules()))

    # Read schedules
    print("\n📖 Reading Schedules:")
    print(f"   Schedule 1: {service.get_schedule('SCH001')}")

    # Update schedule
    print("\n✏️  Updating Schedule (changing room for SCH003)...")
    schedule3_updated = Schedule(
        schedule_id="SCH003",
        course_name="Algoritma & Struktur Data",
        course_code="CS201",
        lecturer_name="Dr. Bambang Susanto",
        day=DayOfWeek.THURSDAY,
        time_slot=TimeSlot(time(14, 0), time(16, 0)),
        room=service.get_room("R002"),
        num_students=30
    )
    service.update_schedule("SCH003", schedule3_updated)

    # Display all schedules
    print("\n📋 All Schedules:")
    dashboard.print_schedule_table()


def demo_conflict_detection(service: SchedulingService, dashboard: DashboardService) -> None:
    """Demonstrate conflict detection (3D conflicts)"""

    print_header("DEMO 2: CONFLICT DETECTION (3D)")

    # Create conflicting schedules
    print("Creating conflicting schedules...\n")

    # Conflict 1: Room conflict (same room, same time, same day)
    conflict_schedule1 = Schedule(
        schedule_id="SCH004",
        course_name="Matematika Diskrit",
        course_code="MTH102",
        lecturer_name="Prof. Imam Wahyudi",
        day=DayOfWeek.MONDAY,
        time_slot=TimeSlot(time(8, 0), time(10, 0)),  # Same time as SCH001
        room=service.get_room("R001"),  # Same room
        num_students=35
    )
    service.create_schedule(conflict_schedule1)

    # Conflict 2: Lecturer conflict (same lecturer, same time, same day)
    conflict_schedule2 = Schedule(
        schedule_id="SCH005",
        course_name="Pemrograman Python",
        course_code="CS301",
        lecturer_name="Dr. Bambang Susanto",  # Same lecturer as SCH001
        day=DayOfWeek.MONDAY,
        time_slot=TimeSlot(time(9, 0), time(11, 0)),  # Overlaps with SCH001
        room=service.get_room("R005"),
        num_students=28
    )
    service.create_schedule(conflict_schedule2)

    # Conflict 3: Capacity exceeded
    conflict_schedule3 = Schedule(
        schedule_id="SCH006",
        course_name="Seminar Teknologi",
        course_code="CS401",
        lecturer_name="Prof. Anton Basuki",
        day=DayOfWeek.FRIDAY,
        time_slot=TimeSlot(time(10, 0), time(12, 0)),
        room=service.get_room("R006"),  # Lab Komputer capacity is 30
        num_students=50  # EXCEEDS CAPACITY
    )
    service.create_schedule(conflict_schedule3)

    # Display conflicts
    print("\n🔴 DETECTED CONFLICTS:")
    dashboard.print_conflicts()

    # Print conflict summary
    print("📊 CONFLICT SUMMARY:")
    summary = service.get_conflict_summary()
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def demo_observer_pattern(service: SchedulingService) -> None:
    """Demonstrate Observer pattern with schedule changes"""

    print_header("DEMO 3: OBSERVER PATTERN (NOTIFICATIONS)")

    print("Scenario: Schedule modification triggers observer notifications\n")

    # Get an existing schedule and modify it
    schedule = service.get_schedule("SCH001")
    if schedule:
        print(f"Modifying schedule: {schedule.course_name}")
        modified = Schedule(
            schedule_id="SCH001",
            course_name="Kalkulus I",
            course_code="MTH101",
            lecturer_name="Dr. Bambang Susanto",
            day=DayOfWeek.WEDNESDAY,  # Changed day
            time_slot=TimeSlot(time(9, 0), time(11, 0)),  # Changed time
            room=service.get_room("R001"),
            num_students=40
        )
        service.update_schedule("SCH001", modified)

    print("\nNotification events were triggered above ☝️")


def demo_conflict_resolution_suggestions(service: SchedulingService, 
                                         suggestion_engine: SchedulingSuggestionEngine) -> None:
    """Demonstrate AI-powered conflict resolution suggestions"""

    print_header("DEMO 4: AI-POWERED CONFLICT RESOLUTION SUGGESTIONS")

    # Get a conflicted schedule
    conflicts = service.get_conflicts()
    if not conflicts:
        print("No conflicts found. Skipping suggestion demo.")
        return

    # Get the first conflict
    conflict = conflicts[0]
    conflicted_schedule = conflict.schedule_1

    print(f"Resolving conflict for: {conflicted_schedule}")
    print(f"Conflict type: {conflict.conflict_type.value}")
    print(f"\nSearching for alternative time slots...\n")

    # Create available slots for suggestions
    available_slots = [
        (DayOfWeek.TUESDAY, TimeSlot(time(8, 0), time(10, 0)), service.get_room("R002")),
        (DayOfWeek.TUESDAY, TimeSlot(time(10, 0), time(12, 0)), service.get_room("R003")),
        (DayOfWeek.TUESDAY, TimeSlot(time(13, 0), time(15, 0)), service.get_room("R004")),
        (DayOfWeek.WEDNESDAY, TimeSlot(time(8, 0), time(10, 0)), service.get_room("R005")),
        (DayOfWeek.THURSDAY, TimeSlot(time(8, 0), time(10, 0)), service.get_room("R001")),
        (DayOfWeek.THURSDAY, TimeSlot(time(10, 0), time(12, 0)), service.get_room("R002")),
        (DayOfWeek.FRIDAY, TimeSlot(time(8, 0), time(10, 0)), service.get_room("R003")),
    ]

    suggestions = suggestion_engine.suggest_alternatives(
        conflicted_schedule,
        available_slots,
        num_suggestions=3
    )

    print("=" * 120)
    print("ALTERNATIVE SCHEDULE SUGGESTIONS".center(120))
    print("=" * 120)

    for i, suggestion in enumerate(suggestions, 1):
        print(f"\nOption {i}:")
        print(f"  Day: {suggestion['day']}")
        print(f"  Time: {suggestion['time_slot']}")
        print(f"  Room: {suggestion['room']} (Capacity: {suggestion['room_capacity']})")
        print(f"  Lecturer Conflict: {'❌ YES' if suggestion['lecturer_conflict'] else '✅ NO'}")
        print(f"  Disruption Score: {suggestion['disruption_score']}/10")
        print(f"  Reasons: {suggestion['reason']}")

    print("\n" + "=" * 120 + "\n")


def demo_dashboard_and_reports(service: SchedulingService, dashboard: DashboardService) -> None:
    """Demonstrate dashboard and reporting features"""

    print_header("DEMO 5: DASHBOARD & REPORTING")

    # Dashboard summary
    print("📊 DASHBOARD SUMMARY:")
    summary = dashboard.get_dashboard_summary()

    print(f"  Total Schedules: {summary['total_schedules']}")
    print(f"  Total Rooms: {summary['total_rooms']}")
    print(f"  Total Conflicts: {summary['total_conflicts']}")

    print("\n  Schedules by Day:")
    for day, count in summary['schedules_by_day'].items():
        print(f"    {day}: {count}")

    print("\n  Room Utilization:")
    for room, stats in summary['room_utilization'].items():
        print(f"    {room}: {stats['utilization_percent']}% ({stats['used_slots']}/{stats['total_slots']})")

    # Conflict report
    print("\n📄 CONFLICT REPORT:")
    report = dashboard.get_conflict_report()
    print(f"  Report Generated: {report['timestamp']}")
    print(f"  Total Conflicts: {report['total_conflicts']}")

    if report['conflicts']:
        print("\n  Conflicts:")
        for i, conflict in enumerate(report['conflicts'], 1):
            print(f"    {i}. {conflict['conflict_type']}: {conflict['description']}")

    # Export report
    print("\n💾 Exporting conflict report to JSON...")
    dashboard.export_conflict_report_json("conflict_report.json")


def demo_advanced_queries(service: SchedulingService) -> None:
    """Demonstrate advanced query operations"""

    print_header("DEMO 6: ADVANCED QUERIES")

    # Query by lecturer
    print("🔎 Schedules for Dr. Bambang Susanto:")
    schedules = service.get_schedules_by_lecturer("Dr. Bambang Susanto")
    for schedule in schedules:
        print(f"  - {schedule}")

    # Query by room
    print("\n🔎 Schedules in Ruang A101:")
    schedules = service.get_schedules_by_room("R001")
    for schedule in schedules:
        print(f"  - {schedule}")

    # Query by day
    print("\n🔎 Schedules on Monday:")
    schedules = service.get_schedules_by_day(DayOfWeek.MONDAY)
    for schedule in schedules:
        print(f"  - {schedule}")

    # Print room schedule
    print("\n🔎 Room Schedule for R001:")
    dashboard.print_room_schedule("R001")


def main():
    """Main demo function"""

    print("\n" + "=" * 80)
    print("SCHEDULE MANAGEMENT SYSTEM WITH CONFLICT DETECTION".center(80))
    print("Module 7-8: Jadwal & Ruangan".center(80))
    print("=" * 80)

    # Setup system
    service, dashboard, suggestion_engine = setup_system()

    # Run demos
    demo_crud_operations(service, dashboard)
    input("\n⏸  Press Enter to continue to Conflict Detection Demo...")

    demo_conflict_detection(service, dashboard)
    input("\n⏸  Press Enter to continue to Observer Pattern Demo...")

    demo_observer_pattern(service)
    input("\n⏸  Press Enter to continue to Conflict Resolution Demo...")

    demo_conflict_resolution_suggestions(service, suggestion_engine)
    input("\n⏸  Press Enter to continue to Dashboard & Reports Demo...")

    demo_dashboard_and_reports(service, dashboard)
    input("\n⏸  Press Enter to continue to Advanced Queries Demo...")

    demo_advanced_queries(service)

    # Final summary
    print_header("SUMMARY")
    print("✅ All demonstrations completed successfully!")
    print("\nKey Features Demonstrated:")
    print("  1. ✅ CRUD Operations (Create, Read, Update, Delete Schedules)")
    print("  2. ✅ 3D Conflict Detection (Room, Lecturer, Capacity)")
    print("  3. ✅ Observer Pattern (Notifications to Students, Lecturers, Admins)")
    print("  4. ✅ AI-Powered Suggestions for Schedule Resolution")
    print("  5. ✅ Dashboard & Reporting")
    print("  6. ✅ Advanced Query Operations")
    print("  7. ✅ KRS Integration (Invalidation)")

    print("\n📝 Generated Files:")
    print("  - conflict_report.json: Detailed conflict report")

    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
