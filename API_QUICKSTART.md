# REST API - Quick Start Guide

## Overview

The Schedule Management System now includes a complete REST API built with Flask. This guide will help you get started quickly.

---

## Installation

### 1. Install Dependencies

```bash
cd c:\Users\erwin\Downloads\MODUL_JADWAL
pip install -r requirements.txt
```

or individually:

```bash
pip install flask flask-cors requests
```

### 2. Verify Installation

```python
python -c "import flask; print(f'Flask {flask.__version__} installed')"
python -c "import requests; print(f'Requests installed')"
```

---

## Running the API Server

### Start the API

```bash
cd c:\Users\erwin\Downloads\MODUL_JADWAL
python api.py
```

Expected output:
```
================================================================================
Schedule Management System - REST API Server
================================================================================

📡 API Server Starting...
🌐 Server: http://localhost:5000
📚 API Docs: http://localhost:5000/api/docs
❤️  Health Check: http://localhost:5000/api/health

Endpoints:
  Rooms:     POST, GET /api/rooms
  Schedules: POST, GET, PUT, DELETE /api/schedules
  Conflicts: GET /api/conflicts
  Dashboard: GET /api/dashboard/...
  Suggestions: POST /api/suggestions

================================================================================
```

### Access the API

- **API Base URL**: http://localhost:5000/api
- **Health Check**: http://localhost:5000/api/health
- **Documentation**: http://localhost:5000/api/docs

---

## Using Python Client

### Simple Example

```python
from api_client import ScheduleAPIClient

# Initialize client
client = ScheduleAPIClient()

# Check connection
client.test_connection()

# Create a room
client.create_room("R001", "Ruang A", 40, "Building A")

# List all rooms
response = client.list_rooms()
print(f"Total rooms: {len(response['data'])}")

# Create schedule
client.create_schedule(
    schedule_id="SCH001",
    course_name="Python 101",
    course_code="CS101",
    lecturer_name="Dr. Smith",
    day="MONDAY",
    start_time="09:00",
    end_time="11:00",
    room_id="R001",
    num_students=30
)

# Get conflicts
conflicts = client.get_conflicts()
print(f"Total conflicts: {len(conflicts['data'])}")

# Get suggestions
suggestions = client.get_suggestions("SCH001", num_suggestions=3)
print(f"Suggestions: {suggestions['data']['suggestions']}")

# Get dashboard summary
dashboard = client.get_dashboard_summary()
print(dashboard['data'])
```

### Complete Example

```python
from api_client import ScheduleAPIClient

client = ScheduleAPIClient()

# 1. Setup rooms
client.create_room("R001", "Ruang Kuliah A", 40)
client.create_room("R002", "Ruang Kuliah B", 35)

# 2. Create schedules
client.create_schedule(
    schedule_id="SCH001",
    course_name="Introduction to Python",
    course_code="CS101",
    lecturer_name="Dr. Smith",
    day="MONDAY",
    start_time="09:00",
    end_time="11:00",
    room_id="R001",
    num_students=30
)

client.create_schedule(
    schedule_id="SCH002",
    course_name="Data Structures",
    course_code="CS102",
    lecturer_name="Dr. Johnson",
    day="TUESDAY",
    start_time="10:00",
    end_time="12:00",
    room_id="R002",
    num_students=25
)

# 3. Query schedules
schedules = client.list_schedules()
print(f"Total schedules: {len(schedules['data'])}")

# 4. Check for conflicts
conflicts = client.get_conflicts()
print(f"Total conflicts: {len(conflicts['data'])}")

# 5. Get suggestions
suggestions = client.get_suggestions("SCH001", num_suggestions=3)
print(f"Generated {len(suggestions['data']['suggestions'])} suggestions")

# 6. Attach observers
client.attach_observer("admin", "ADMIN001", "Administrator", "admin@university.edu")

# 7. Get dashboard
dashboard = client.get_dashboard_summary()
print(f"Dashboard: {dashboard['data']}")
```

---

