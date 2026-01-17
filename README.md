# SCHEDULE MANAGEMENT SYSTEM

## 📋 Module 7-8: Jadwal & Ruangan (Schedule & Room)

### Sistem Penjadwalan Kuliah dengan Deteksi Otomatis Bentrok Jadwal

---

## 📖 DAFTAR ISI

1. [Gambaran Umum](#gambaran-umum)
2. [Fitur Utama](#fitur-utama)
3. [Arsitektur Sistem](#arsitektur-sistem)
4. [Komponen Utama](#komponen-utama)
5. [Penggunaan](#penggunaan)
6. [Contoh Kode](#contoh-kode)
7. [Testing](#testing)
8. [Hasil Implementasi](#hasil-implementasi)

---

## 📌 Gambaran Umum

Sistem manajemen penjadwalan kuliah yang canggih dengan deteksi otomatis bentrok jadwal 3-dimensi:
- **Bentrok Ruangan**: Satu ruangan digunakan untuk dua kelas pada waktu yang sama
- **Bentrok Dosen**: Satu dosen mengajar dua kelas pada waktu yang sama
- **Melebihi Kapasitas**: Jumlah mahasiswa melebihi kapasitas ruangan

Sistem mengimplementasikan **Observer Pattern** untuk notifikasi real-time kepada:
- Mahasiswa
- Dosen
- Admin Akademik

---

## ✨ Fitur Utama

### 1. **CRUD Operations**
✅ Create, Read, Update, Delete schedules
✅ Manajemen ruangan (Room)
✅ Query scheduling by lecturer, room, atau day

### 2. **3D Conflict Detection Engine**
✅ Deteksi bentrok ruangan
✅ Deteksi bentrok dosen
✅ Deteksi melebihi kapasitas
✅ Algoritma O(n²) untuk perbandingan jadwal

### 3. **Observer Pattern (Pub-Sub)**
✅ NotificationManager mengirim notifikasi saat jadwal berubah
✅ Multiple observer types: Student, Lecturer, Admin
✅ Event types: CREATED, UPDATED, DELETED, CONFLICT_DETECTED, RESOLVED
✅ Notifikasi via logging (dapat diperluas ke Email/SMS/Push)

### 4. **AI-Powered Suggestion Engine**
✅ Merekomendasikan 3 alternatif jadwal
✅ Mempertimbangkan kapasitas ruangan
✅ Menghindari bentrok dengan jadwal dosen
✅ Prioritas: Pagi > Siang > Malam
✅ Menghitung disruption score

### 5. **Dashboard & Reporting**
✅ Summary statistik penjadwalan
✅ Analisis room utilization
✅ Conflict report (exportable to JSON)
✅ Visualisasi jadwal per ruangan

### 6. **KRS Integration**
✅ Invalidasi KRS saat jadwal berubah
✅ Tracking jadwal dengan KRS ID

---

## 🏗️ Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────────┐
│                    Scheduling Service                        │
│                   (ScheduleSubject)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ - CRUD Operations                                    │   │
│  │ - Schedule Management                                │   │
│  │ - Conflict Detection                                 │   │
│  │ - Observer Management                                │   │
│  │ - Room Management                                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │                                           │
         ▼                                           ▼
┌──────────────────────────┐         ┌─────────────────────────┐
│ ConflictDetectionEngine  │         │ SchedulingSuggestion    │
│                          │         │ Engine                  │
│ - Detect Room Conflicts  │         │ - Generate Alternatives │
│ - Detect Lecturer        │         │ - Rank by Preference    │
│   Conflicts              │         │ - Calculate Disruption  │
│ - Detect Capacity Issues │         │   Score                 │
└──────────────────────────┘         └─────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│      Observers (Subscribers)     │
│ ┌──────────────────────────────┐ │
│ │ StudentObserver              │ │
│ │ LecturerObserver             │ │
│ │ AdminObserver                │ │
│ └──────────────────────────────┘ │
└─────────────────────────────────┘
```

---

## 🔧 Komponen Utama

### 1. Data Models

#### TimeSlot
```python
@dataclass
class TimeSlot:
    start_time: time
    end_time: time
    
    def overlaps_with(other: 'TimeSlot') -> bool:
        """Cek apakah time slot overlaps"""
```

#### Room
```python
@dataclass
class Room:
    room_id: str
    room_name: str
    capacity: int
    building: str
    
    def can_accommodate(num_students: int) -> bool:
        """Cek apakah ruangan bisa menampung mahasiswa"""
```

#### Schedule
```python
@dataclass
class Schedule:
    schedule_id: str
    course_name: str
    course_code: str
    lecturer_name: str
    day: DayOfWeek
    time_slot: TimeSlot
    room: Room
    num_students: int
    krs_id: Optional[str]
```

#### ScheduleConflict
```python
@dataclass
class ScheduleConflict:
    conflict_type: ConflictType  # room, lecturer, capacity
    schedule_1: Schedule
    schedule_2: Optional[Schedule]
    description: str
    severity: str  # high, medium, low
```

### 2. Observer Pattern

#### Abstract Observer
```python
class Observer(ABC):
    @abstractmethod
    def update(event_type: EventType, data: Dict) -> None:
        pass
```

#### Concrete Observers
- **StudentObserver**: Notifikasi untuk mahasiswa
- **LecturerObserver**: Notifikasi untuk dosen
- **AdminObserver**: Notifikasi untuk admin akademik

#### Subject (Publisher)
```python
class ScheduleSubject:
    def attach(observer: Observer) -> None
    def detach(observer: Observer) -> None
    def notify(event_type: EventType, data: Dict) -> None
```

### 3. Conflict Detection Algorithm

```python
def detect_schedule_conflicts(schedules: List[Schedule]) -> List[ScheduleConflict]:
    """
    3D Conflict Detection:
    
    1. Room Conflict:
       - Same day AND overlapping time AND same room
    
    2. Lecturer Conflict:
       - Same day AND overlapping time AND same lecturer
    
    3. Capacity Exceeded:
       - num_students > room.capacity
    
    Time Complexity: O(n²)
    Space Complexity: O(n)
    """
```

---

## 💻 Penggunaan

### Installation

```bash
# Python 3.7+
pip install -r requirements.txt
```

### Basic Usage

```python
from schedule_system import *

# Initialize service
service = SchedulingService()

# Add rooms
room = Room("R001", "Ruang A101", 40, "Building A")
service.add_room(room)

# Create observers
student = StudentObserver("STU001", "Andi", "andi@email.com")
lecturer = LecturerObserver("LEC001", "Dr. Bambang", "bambang@email.com")
admin = AdminObserver("ADMIN001", "Hendra", "hendra@email.com")

# Attach observers
service.attach(student)
service.attach(lecturer)
service.attach(admin)

# Create schedule
schedule = Schedule(
    schedule_id="SCH001",
    course_name="Kalkulus I",
    course_code="MTH101",
    lecturer_name="Dr. Bambang",
    day=DayOfWeek.MONDAY,
    time_slot=TimeSlot(time(8, 0), time(10, 0)),
    room=room,
    num_students=35
)

# Save schedule (akan trigger notifikasi ke observers)
service.create_schedule(schedule)

# Check conflicts
conflicts = service.get_conflicts()
if conflicts:
    print(f"Found {len(conflicts)} conflicts!")
    for conflict in conflicts:
        print(f"  - {conflict}")
```

### Advanced Queries

```python
# Get schedules by lecturer
dr_bambang_schedules = service.get_schedules_by_lecturer("Dr. Bambang")

# Get schedules by room
room_schedules = service.get_schedules_by_room("R001")

# Get schedules by day
monday_schedules = service.get_schedules_by_day(DayOfWeek.MONDAY)

# Get conflicts for specific schedule
schedule_conflicts = service.get_conflicts_for_schedule("SCH001")
```

### Conflict Resolution with Suggestions

```python
from schedule_system import SchedulingSuggestionEngine

suggestion_engine = SchedulingSuggestionEngine(service)

# Define available slots
available_slots = [
    (DayOfWeek.TUESDAY, TimeSlot(time(8, 0), time(10, 0)), room),
    (DayOfWeek.WEDNESDAY, TimeSlot(time(10, 0), time(12, 0)), room),
    (DayOfWeek.THURSDAY, TimeSlot(time(14, 0), time(16, 0)), room),
]

# Get alternative suggestions
schedule_to_move = service.get_schedule("SCH001")
suggestions = suggestion_engine.suggest_alternatives(
    schedule_to_move, 
    available_slots,
    num_suggestions=3
)

# Print suggestions
for i, suggestion in enumerate(suggestions, 1):
    print(f"Option {i}:")
    print(f"  Day: {suggestion['day']}")
    print(f"  Time: {suggestion['time_slot']}")
    print(f"  Room: {suggestion['room']}")
    print(f"  Disruption: {suggestion['disruption_score']}/10")
```

### Dashboard & Reporting

```python
from schedule_system import DashboardService

dashboard = DashboardService(service)

# Get summary
summary = dashboard.get_dashboard_summary()
print(f"Total Schedules: {summary['total_schedules']}")
print(f"Total Conflicts: {summary['total_conflicts']}")

# Print schedules
dashboard.print_schedule_table()

# Print room schedule
dashboard.print_room_schedule("R001")

# Export conflict report
dashboard.export_conflict_report_json("conflict_report.json")

# Print conflicts
dashboard.print_conflicts()
```

---

## 📝 Contoh Kode

### Example 1: Menciptakan Schedule Tanpa Konflik

```python
service = SchedulingService()

# Add rooms
room_a = Room("R001", "Ruang A101", 40)
room_b = Room("R002", "Ruang B201", 50)
service.add_room(room_a)
service.add_room(room_b)

# Create non-conflicting schedules
schedule1 = Schedule(
    "SCH001", "Kalkulus I", "MTH101", "Dr. Smith",
    DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
    room_a, 35
)

schedule2 = Schedule(
    "SCH002", "Fisika Dasar", "PHY101", "Prof. Jones",
    DayOfWeek.TUESDAY, TimeSlot(time(10, 0), time(12, 0)),
    room_b, 40
)

service.create_schedule(schedule1)
service.create_schedule(schedule2)

print(f"Schedules created: {len(service.list_schedules())}")
print(f"Conflicts: {len(service.get_conflicts())}")  # Output: 0
```

### Example 2: Mendeteksi Bentrok Ruangan

```python
# Jadwal 1: Senin 08:00-10:00 di Ruang A101
schedule1 = Schedule(
    "SCH001", "Kalkulus I", "MTH101", "Dr. Smith",
    DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
    room_a, 35
)

# Jadwal 2: Senin 09:00-11:00 di Ruang A101 (BENTROK RUANGAN!)
schedule2 = Schedule(
    "SCH002", "Aljabar Linear", "MTH102", "Prof. Jones",
    DayOfWeek.MONDAY, TimeSlot(time(9, 0), time(11, 0)),
    room_a, 30  # Same room as schedule1
)

service.create_schedule(schedule1)
service.create_schedule(schedule2)

conflicts = service.get_conflicts()
# Output: 1 room conflict detected
```

### Example 3: Mendeteksi Bentrok Dosen

```python
# Jadwal 1: Senin 08:00-10:00, Dr. Smith mengajar Kalkulus
schedule1 = Schedule(
    "SCH001", "Kalkulus I", "MTH101", "Dr. Smith",
    DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
    room_a, 35
)

# Jadwal 2: Senin 09:00-11:00, Dr. Smith mengajar Aljabar (BENTROK DOSEN!)
schedule2 = Schedule(
    "SCH002", "Aljabar Linear", "MTH102", "Dr. Smith",
    DayOfWeek.MONDAY, TimeSlot(time(9, 0), time(11, 0)),
    room_b, 30  # Different room, but same lecturer
)

service.create_schedule(schedule1)
service.create_schedule(schedule2)

conflicts = service.get_conflicts()
# Output: 1 lecturer conflict detected
```

### Example 4: Notifikasi Observer

```python
# Setup observers
student = StudentObserver("STU001", "Andi", "andi@email.com")
lecturer = LecturerObserver("LEC001", "Dr. Smith", "smith@email.com")
admin = AdminObserver("ADMIN001", "Hendra", "hendra@email.com")

service.attach(student)
service.attach(lecturer)
service.attach(admin)

# Create schedule - akan trigger notifikasi ke semua observers
schedule = Schedule(
    "SCH001", "Kalkulus I", "MTH101", "Dr. Smith",
    DayOfWeek.MONDAY, TimeSlot(time(8, 0), time(10, 0)),
    room_a, 35
)

service.create_schedule(schedule)

# Output:
# 📧 STUDENT NOTIFICATION (Andi): New schedule created: Kalkulus I
# 👨‍🏫 LECTURER NOTIFICATION (Dr. Smith): You have a new class: Kalkulus I
# 👨‍💼 ADMIN NOTIFICATION (Hendra): New schedule created: Kalkulus I
```

### Example 5: Resolusi Konflik dengan Saran Jadwal

```python
suggestion_engine = SchedulingSuggestionEngine(service)

# Get conflicted schedule
conflicted = service.get_schedule("SCH001")

# Available alternative slots
available = [
    (DayOfWeek.TUESDAY, TimeSlot(time(8, 0), time(10, 0)), room_a),
    (DayOfWeek.WEDNESDAY, TimeSlot(time(8, 0), time(10, 0)), room_b),
    (DayOfWeek.THURSDAY, TimeSlot(time(14, 0), time(16, 0)), room_a),
]

# Get suggestions
suggestions = suggestion_engine.suggest_alternatives(conflicted, available, 2)

for i, sug in enumerate(suggestions, 1):
    print(f"Option {i}: {sug['day']} {sug['time_slot']}")
    print(f"  Room: {sug['room']}")
    print(f"  Disruption: {sug['disruption_score']}/10")
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python test_schedule_system.py

# Run specific test class
python -m unittest test_schedule_system.TestConflictDetection

# Run with verbose output
python test_schedule_system.py -v
```

### Test Coverage

**Total Tests**: 30+

#### Unit Tests
- ✅ TimeSlot tests (overlap detection)
- ✅ Room tests (capacity management)
- ✅ Conflict Detection tests
  - Room conflicts
  - Lecturer conflicts
  - Capacity exceeded
  - Case-insensitive lecturer names
- ✅ SchedulingService tests
  - CRUD operations
  - Query operations
  - Room management
- ✅ Observer Pattern tests
  - Attach/detach observers
  - Notification
- ✅ Suggestion Engine tests

#### Integration Tests
- ✅ Full workflow test

---

## ✅ Hasil Implementasi

### 1. Scheduling Service (35%)
- ✅ Create/Update/Delete jadwal
- ✅ Algoritma deteksi bentrok 3 dimensi
- ✅ Capacity check

### 2. Observer Implementation (25%)
- ✅ NotificationManager
- ✅ Multiple subscriber types
- ✅ Event logging system

### 3. Conflict Resolver UI (20%)
- ✅ Dashboard untuk melihat bentrok
- ✅ AI-powered suggestion alternatives
- ✅ Ranking by disruption score

### 4. Integration dengan KRS (15%)
- ✅ KRS invalidation saat jadwal berubah
- ✅ Tracking schedule dengan KRS ID

### 5. Testing + Documentation (5%)
- ✅ 30+ unit tests
- ✅ Comprehensive documentation
- ✅ Code examples

---

## 📊 Performance Analysis

### Time Complexity
- **Create Schedule**: O(n) - untuk conflict detection
- **Detect Conflicts**: O(n²) - perbandingan setiap pair jadwal
- **Query by Lecturer**: O(n)
- **Query by Room**: O(n)
- **Query by Day**: O(n)

### Space Complexity
- **Overall**: O(n) - menyimpan n schedules
- **Conflict Detection**: O(c) dimana c adalah jumlah conflicts

### Optimization Opportunities
1. Gunakan interval trees untuk time overlap detection
2. Index lecturer names dan room IDs
3. Implement caching untuk queries yang sering digunakan

---

## 🚀 Cara Menjalankan

### 1. Menjalankan Demo

```bash
python demo.py
```

Program akan menunjukkan semua fitur secara interaktif:
- CRUD operations
- Conflict detection
- Observer pattern
- Suggestions
- Dashboard

### 2. Menjalankan Tests

```bash
python test_schedule_system.py
```

### 3. File yang Dihasilkan

- `conflict_report.json`: Laporan konfllik dalam format JSON

---

## 📚 Referensi Design Patterns

### Observer Pattern
- **Tujuan**: Notify multiple observers saat state berubah
- **Implementation**: ScheduleSubject (Observable), StudentObserver, LecturerObserver, AdminObserver
- **Benefits**: Loose coupling, easy to add new observers

### Conflict Detection Algorithm
- **Approach**: Brute force comparison (dapat dioptimasi dengan interval trees)
- **Dimensi**: 3D (waktu, ruangan, dosen)

---

## 📞 Support

Untuk pertanyaan atau masalah, silakan buat issue atau hubungi tim development.

---

**Last Updated**: January 2026
**Version**: 1.0
**Author**: AI Developer
