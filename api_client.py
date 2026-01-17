"""
Client library for Schedule Management System API
Provides easy-to-use Python client for interacting with the REST API
"""

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScheduleAPIClient:
    """Python client for Schedule Management System API"""
    
    def __init__(self, base_url: str = "http://localhost:5000/api"):
        """Initialize the API client
        
        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make HTTP request to API
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request body data
            
        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = self.session.get(url)
            elif method == "POST":
                response = self.session.post(url, json=data)
            elif method == "PUT":
                response = self.session.put(url, json=data)
            elif method == "DELETE":
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error: Unable to connect to {self.base_url}")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Request error: {str(e)}")
            raise
    
    # Health & Info Methods
    
    def health_check(self) -> Dict:
        """Check API health status"""
        return self._make_request("GET", "/health")
    
    def get_info(self) -> Dict:
        """Get API information"""
        return self._make_request("GET", "/info")
    
    def get_docs(self) -> Dict:
        """Get API documentation"""
        return self._make_request("GET", "/docs")
    
    # Room Methods
    
    def create_room(self, room_id: str, room_name: str, capacity: int, 
                   building: str = "Main Building") -> Dict:
        """Create a new room
        
        Args:
            room_id: Unique room identifier
            room_name: Name of the room
            capacity: Room capacity (number of students)
            building: Building name
            
        Returns:
            Created room data
        """
        data = {
            "room_id": room_id,
            "room_name": room_name,
            "capacity": capacity,
            "building": building
        }
        return self._make_request("POST", "/rooms", data)
    
    def list_rooms(self) -> Dict:
        """List all rooms"""
        return self._make_request("GET", "/rooms")
    
    def get_room(self, room_id: str) -> Dict:
        """Get room details"""
        return self._make_request("GET", f"/rooms/{room_id}")
    
    # Schedule Methods
    
    def create_schedule(self, schedule_id: str, course_name: str, course_code: str,
                       lecturer_name: str, day: str, start_time: str, end_time: str,
                       room_id: str, num_students: int, krs_id: Optional[str] = None) -> Dict:
        """Create a new schedule
        
        Args:
            schedule_id: Unique schedule identifier
            course_name: Course name
            course_code: Course code
            lecturer_name: Lecturer name
            day: Day of week (MONDAY, TUESDAY, etc.)
            start_time: Start time (HH:MM format)
            end_time: End time (HH:MM format)
            room_id: Room identifier
            num_students: Number of students
            krs_id: Optional KRS identifier
            
        Returns:
            Created schedule data
        """
        data = {
            "schedule_id": schedule_id,
            "course_name": course_name,
            "course_code": course_code,
            "lecturer_name": lecturer_name,
            "day": day,
            "start_time": start_time,
            "end_time": end_time,
            "room_id": room_id,
            "num_students": num_students,
            "krs_id": krs_id
        }
        return self._make_request("POST", "/schedules", data)
    
    def list_schedules(self) -> Dict:
        """List all schedules"""
        return self._make_request("GET", "/schedules")
    
    def get_schedule(self, schedule_id: str) -> Dict:
        """Get schedule details"""
        return self._make_request("GET", f"/schedules/{schedule_id}")
    
    def update_schedule(self, schedule_id: str, **kwargs) -> Dict:
        """Update a schedule
        
        Args:
            schedule_id: Schedule identifier
            **kwargs: Fields to update (course_name, lecturer_name, day, etc.)
            
        Returns:
            Updated schedule data
        """
        return self._make_request("PUT", f"/schedules/{schedule_id}", kwargs)
    
    def delete_schedule(self, schedule_id: str) -> Dict:
        """Delete a schedule"""
        return self._make_request("DELETE", f"/schedules/{schedule_id}")
    
    # Schedule Query Methods
    
    def get_schedules_by_lecturer(self, lecturer_name: str) -> Dict:
        """Get schedules by lecturer name"""
        return self._make_request("GET", f"/schedules/lecturer/{lecturer_name}")
    
    def get_schedules_by_room(self, room_id: str) -> Dict:
        """Get schedules by room"""
        return self._make_request("GET", f"/schedules/room/{room_id}")
    
    def get_schedules_by_day(self, day: str) -> Dict:
        """Get schedules by day"""
        return self._make_request("GET", f"/schedules/day/{day}")
    
    # Conflict Methods
    
    def get_conflicts(self) -> Dict:
        """Get all conflicts"""
        return self._make_request("GET", "/conflicts")
    
    def get_conflicts_for_schedule(self, schedule_id: str) -> Dict:
        """Get conflicts for a specific schedule"""
        return self._make_request("GET", f"/conflicts/{schedule_id}")
    
    def get_conflict_summary(self) -> Dict:
        """Get conflict summary"""
        return self._make_request("GET", "/conflicts/summary")
    
    # Suggestion Methods
    
    def get_suggestions(self, schedule_id: str, num_suggestions: int = 3) -> Dict:
        """Get alternative schedule suggestions
        
        Args:
            schedule_id: Schedule identifier
            num_suggestions: Number of suggestions to generate
            
        Returns:
            Suggestions with scores
        """
        data = {
            "schedule_id": schedule_id,
            "num_suggestions": num_suggestions
        }
        return self._make_request("POST", "/suggestions", data)
    
    # Dashboard Methods
    
    def get_dashboard_summary(self) -> Dict:
        """Get dashboard summary"""
        return self._make_request("GET", "/dashboard/summary")
    
    def get_dashboard_conflicts(self) -> Dict:
        """Get conflict report from dashboard"""
        return self._make_request("GET", "/dashboard/conflicts")
    
    def get_room_schedule(self, room_id: str) -> Dict:
        """Get room schedule and utilization"""
        return self._make_request("GET", f"/dashboard/room-schedule/{room_id}")
    
    # Observer Methods
    
    def attach_observer(self, observer_type: str, observer_id: str, 
                       name: str, email: str) -> Dict:
        """Attach an observer to receive notifications
        
        Args:
            observer_type: Type of observer (student, lecturer, admin)
            observer_id: Observer identifier
            name: Observer name
            email: Observer email
            
        Returns:
            Observer attachment confirmation
        """
        data = {
            "type": observer_type,
            "id": observer_id,
            "name": name,
            "email": email
        }
        return self._make_request("POST", "/observers", data)
    
    # Utility Methods
    
    def print_response(self, response: Dict, title: str = "Response"):
        """Pretty print API response"""
        print(f"\n{'='*80}")
        print(f"{title}")
        print(f"{'='*80}")
        print(json.dumps(response, indent=2))
        print(f"{'='*80}\n")
    
    def test_connection(self) -> bool:
        """Test API connection"""
        try:
            response = self.health_check()
            if response['status'] == 'success':
                print("✅ API Connection Successful!")
                print(f"   Status: {response['data']['status']}")
                print(f"   Version: {response['data']['version']}")
                return True
        except Exception as e:
            print(f"❌ API Connection Failed: {str(e)}")
            return False


if __name__ == "__main__":
    print("="*80)
    print("Schedule Management System - Python API Client")
    print("="*80 + "\n")
    
    # Initialize client
    client = ScheduleAPIClient()
    
    # Test connection
    print("Testing API connection...")
    if not client.test_connection():
        print("\n❌ Make sure the API server is running:")
        print("   python api.py\n")
        exit(1)
    
    # Example usage
    print("\nExample Usage:\n")
    
    # Create rooms
    print("1. Creating rooms...")
    try:
        client.create_room("R001", "Ruang A", 40, "Building A")
        client.create_room("R002", "Ruang B", 30, "Building A")
        print("   ✅ Rooms created\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # List rooms
    print("2. Listing rooms...")
    try:
        response = client.list_rooms()
        rooms = response['data']
        print(f"   ✅ Found {len(rooms)} rooms\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # Create schedule
    print("3. Creating schedule...")
    try:
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
        print("   ✅ Schedule created\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # Get schedules
    print("4. Getting schedules...")
    try:
        response = client.list_schedules()
        schedules = response['data']
        print(f"   ✅ Found {len(schedules)} schedules\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # Get conflicts
    print("5. Checking conflicts...")
    try:
        response = client.get_conflicts()
        conflicts = response['data']
        print(f"   ✅ Found {len(conflicts)} conflicts\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # Get dashboard
    print("6. Getting dashboard summary...")
    try:
        response = client.get_dashboard_summary()
        client.print_response(response, "Dashboard Summary")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