## Using cURL

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Get API Info
```bash
curl http://localhost:5000/api/info
```

### Create Room
```bash
curl -X POST http://localhost:5000/api/rooms \
  -H "Content-Type: application/json" \
  -d "{
    \"room_id\": \"R001\",
    \"room_name\": \"Ruang Kuliah A\",
    \"capacity\": 40,
    \"building\": \"Building A\"
  }"
```

### List Rooms
```bash
curl http://localhost:5000/api/rooms
```

### Create Schedule
```bash
curl -X POST http://localhost:5000/api/schedules \
  -H "Content-Type: application/json" \
  -d "{
    \"schedule_id\": \"SCH001\",
    \"course_name\": \"Introduction to Python\",
    \"course_code\": \"CS101\",
    \"lecturer_name\": \"Dr. Smith\",
    \"day\": \"MONDAY\",
    \"start_time\": \"09:00\",
    \"end_time\": \"11:00\",
    \"room_id\": \"R001\",
    \"num_students\": 30
  }"
```

### List Schedules
```bash
curl http://localhost:5000/api/schedules
```

### Get Conflicts
```bash
curl http://localhost:5000/api/conflicts
```

### Get Dashboard
```bash
curl http://localhost:5000/api/dashboard/summary
```

---

## Running Tests

### Option 1: Run Full API Test & Demo

```bash
python test_api.py
```

This will:
- Test all endpoints
- Create sample data
- Run comprehensive demonstrations
- Show statistics

### Option 2: Run with Python

```python
python -c "from api_client import ScheduleAPIClient; c = ScheduleAPIClient(); c.test_connection()"
```

---

## API Endpoints Reference

### Rooms
```
POST   /api/rooms                    Create room
GET    /api/rooms                    List all rooms
GET    /api/rooms/{room_id}         Get room details
```

### Schedules
```
POST   /api/schedules                Create schedule
GET    /api/schedules                List all schedules
GET    /api/schedules/{schedule_id} Get schedule details
PUT    /api/schedules/{schedule_id} Update schedule
DELETE /api/schedules/{schedule_id} Delete schedule
```

### Schedule Queries
```
GET    /api/schedules/lecturer/{lecturer_name}  Get by lecturer
GET    /api/schedules/room/{room_id}             Get by room
GET    /api/schedules/day/{day}                  Get by day
```

### Conflicts
```
GET    /api/conflicts                      Get all conflicts
GET    /api/conflicts/{schedule_id}       Get conflicts for schedule
GET    /api/conflicts/summary             Get conflict summary
```

### Suggestions
```
POST   /api/suggestions               Get alternative suggestions
```

### Dashboard
```
GET    /api/dashboard/summary              Get summary
GET    /api/dashboard/conflicts            Get conflict report
GET    /api/dashboard/room-schedule/{id}   Get room schedule
```

### Observers
```
POST   /api/observers                 Attach observer
```

### Health & Info
```
GET    /api/health                    Health check
GET    /api/info                      API information
GET    /api/docs                      Documentation
```

---

## Common Use Cases

### Use Case 1: Schedule a Course

```python
from api_client import ScheduleAPIClient

client = ScheduleAPIClient()

# 1. Create room if not exists
client.create_room("R001", "Ruang Kuliah A", 40)

# 2. Create schedule
response = client.create_schedule(
    schedule_id="CS101_S1",
    course_name="Introduction to Computer Science",
    course_code="CS101",
    lecturer_name="Dr. Smith",
    day="MONDAY",
    start_time="09:00",
    end_time="11:00",
    room_id="R001",
    num_students=35
)

print(f"Schedule created: {response['data']['schedule_id']}")
```

### Use Case 2: Check for Conflicts

```python
# Create conflicting schedule
client.create_schedule(
    schedule_id="CS102_S1",
    course_name="Data Structures",
    course_code="CS102",
    lecturer_name="Dr. Smith",  # Same lecturer
    day="MONDAY",
    start_time="10:30",  # Overlapping time
    end_time="12:30",
    room_id="R001",  # Same room
    num_students=25
)

# Check conflicts
conflicts = client.get_conflicts()
for conflict in conflicts['data']:
    print(f"Conflict: {conflict['description']}")
    print(f"Type: {conflict['conflict_type']}")
    print(f"Severity: {conflict['severity']}")
```

