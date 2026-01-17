"""
REST API for Schedule Management System
Using Flask to provide HTTP endpoints for the scheduling system
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, time
from typing import Dict, Any, Tuple
import json
import logging
from schedule_system import (
    SchedulingService, Room, Schedule, TimeSlot, DayOfWeek, 
    ConflictDetectionEngine, SchedulingSuggestionEngine, DashboardService,
    StudentObserver, LecturerObserver, AdminObserver, EventType
)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize service
service = SchedulingService()
dashboard = DashboardService(service)

# Add default observers
admin = AdminObserver("admin", "Administrator", "admin@university.edu")
service.attach(admin)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def success_response(data: Any, status_code: int = 200, message: str = "Success"):
    """Create a successful JSON response"""
    return jsonify({
        "status": "success",
        "message": message,
        "data": data
    }), status_code


def error_response(message: str, status_code: int = 400, details: str = None):
    """Create an error JSON response"""
    response = {
        "status": "error",
        "message": message
    }
    if details:
        response["details"] = details
    return jsonify(response), status_code


def parse_time_string(time_str: str) -> time:
    """Parse time string in format HH:MM"""
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        raise ValueError(f"Invalid time format. Use HH:MM")


def parse_day_string(day_str: str) -> DayOfWeek:
    """Parse day string to DayOfWeek enum"""
    try:
        return DayOfWeek[day_str.upper()]
    except KeyError:
        raise ValueError(f"Invalid day. Use: {', '.join([d.name for d in DayOfWeek])}")


def schedule_to_dict(schedule: Schedule) -> Dict:
    """Convert Schedule object to dictionary"""
    return {
        "schedule_id": schedule.schedule_id,
        "course_name": schedule.course_name,
        "course_code": schedule.course_code,
        "lecturer_name": schedule.lecturer_name,
        "day": schedule.day.name,
        "time_slot": str(schedule.time_slot),
        "start_time": schedule.time_slot.start_time.strftime("%H:%M"),
        "end_time": schedule.time_slot.end_time.strftime("%H:%M"),
        "room_id": schedule.room.room_id,
        "room_name": schedule.room.room_name,
        "capacity": schedule.room.capacity,
        "num_students": schedule.num_students,
        "building": schedule.room.building,
        "krs_id": schedule.krs_id,
        "created_at": schedule.created_at.isoformat(),
        "updated_at": schedule.updated_at.isoformat()
    }


def room_to_dict(room: Room) -> Dict:
    """Convert Room object to dictionary"""
    return {
        "room_id": room.room_id,
        "room_name": room.room_name,
        "capacity": room.capacity,
        "building": room.building
    }


def conflict_to_dict(conflict) -> Dict:
    """Convert ScheduleConflict object to dictionary"""
    return {
        "conflict_id": conflict.conflict_id,
        "conflict_type": conflict.conflict_type.value,
        "schedule1_id": conflict.schedule1_id,
        "schedule2_id": conflict.schedule2_id,
        "description": conflict.description,
        "severity": conflict.severity,
        "detected_at": conflict.detected_at.isoformat()
    }


# ============================================================================
# HEALTH & INFO ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return success_response({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0"
    }, message="API is running")


@app.route('/api/info', methods=['GET'])
def api_info():
    """Get API information"""
    return success_response({
        "name": "Schedule Management System API",
        "version": "1.0",
        "description": "REST API for academic schedule management with conflict detection",
        "features": [
            "Room management",
            "Schedule CRUD operations",
            "3D conflict detection",
            "Observer pattern notifications",
            "AI-powered suggestions",
            "Dashboard and reporting"
        ],
        "endpoints": "/api/docs"
    }, message="API Information")


@app.route('/api/docs', methods=['GET'])
def api_docs():
    """API documentation"""
    docs = {
        "title": "Schedule Management System API",
        "version": "1.0",
        "baseUrl": "/api",
        "endpoints": {
            "Rooms": {
                "POST /rooms": "Create a new room",
                "GET /rooms": "List all rooms",
                "GET /rooms/{room_id}": "Get room details"
            },
            "Schedules": {
                "POST /schedules": "Create a new schedule",
                "GET /schedules": "List all schedules",
                "GET /schedules/{schedule_id}": "Get schedule details",
                "PUT /schedules/{schedule_id}": "Update schedule",
                "DELETE /schedules/{schedule_id}": "Delete schedule",
                "GET /schedules/lecturer/{lecturer_name}": "Get schedules by lecturer",
                "GET /schedules/room/{room_id}": "Get schedules by room",
                "GET /schedules/day/{day}": "Get schedules by day"
            },
            "Conflicts": {
                "GET /conflicts": "Get all conflicts",
                "GET /conflicts/{schedule_id}": "Get conflicts for schedule",
                "GET /conflicts/summary": "Get conflict summary"
            },
            "Suggestions": {
                "POST /suggestions": "Get alternative schedule suggestions"
            },
            "Dashboard": {
                "GET /dashboard/summary": "Get dashboard summary",
                "GET /dashboard/conflicts": "Get conflict report",
                "GET /dashboard/room-schedule/{room_id}": "Get room schedule"
            }
        }
    }
    return success_response(docs, message="API Documentation")


# ============================================================================
# ROOM ENDPOINTS
# ============================================================================

@app.route('/api/rooms', methods=['POST'])
def create_room():
    """Create a new room"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['room_id', 'room_name', 'capacity']
        if not all(field in data for field in required_fields):
            return error_response(f"Missing required fields: {', '.join(required_fields)}")
        
        room = Room(
            room_id=data['room_id'],
            room_name=data['room_name'],
            capacity=int(data['capacity']),
            building=data.get('building', 'Main Building')
        )
        
        service.add_room(room)
        logger.info(f"Room created: {room.room_id}")
        
        return success_response(room_to_dict(room), 201, "Room created successfully")
    
    except Exception as e:
        logger.error(f"Error creating room: {str(e)}")
        return error_response(f"Error creating room: {str(e)}", 500)


