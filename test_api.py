"""
REST API Test & Demo Script
Demonstrates all API endpoints with comprehensive examples
"""

import time
import sys
from api_client import ScheduleAPIClient

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}")

def print_subsection(title):
    """Print a formatted subsection header"""
    print(f"\n--- {title} ---")

def test_api():
    """Test all API endpoints"""
    
    print_section("SCHEDULE MANAGEMENT SYSTEM - API TEST & DEMO")
    
    # Initialize client
    print("\n🔌 Connecting to API...")
    client = ScheduleAPIClient()
    
    # Test connection
    if not client.test_connection():
        print("\n❌ API server is not running!")
        print("Start the API server with: python api.py")
        sys.exit(1)
    
    # ==============================================================================
    # HEALTH & INFO TESTS
    # ==============================================================================
    
    print_section("1. HEALTH & INFO ENDPOINTS")
    
    print_subsection("1.1 API Information")
    try:
        response = client.get_info()
        print(f"✅ API Name: {response['data']['name']}")
        print(f"   Version: {response['data']['version']}")
        print(f"   Features: {len(response['data']['features'])} available")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print_subsection("1.2 API Documentation")
    try:
        response = client.get_docs()
        docs = response['data']
        print(f"✅ Endpoints available:")
        for category, endpoints in docs['endpoints'].items():
            print(f"   {category}: {len(endpoints)} endpoints")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # ==============================================================================
    # ROOM MANAGEMENT TESTS
    # ==============================================================================
    
    print_section("2. ROOM MANAGEMENT")
    
    print_subsection("2.1 Creating Rooms")
    rooms_to_create = [
        ("R001", "Ruang Kuliah A", 40, "Building A"),
        ("R002", "Ruang Kuliah B", 35, "Building A"),
        ("R003", "Ruang Seminar", 20, "Building B"),
        ("R004", "Lab Komputer", 30, "Building B"),
    ]
    
    created_rooms = []
    for room_id, name, capacity, building in rooms_to_create:
        try:
            response = client.create_room(room_id, name, capacity, building)
            created_rooms.append(room_id)
            print(f"✅ Created: {name} ({capacity} seats)")
        except Exception as e:
            print(f"❌ Error creating {room_id}: {e}")
    
    print_subsection("2.2 Listing All Rooms")
    try:
        response = client.list_rooms()
        rooms = response['data']
        print(f"✅ Total rooms: {len(rooms)}")
        for room in rooms:
            print(f"   • {room['room_id']}: {room['room_name']} ({room['capacity']} seats) - {room['building']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print_subsection("2.3 Getting Specific Room")
    try:
        response = client.get_room("R001")
        room = response['data']
        print(f"✅ Room Details:")
        print(f"   ID: {room['room_id']}")
        print(f"   Name: {room['room_name']}")
        print(f"   Capacity: {room['capacity']}")
        print(f"   Building: {room['building']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # ==============================================================================
    # SCHEDULE MANAGEMENT TESTS
    # ==============================================================================
    
    print_section("3. SCHEDULE MANAGEMENT")
    
    print_subsection("3.1 Creating Schedules")
    schedules_to_create = [
        {
            "schedule_id": "SCH001",
            "course_name": "Introduction to Python",
            "course_code": "CS101",
            "lecturer_name": "Dr. Smith",
            "day": "MONDAY",
            "start_time": "09:00",
            "end_time": "11:00",
            "room_id": "R001",
            "num_students": 30
        },
        {
            "schedule_id": "SCH002",
            "course_name": "Data Structures",
            "course_code": "CS102",
            "lecturer_name": "Dr. Johnson",
            "day": "TUESDAY",
            "start_time": "10:00",
            "end_time": "12:00",
            "room_id": "R002",
            "num_students": 25
        },
        {
            "schedule_id": "SCH003",
            "course_name": "Web Development",
            "course_code": "CS103",
            "lecturer_name": "Dr. Williams",
            "day": "WEDNESDAY",
            "start_time": "14:00",
            "end_time": "16:00",
            "room_id": "R001",
            "num_students": 28
        },
        {
            "schedule_id": "SCH004",
            "course_name": "Database Design",
            "course_code": "CS104",
            "lecturer_name": "Dr. Smith",
            "day": "THURSDAY",
            "start_time": "09:00",
            "end_time": "11:00",
            "room_id": "R003",
            "num_students": 22
        },
    ]
    
    created_schedules = []
    for sched in schedules_to_create:
        try:
            response = client.create_schedule(**sched)
            created_schedules.append(sched['schedule_id'])
            print(f"✅ Created: {sched['course_name']} ({sched['schedule_id']})")
        except Exception as e:
            print(f"❌ Error creating {sched['schedule_id']}: {e}")
    
    print_subsection("3.2 Listing All Schedules")
    try:
        response = client.list_schedules()
        schedules = response['data']
        print(f"✅ Total schedules: {len(schedules)}")
        for sched in schedules[:3]:  # Show first 3
            print(f"   • {sched['course_code']}: {sched['course_name']} on {sched['day']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print_subsection("3.3 Getting Specific Schedule")
    try:
        response = client.get_schedule("SCH001")
        sched = response['data']
        print(f"✅ Schedule Details:")
        print(f"   Course: {sched['course_name']} ({sched['course_code']})")
        print(f"   Lecturer: {sched['lecturer_name']}")
        print(f"   Day/Time: {sched['day']} {sched['time_slot']}")
        print(f"   Room: {sched['room_name']} ({sched['num_students']}/{sched['capacity']} students)")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print_subsection("3.4 Updating Schedule")
    try:
        response = client.update_schedule("SCH001", lecturer_name="Dr. Anderson", num_students=32)
        sched = response['data']
        print(f"✅ Schedule Updated:")
        print(f"   New Lecturer: {sched['lecturer_name']}")
        print(f"   New Students: {sched['num_students']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # ==============================================================================
    # SCHEDULE QUERY TESTS
    # ==============================================================================
    
    print_section("4. SCHEDULE QUERIES")
    
    print_subsection("4.1 Get Schedules by Lecturer")
    try:
        response = client.get_schedules_by_lecturer("Dr. Smith")
        schedules = response['data']
        print(f"✅ Dr. Smith has {len(schedules)} schedules:")
        for sched in schedules:
            print(f"   • {sched['course_name']} - {sched['day']} {sched['time_slot']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print_subsection("4.2 Get Schedules by Room")
    try:
        response = client.get_schedules_by_room("R001")
        schedules = response['data']
        print(f"✅ Room R001 has {len(schedules)} schedules:")
        for sched in schedules:
            print(f"   • {sched['course_name']} - {sched['day']} {sched['time_slot']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print_subsection("4.3 Get Schedules by Day")
    try:
        response = client.get_schedules_by_day("MONDAY")
        schedules = response['data']
        print(f"✅ MONDAY has {len(schedules)} schedules:")
        for sched in schedules:
            print(f"   • {sched['course_name']} at {sched['time_slot']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # ==============================================================================
    # CONFLICT DETECTION TESTS
    # ==============================================================================
    
    print_section("5. CONFLICT DETECTION")
    
    # Create conflicting schedules
    print_subsection("5.1 Creating Schedules with Potential Conflicts")
    try:
        # Same room, overlapping time
        client.create_schedule(
            schedule_id="SCH005",
            course_name="Conflict Test 1",
            course_code="CS105",
            lecturer_name="Dr. Brown",
            day="MONDAY",
            start_time="09:30",
            end_time="10:30",
            room_id="R001",
            num_students=25
        )
        print(f"✅ Created conflicting schedule SCH005")
    except Exception as e:
        print(f"⚠️  Note: {e}")
    
    print_subsection("5.2 Detecting All Conflicts")
    time.sleep(1)  # Give time for conflict detection
    try:
        response = client.get_conflicts()
        conflicts = response['data']
        print(f"✅ Total conflicts detected: {len(conflicts)}")
        for conflict in conflicts:
            print(f"   • Type: {conflict['conflict_type']}")
            print(f"     Description: {conflict['description']}")
            print(f"     Severity: {conflict['severity']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print_subsection("5.3 Conflict Summary")
    try:
        response = client.get_conflict_summary()
        summary = response['data']
        print(f"✅ Conflict Summary:")
        print(f"   Total Conflicts: {summary['total_conflicts']}")
        print(f"   Conflict Rate: {summary['conflict_rate']}")
        print(f"   By Type:")
        for conflict_type, count in summary['by_type'].items():
            if count > 0:
                print(f"     • {conflict_type}: {count}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # ==============================================================================
    # SUGGESTIONS TESTS
    # ==============================================================================
    
    print_section("6. SCHEDULE SUGGESTIONS")
    
    print_subsection("6.1 Getting Suggestions for Conflicting Schedule")
    try:
        response = client.get_suggestions("SCH001", num_suggestions=3)
        suggestions = response['data']['suggestions']
        print(f"✅ Generated {len(suggestions)} alternative suggestions:")
        for sugg in suggestions:
            print(f"   #{sugg['rank']} - Score: {sugg['score']:.2f}")
            print(f"      {sugg['alternative']['day']} at {sugg['alternative']['time_slot']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # ==============================================================================
    # DASHBOARD & REPORTING TESTS
    # ==============================================================================
    
    print_section("7. DASHBOARD & REPORTING")
    
    print_subsection("7.1 Dashboard Summary")
    try:
        response = client.get_dashboard_summary()
        summary = response['data']
        print(f"✅ Dashboard Summary:")
        print(f"   Total Schedules: {summary['total_schedules']}")
        print(f"   Total Rooms: {summary['total_rooms']}")
        print(f"   Total Conflicts: {summary['total_conflicts']}")
        print(f"   Conflict Rate: {summary['conflict_rate']}")
        print(f"   Lecturers: {summary['lecturers']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print_subsection("7.2 Conflict Report")
    try:
        response = client.get_dashboard_conflicts()
        report = response['data']
        print(f"✅ Conflict Report:")
        print(f"   Total Conflicts: {report['total_conflicts']}")
        print(f"   High Severity: {report['high_severity']}")
        print(f"   Medium Severity: {report['medium_severity']}")
        print(f"   Low Severity: {report['low_severity']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print_subsection("7.3 Room Utilization Report")
    try:
        response = client.get_room_schedule("R001")
        data = response['data']
        print(f"✅ Room R001 - {data['room']['room_name']}:")
        print(f"   Total Schedules: {data['total_schedules']}")
        print(f"   Occupied Slots: {data['utilization']['occupied_slots']}")
        print(f"   Available Slots: {data['utilization']['available_slots']}")
        print(f"   Utilization Rate: {data['utilization']['utilization_rate']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # ==============================================================================
    # OBSERVER TESTS
    # ==============================================================================
    
    print_section("8. OBSERVER PATTERN")
    
    print_subsection("8.1 Attaching Observers")
    observers = [
        ("admin", "ADMIN001", "Administrator", "admin@university.edu"),
        ("lecturer", "LEC001", "Dr. Smith", "smith@university.edu"),
        ("student", "STU001", "John Doe", "john@university.edu"),
    ]
    
    for obs_type, obs_id, name, email in observers:
        try:
            response = client.attach_observer(obs_type, obs_id, name, email)
            print(f"✅ Attached {obs_type}: {name}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # ==============================================================================
    # SUMMARY
    # ==============================================================================
    
    print_section("TEST SUMMARY")
    
    try:
        response = client.list_schedules()
        total_schedules = len(response['data'])
        
        response = client.list_rooms()
        total_rooms = len(response['data'])
        
        response = client.get_conflicts()
        total_conflicts = len(response['data'])
        
        print(f"\n📊 Final Statistics:")
        print(f"   ✅ Total Rooms: {total_rooms}")
        print(f"   ✅ Total Schedules: {total_schedules}")
        print(f"   ✅ Total Conflicts: {total_conflicts}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n{'='*80}")
    print("  🎉 API TEST COMPLETED SUCCESSFULLY!")
    print(f"{'='*80}\n")
    
    print("📚 Next Steps:")
    print("   1. Review API_DOCS.md for complete documentation")
    print("   2. Check api_client.py for Python client usage")
    print("   3. Use cURL to test specific endpoints")
    print("   4. Integrate API into your application\n")


if __name__ == "__main__":
    try:
        test_api()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