### Use Case 3: Get Alternative Times

```python
# Get suggestions for conflicting schedule
suggestions = client.get_suggestions("CS102_S1", num_suggestions=3)

print("Alternative times:")
for sugg in suggestions['data']['suggestions']:
    print(f"  #{sugg['rank']} - Score: {sugg['score']:.2f}")
    print(f"     {sugg['alternative']['day']} at {sugg['alternative']['time_slot']}")
```

### Use Case 4: Monitor Utilization

```python
# Get room utilization
response = client.get_room_schedule("R001")
data = response['data']

print(f"Room: {data['room']['room_name']}")
print(f"Schedules: {data['total_schedules']}")
print(f"Utilization: {data['utilization']['utilization_rate']}")
```

### Use Case 5: Get Lecturer Schedule

```python
# Get all schedules for a lecturer
response = client.get_schedules_by_lecturer("Dr. Smith")

print(f"Dr. Smith's Schedules:")
for sched in response['data']:
    print(f"  • {sched['course_name']} on {sched['day']} at {sched['time_slot']}")
```

---

## Response Examples

### Success Response
```json
{
    "status": "success",
    "message": "Schedule created successfully",
    "data": {
        "schedule_id": "SCH001",
        "course_name": "Introduction to Python",
        "course_code": "CS101",
        "lecturer_name": "Dr. Smith",
        "day": "MONDAY",
        "time_slot": "09:00-11:00",
        "room_id": "R001",
        "room_name": "Ruang Kuliah A",
        "capacity": 40,
        "num_students": 30,
        "created_at": "2026-01-17T10:30:00.000000",
        "updated_at": "2026-01-17T10:30:00.000000"
    }
}
```

### Error Response
```json
{
    "status": "error",
    "message": "Room R999 not found",
    "details": null
}
```

---

## Troubleshooting

### Problem: Connection Refused
**Solution:** Make sure API server is running:
```bash
python api.py
```

### Problem: Port 5000 Already in Use
**Solution:** Kill the existing process or use a different port:
```bash
# Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Problem: Module Not Found
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Problem: Invalid Time Format
**Solution:** Use HH:MM format (24-hour):
```python
"start_time": "09:00"  # Correct
"start_time": "9:00"   # Incorrect
```

### Problem: Room Not Found
**Solution:** Create room first:
```python
client.create_room("R001", "Ruang A", 40)
client.create_schedule(..., room_id="R001", ...)
```

---

## Performance Tips

1. **Batch Operations**: Create multiple rooms/schedules before querying
2. **Caching**: Cache API responses if not real-time critical
3. **Async Requests**: Use async HTTP client for parallel requests
4. **Indexing**: Use database instead of in-memory for large datasets

---

## Security Considerations

For production deployment:
1. Add authentication (JWT, OAuth2)
2. Add authorization (role-based access)
3. Add rate limiting
4. Use HTTPS
5. Validate and sanitize inputs
6. Add CORS restrictions

---

## Documentation

- **Complete API Docs**: See `API_DOCS.md`
- **System Overview**: See `README.md`
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`
- **Code Examples**: See `quick_start.py`

---

## Support

For issues or questions:
1. Check `API_DOCS.md` for complete documentation
2. Review code comments in `api.py` and `api_client.py`
3. Run `test_api.py` to verify setup
4. Check error messages in API response

---

## Files

- `api.py` - Flask REST API server
- `api_client.py` - Python client library
- `test_api.py` - Comprehensive API tests
- `API_DOCS.md` - Complete API documentation
- `schedule_system.py` - Core scheduling system
- `requirements.txt` - Python dependencies

---

**Version**: 1.0  
**Status**: Production Ready ✅  
**Last Updated**: January 17, 2026