@app.route('/api/rooms', methods=['GET'])
def list_rooms():
    """List all rooms"""
    try:
        rooms = service.list_rooms()
        return success_response(
            [room_to_dict(room) for room in rooms],
            message=f"Retrieved {len(rooms)} rooms"
        )
    except Exception as e:
        logger.error(f"Error listing rooms: {str(e)}")
        return error_response(f"Error listing rooms: {str(e)}", 500)


@app.route('/api/rooms/<room_id>', methods=['GET'])
def get_room(room_id):
    """Get room details"""
    try:
        room = service.get_room(room_id)
        if not room:
            return error_response(f"Room {room_id} not found", 404)
        return success_response(room_to_dict(room), message="Room retrieved")
    except Exception as e:
        logger.error(f"Error getting room: {str(e)}")
        return error_response(f"Error getting room: {str(e)}", 500)


# ============================================================================
# SCHEDULE ENDPOINTS
# ============================================================================

@app.route('/api/schedules', methods=['POST'])
def create_schedule():
    """Create a new schedule"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['schedule_id', 'course_name', 'course_code', 
                          'lecturer_name', 'day', 'start_time', 'end_time',
                          'room_id', 'num_students']
        if not all(field in data for field in required_fields):
            return error_response(f"Missing required fields: {', '.join(required_fields)}")
        
        # Parse time and day
        start_time = parse_time_string(data['start_time'])
        end_time = parse_time_string(data['end_time'])
        day = parse_day_string(data['day'])
        
        # Get room
        room = service.get_room(data['room_id'])
        if not room:
            return error_response(f"Room {data['room_id']} not found", 404)
        
        # Create time slot
        time_slot = TimeSlot(start_time, end_time)
        
        # Create schedule
        schedule = Schedule(
            schedule_id=data['schedule_id'],
            course_name=data['course_name'],
            course_code=data['course_code'],
            lecturer_name=data['lecturer_name'],
            day=day,
            time_slot=time_slot,
            room=room,
            num_students=int(data['num_students']),
            krs_id=data.get('krs_id')
        )
        
        service.create_schedule(schedule)
        logger.info(f"Schedule created: {schedule.schedule_id}")
        
        return success_response(schedule_to_dict(schedule), 201, "Schedule created successfully")
    
    except ValueError as e:
        return error_response(f"Invalid input: {str(e)}", 400)
    except Exception as e:
        logger.error(f"Error creating schedule: {str(e)}")
        return error_response(f"Error creating schedule: {str(e)}", 500)


@app.route('/api/schedules', methods=['GET'])
def list_schedules():
    """List all schedules"""
    try:
        schedules = service.list_schedules()
        return success_response(
            [schedule_to_dict(schedule) for schedule in schedules],
            message=f"Retrieved {len(schedules)} schedules"
        )
    except Exception as e:
        logger.error(f"Error listing schedules: {str(e)}")
        return error_response(f"Error listing schedules: {str(e)}", 500)


@app.route('/api/schedules/<schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    """Get schedule details"""
    try:
        schedule = service.get_schedule(schedule_id)
        if not schedule:
            return error_response(f"Schedule {schedule_id} not found", 404)
        return success_response(schedule_to_dict(schedule), message="Schedule retrieved")
    except Exception as e:
        logger.error(f"Error getting schedule: {str(e)}")
        return error_response(f"Error getting schedule: {str(e)}", 500)


@app.route('/api/schedules/<schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    """Update a schedule"""
    try:
        data = request.get_json()
        
        # Get existing schedule
        existing = service.get_schedule(schedule_id)
        if not existing:
            return error_response(f"Schedule {schedule_id} not found", 404)
        
        # Parse time and day if provided
        start_time = parse_time_string(data.get('start_time', existing.time_slot.start_time.strftime("%H:%M")))
        end_time = parse_time_string(data.get('end_time', existing.time_slot.end_time.strftime("%H:%M")))
        day = parse_day_string(data.get('day', existing.day.name))
        
        # Get room if provided
        room_id = data.get('room_id', existing.room.room_id)
        room = service.get_room(room_id)
        if not room:
            return error_response(f"Room {room_id} not found", 404)
        
        # Create updated schedule
        updated_schedule = Schedule(
            schedule_id=schedule_id,
            course_name=data.get('course_name', existing.course_name),
            course_code=data.get('course_code', existing.course_code),
            lecturer_name=data.get('lecturer_name', existing.lecturer_name),
            day=day,
            time_slot=TimeSlot(start_time, end_time),
            room=room,
            num_students=int(data.get('num_students', existing.num_students)),
            krs_id=data.get('krs_id', existing.krs_id)
        )
        
        service.update_schedule(schedule_id, updated_schedule)
        logger.info(f"Schedule updated: {schedule_id}")
        
        return success_response(schedule_to_dict(updated_schedule), message="Schedule updated successfully")
    
    except ValueError as e:
        return error_response(f"Invalid input: {str(e)}", 400)
    except Exception as e:
        logger.error(f"Error updating schedule: {str(e)}")
        return error_response(f"Error updating schedule: {str(e)}", 500)


@app.route('/api/schedules/<schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    """Delete a schedule"""
    try:
        service.delete_schedule(schedule_id)
        logger.info(f"Schedule deleted: {schedule_id}")
        return success_response({"deleted": schedule_id}, message="Schedule deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting schedule: {str(e)}")
        return error_response(f"Error deleting schedule: {str(e)}", 500)


# ============================================================================
# SCHEDULE QUERY ENDPOINTS
# ============================================================================

@app.route('/api/schedules/lecturer/<lecturer_name>', methods=['GET'])
def get_schedules_by_lecturer(lecturer_name):
    """Get schedules by lecturer name"""
    try:
        schedules = service.get_schedules_by_lecturer(lecturer_name)
        return success_response(
            [schedule_to_dict(schedule) for schedule in schedules],
            message=f"Retrieved {len(schedules)} schedules for {lecturer_name}"
        )
    except Exception as e:
        logger.error(f"Error getting schedules by lecturer: {str(e)}")
        return error_response(f"Error getting schedules: {str(e)}", 500)


@app.route('/api/schedules/room/<room_id>', methods=['GET'])
def get_schedules_by_room(room_id):
    """Get schedules by room"""
    try:
        schedules = service.get_schedules_by_room(room_id)
        return success_response(
            [schedule_to_dict(schedule) for schedule in schedules],
            message=f"Retrieved {len(schedules)} schedules for room {room_id}"
        )
    except Exception as e:
        logger.error(f"Error getting schedules by room: {str(e)}")
        return error_response(f"Error getting schedules: {str(e)}", 500)


@app.route('/api/schedules/day/<day>', methods=['GET'])
def get_schedules_by_day(day):
    """Get schedules by day"""
    try:
        day_enum = parse_day_string(day)
        schedules = service.get_schedules_by_day(day_enum)
        return success_response(
            [schedule_to_dict(schedule) for schedule in schedules],
            message=f"Retrieved {len(schedules)} schedules for {day}"
        )
    except ValueError as e:
        return error_response(f"Invalid day: {str(e)}", 400)
    except Exception as e:
        logger.error(f"Error getting schedules by day: {str(e)}")
        return error_response(f"Error getting schedules: {str(e)}", 500)


# ============================================================================
# CONFLICT ENDPOINTS
# ============================================================================

@app.route('/api/conflicts', methods=['GET'])
def get_conflicts():
    """Get all conflicts"""
    try:
        conflicts = service.get_conflicts()
        return success_response(
            [conflict_to_dict(conflict) for conflict in conflicts],
            message=f"Retrieved {len(conflicts)} conflicts"
        )
    except Exception as e:
        logger.error(f"Error getting conflicts: {str(e)}")
        return error_response(f"Error getting conflicts: {str(e)}", 500)


@app.route('/api/conflicts/<schedule_id>', methods=['GET'])
def get_conflicts_for_schedule(schedule_id):
    """Get conflicts for a specific schedule"""
    try:
        conflicts = service.get_conflicts_for_schedule(schedule_id)
        return success_response(
            [conflict_to_dict(conflict) for conflict in conflicts],
            message=f"Retrieved {len(conflicts)} conflicts for schedule {schedule_id}"
        )
    except Exception as e:
        logger.error(f"Error getting conflicts: {str(e)}")
        return error_response(f"Error getting conflicts: {str(e)}", 500)


@app.route('/api/conflicts/summary', methods=['GET'])
def get_conflict_summary():
    """Get conflict summary statistics"""
    try:
        conflicts = service.get_conflicts()
        summary = service.get_conflict_summary()
        return success_response(summary, message="Conflict summary retrieved")
    except Exception as e:
        logger.error(f"Error getting conflict summary: {str(e)}")
        return error_response(f"Error getting conflict summary: {str(e)}", 500)


# ============================================================================
# SUGGESTION ENDPOINTS
# ============================================================================

@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    """Get alternative schedule suggestions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'schedule_id' not in data:
            return error_response("Missing schedule_id")
        
        schedule = service.get_schedule(data['schedule_id'])
        if not schedule:
            return error_response(f"Schedule {data['schedule_id']} not found", 404)
        
        # Generate available slots (for demo purposes)
        available_slots = []
        for day in DayOfWeek:
            for hour in range(7, 18):
                for minute in [0, 30]:
                    start = time(hour, minute)
                    end = time(hour + 1, minute)
                    available_slots.append((day, TimeSlot(start, end)))
        
        # Get suggestions
        engine = SchedulingSuggestionEngine(service)
        suggestions = engine.suggest_alternatives(
            schedule,
            available_slots,
            num_suggestions=data.get('num_suggestions', 3)
        )
        
        result = {
            "original_schedule": schedule_to_dict(schedule),
            "suggestions": [
                {
                    "rank": i + 1,
                    "score": float(suggestion[1]),
                    "alternative": {
                        "day": suggestion[0][0].name,
                        "time_slot": str(suggestion[0][1])
                    }
                }
                for i, suggestion in enumerate(suggestions)
            ]
        }
        
        return success_response(result, message="Suggestions generated")
    
    except Exception as e:
        logger.error(f"Error getting suggestions: {str(e)}")
        return error_response(f"Error getting suggestions: {str(e)}", 500)


# ============================================================================
# DASHBOARD ENDPOINTS
# ============================================================================

@app.route('/api/dashboard/summary', methods=['GET'])
def dashboard_summary():
    """Get dashboard summary"""
    try:
        summary = dashboard.get_dashboard_summary()
        return success_response(summary, message="Dashboard summary retrieved")
    except Exception as e:
        logger.error(f"Error getting dashboard summary: {str(e)}")
        return error_response(f"Error getting summary: {str(e)}", 500)


@app.route('/api/dashboard/conflicts', methods=['GET'])
def dashboard_conflicts():
    """Get conflict report"""
    try:
        report = dashboard.get_conflict_report()
        return success_response(report, message="Conflict report retrieved")
    except Exception as e:
        logger.error(f"Error getting conflict report: {str(e)}")
        return error_response(f"Error getting report: {str(e)}", 500)


@app.route('/api/dashboard/room-schedule/<room_id>', methods=['GET'])
def dashboard_room_schedule(room_id):
    """Get room schedule"""
    try:
        room = service.get_room(room_id)
        if not room:
            return error_response(f"Room {room_id} not found", 404)
        
        schedules = service.get_schedules_by_room(room_id)
        
        result = {
            "room": room_to_dict(room),
            "schedules": [schedule_to_dict(schedule) for schedule in schedules],
            "total_schedules": len(schedules),
            "utilization": {
                "occupied_slots": len(schedules),
                "available_slots": 80 - len(schedules),
                "utilization_rate": f"{(len(schedules) / 80) * 100:.1f}%"
            }
        }
        
        return success_response(result, message="Room schedule retrieved")
    except Exception as e:
        logger.error(f"Error getting room schedule: {str(e)}")
        return error_response(f"Error getting room schedule: {str(e)}", 500)


# ============================================================================
# OBSERVER ENDPOINTS
# ============================================================================

@app.route('/api/observers', methods=['POST'])
def attach_observer():
    """Attach an observer"""
    try:
        data = request.get_json()
        
        observer_type = data.get('type', 'admin').lower()
        observer_id = data.get('id', 'obs_1')
        name = data.get('name', 'Observer')
        email = data.get('email', 'observer@university.edu')
        
        if observer_type == 'student':
            observer = StudentObserver(observer_id, name, email)
        elif observer_type == 'lecturer':
            observer = LecturerObserver(observer_id, name, email)
        elif observer_type == 'admin':
            observer = AdminObserver(observer_id, name, email)
        else:
            return error_response(f"Invalid observer type: {observer_type}", 400)
        
        service.attach(observer)
        logger.info(f"Observer attached: {observer_type} - {observer_id}")
        
        return success_response({
            "type": observer_type,
            "id": observer_id,
            "name": name,
            "email": email
        }, 201, "Observer attached successfully")
    
    except Exception as e:
        logger.error(f"Error attaching observer: {str(e)}")
        return error_response(f"Error attaching observer: {str(e)}", 500)


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return error_response("Endpoint not found", 404)


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return error_response("Method not allowed", 405)


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return error_response("Internal server error", 500)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*80)
    print("Schedule Management System - REST API Server")
    print("="*80)
    print("\n📡 API Server Starting...")
    print(f"🌐 Server: http://localhost:5000")
    print(f"📚 API Docs: http://localhost:5000/api/docs")
    print(f"❤️  Health Check: http://localhost:5000/api/health")
    print("\nEndpoints:")
    print("  Rooms:     POST, GET /api/rooms")
    print("  Schedules: POST, GET, PUT, DELETE /api/schedules")
    print("  Conflicts: GET /api/conflicts")
    print("  Dashboard: GET /api/dashboard/...")
    print("  Suggestions: POST /api/suggestions")
    print("\n" + "="*80 + "\n")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )
