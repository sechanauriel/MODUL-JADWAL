"""
Schedule Management System - Web Dashboard
Interactive web interface for the REST API
"""

from flask import Flask, render_template_string, request, jsonify
from api_client import ScheduleAPIClient
import json

app = Flask(__name__)
client = ScheduleAPIClient()

# HTML/CSS/JavaScript untuk dashboard interaktif
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Schedule Management System - Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .status {
            display: inline-block;
            padding: 8px 15px;
            background: #4CAF50;
            color: white;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
        }
        
        .status.error {
            background: #f44336;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .tab-btn {
            padding: 12px 24px;
            background: white;
            border: 2px solid #667eea;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            color: #667eea;
            transition: all 0.3s;
        }
        
        .tab-btn:hover, .tab-btn.active {
            background: #667eea;
            color: white;
        }
        
        .tab-content {
            display: none;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .tab-content.active {
            display: block;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        
        input, select, textarea {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            padding: 12px 24px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.3s;
        }
        
        button:hover {
            background: #764ba2;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        @media (max-width: 768px) {
            .form-row {
                grid-template-columns: 1fr;
            }
        }
        
        .result {
            margin-top: 20px;
            padding: 15px;
            background: #f5f5f5;
            border-radius: 5px;
            border-left: 4px solid #667eea;
            display: none;
        }
        
        .result.show {
            display: block;
        }
        
        .result.success {
            border-left-color: #4CAF50;
            background: #f1f8f5;
        }
        
        .result.error {
            border-left-color: #f44336;
            background: #fdf5f5;
        }
        
        .result-content {
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            color: #333;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-card h3 {
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 10px;
        }
        
        .stat-card .number {
            font-size: 32px;
            font-weight: bold;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        th {
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
        }
        
        td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }
        
        tr:hover {
            background: #f5f5f5;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .loading.show {
            display: block;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }
        
        .badge.success {
            background: #4CAF50;
            color: white;
        }
        
        .badge.error {
            background: #f44336;
            color: white;
        }
        
        .badge.warning {
            background: #ff9800;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📅 Schedule Management System - Web Dashboard</h1>
            <p>Interactive interface untuk REST API</p>
            <span class="status" id="status">🟢 Connected</span>
        </header>
        
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('dashboard')">📊 Dashboard</button>
            <button class="tab-btn" onclick="switchTab('rooms')">🏢 Rooms</button>
            <button class="tab-btn" onclick="switchTab('schedules')">📅 Schedules</button>
            <button class="tab-btn" onclick="switchTab('conflicts')">🚨 Conflicts</button>
            <button class="tab-btn" onclick="switchTab('suggestions')">🤖 Suggestions</button>
        </div>
        
        <!-- DASHBOARD TAB -->
        <div id="dashboard" class="tab-content active">
            <h2>📊 Dashboard Overview</h2>
            
            <div class="stats" id="stats">
                <div class="stat-card">
                    <h3>Total Rooms</h3>
                    <div class="number" id="stat-rooms">-</div>
                </div>
                <div class="stat-card">
                    <h3>Total Schedules</h3>
                    <div class="number" id="stat-schedules">-</div>
                </div>
                <div class="stat-card">
                    <h3>Total Conflicts</h3>
                    <div class="number" id="stat-conflicts">-</div>
                </div>
                <div class="stat-card">
                    <h3>Conflict Rate</h3>
                    <div class="number" id="stat-rate">-</div>
                </div>
            </div>
            
            <button onclick="loadDashboard()" style="margin-top: 20px;">🔄 Refresh Dashboard</button>
            
            <div class="result" id="dashboard-result">
                <div class="result-content" id="dashboard-content"></div>
            </div>
        </div>
        
        <!-- ROOMS TAB -->
        <div id="rooms" class="tab-content">
            <h2>🏢 Room Management</h2>
            
            <div class="form-row">
                <div>
                    <h3>Create New Room</h3>
                    <div class="form-group">
                        <label>Room ID</label>
                        <input type="text" id="room-id" placeholder="R001">
                    </div>
                    <div class="form-group">
                        <label>Room Name</label>
                        <input type="text" id="room-name" placeholder="Ruang Kuliah A">
                    </div>
                    <div class="form-group">
                        <label>Capacity</label>
                        <input type="number" id="room-capacity" placeholder="40" min="1">
                    </div>
                    <div class="form-group">
                        <label>Building</label>
                        <input type="text" id="room-building" placeholder="Building A">
                    </div>
                    <button onclick="createRoom()">➕ Create Room</button>
                </div>
                
                <div>
                    <h3>All Rooms</h3>
                    <button onclick="listRooms()" style="margin-bottom: 15px;">📋 Refresh Rooms</button>
                    <div id="rooms-table"></div>
                </div>
            </div>
            
            <div class="result" id="rooms-result">
                <div class="result-content" id="rooms-content"></div>
            </div>
        </div>
        
        <!-- SCHEDULES TAB -->
        <div id="schedules" class="tab-content">
            <h2>📅 Schedule Management</h2>
            
            <div class="form-row">
                <div>
                    <h3>Create New Schedule</h3>
                    <div class="form-group">
                        <label>Schedule ID</label>
                        <input type="text" id="sched-id" placeholder="SCH001">
                    </div>
                    <div class="form-group">
                        <label>Course Name</label>
                        <input type="text" id="sched-course" placeholder="Introduction to Python">
                    </div>
                    <div class="form-group">
                        <label>Course Code</label>
                        <input type="text" id="sched-code" placeholder="CS101">
                    </div>
                    <div class="form-group">
                        <label>Lecturer Name</label>
                        <input type="text" id="sched-lecturer" placeholder="Dr. Smith">
                    </div>
                    <div class="form-group">
                        <label>Day</label>
                        <select id="sched-day">
                            <option>MONDAY</option>
                            <option>TUESDAY</option>
                            <option>WEDNESDAY</option>
                            <option>THURSDAY</option>
                            <option>FRIDAY</option>
                            <option>SATURDAY</option>
                            <option>SUNDAY</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Start Time (HH:MM)</label>
                        <input type="text" id="sched-start" placeholder="09:00">
                    </div>
                    <div class="form-group">
                        <label>End Time (HH:MM)</label>
                        <input type="text" id="sched-end" placeholder="11:00">
                    </div>
                    <div class="form-group">
                        <label>Room ID</label>
                        <input type="text" id="sched-room" placeholder="R001">
                    </div>
                    <div class="form-group">
                        <label>Number of Students</label>
                        <input type="number" id="sched-students" placeholder="30" min="1">
                    </div>
                    <button onclick="createSchedule()">➕ Create Schedule</button>
                </div>
                
                <div>
                    <h3>All Schedules</h3>
                    <button onclick="listSchedules()" style="margin-bottom: 15px;">📋 Refresh Schedules</button>
                    <div id="schedules-table"></div>
                </div>
            </div>
            
            <div class="result" id="schedules-result">
                <div class="result-content" id="schedules-content"></div>
            </div>
        </div>
        
        <!-- CONFLICTS TAB -->
        <div id="conflicts" class="tab-content">
            <h2>🚨 Conflict Detection</h2>
            
            <button onclick="getConflicts()" style="margin-bottom: 20px;">🔍 Check for Conflicts</button>
            
            <div id="conflicts-display"></div>
            
            <div class="result" id="conflicts-result">
                <div class="result-content" id="conflicts-content"></div>
            </div>
        </div>
        
        <!-- SUGGESTIONS TAB -->
        <div id="suggestions" class="tab-content">
            <h2>🤖 Schedule Suggestions</h2>
            
            <div class="form-group">
                <label>Schedule ID (for suggestions)</label>
                <input type="text" id="suggest-id" placeholder="SCH001">
            </div>
            
            <button onclick="getSuggestions()">💡 Get Suggestions</button>
            
            <div class="result" id="suggestions-result">
                <div class="result-content" id="suggestions-content"></div>
            </div>
        </div>
    </div>
    
    <script>
        // Tab switching
        function switchTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
        
        // API calls
        async function apiCall(method, endpoint, data = null) {
            try {
                const options = {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json'
                    }
                };
                
                if (data) {
                    options.body = JSON.stringify(data);
                }
                
                const response = await fetch(`http://localhost:5000/api${endpoint}`, options);
                return await response.json();
            } catch (error) {
                return { status: 'error', message: error.message };
            }
        }
        
        // Dashboard
        async function loadDashboard() {
            const result = await apiCall('GET', '/dashboard/summary');
            if (result.status === 'success') {
                const data = result.data;
                document.getElementById('stat-rooms').textContent = data.total_rooms;
                document.getElementById('stat-schedules').textContent = data.total_schedules;
                document.getElementById('stat-conflicts').textContent = data.total_conflicts;
                document.getElementById('stat-rate').textContent = data.conflict_rate;
                
                showResult('dashboard-result', JSON.stringify(data, null, 2), 'success');
            } else {
                showResult('dashboard-result', 'Error: ' + result.message, 'error');
            }
        }
        
        // Rooms
        async function createRoom() {
            const data = {
                room_id: document.getElementById('room-id').value,
                room_name: document.getElementById('room-name').value,
                capacity: parseInt(document.getElementById('room-capacity').value),
                building: document.getElementById('room-building').value
            };
            
            const result = await apiCall('POST', '/rooms', data);
            showResult('rooms-result', JSON.stringify(result, null, 2), result.status);
            listRooms();
        }
        
        async function listRooms() {
            const result = await apiCall('GET', '/rooms');
            if (result.status === 'success') {
                let html = '<table><tr><th>Room ID</th><th>Name</th><th>Capacity</th><th>Building</th></tr>';
                result.data.forEach(room => {
                    html += `<tr><td>${room.room_id}</td><td>${room.room_name}</td><td>${room.capacity}</td><td>${room.building}</td></tr>`;
                });
                html += '</table>';
                document.getElementById('rooms-table').innerHTML = html;
            }
        }
        
        // Schedules
        async function createSchedule() {
            const data = {
                schedule_id: document.getElementById('sched-id').value,
                course_name: document.getElementById('sched-course').value,
                course_code: document.getElementById('sched-code').value,
                lecturer_name: document.getElementById('sched-lecturer').value,
                day: document.getElementById('sched-day').value,
                start_time: document.getElementById('sched-start').value,
                end_time: document.getElementById('sched-end').value,
                room_id: document.getElementById('sched-room').value,
                num_students: parseInt(document.getElementById('sched-students').value)
            };
            
            const result = await apiCall('POST', '/schedules', data);
            showResult('schedules-result', JSON.stringify(result, null, 2), result.status);
            listSchedules();
        }
        
        async function listSchedules() {
            const result = await apiCall('GET', '/schedules');
            if (result.status === 'success') {
                let html = '<table><tr><th>Code</th><th>Course</th><th>Lecturer</th><th>Day</th><th>Time</th><th>Room</th><th>Students</th></tr>';
                result.data.forEach(sched => {
                    html += `<tr><td>${sched.course_code}</td><td>${sched.course_name}</td><td>${sched.lecturer_name}</td><td>${sched.day}</td><td>${sched.time_slot}</td><td>${sched.room_id}</td><td>${sched.num_students}</td></tr>`;
                });
                html += '</table>';
                document.getElementById('schedules-table').innerHTML = html;
            }
        }
        
        // Conflicts
        async function getConflicts() {
            const result = await apiCall('GET', '/conflicts');
            if (result.status === 'success') {
                if (result.data.length === 0) {
                    showResult('conflicts-result', '✅ No conflicts detected!', 'success');
                } else {
                    let html = '<table><tr><th>Type</th><th>Description</th><th>Severity</th></tr>';
                    result.data.forEach(conflict => {
                        html += `<tr><td><span class="badge warning">${conflict.conflict_type}</span></td><td>${conflict.description}</td><td>${conflict.severity}</td></tr>`;
                    });
                    html += '</table>';
                    document.getElementById('conflicts-display').innerHTML = html;
                    showResult('conflicts-result', JSON.stringify(result.data, null, 2), 'success');
                }
            } else {
                showResult('conflicts-result', 'Error: ' + result.message, 'error');
            }
        }
        
        // Suggestions
        async function getSuggestions() {
            const scheduleId = document.getElementById('suggest-id').value;
            const data = { schedule_id: scheduleId, num_suggestions: 3 };
            
            const result = await apiCall('POST', '/suggestions', data);
            showResult('suggestions-result', JSON.stringify(result, null, 2), result.status);
        }
        
        // Utility
        function showResult(elementId, content, type) {
            const element = document.getElementById(elementId);
            element.classList.add('show', type);
            element.classList.remove(type === 'success' ? 'error' : 'success');
            document.getElementById(elementId.replace('-result', '-content')).textContent = content;
        }
        
        // Initial load
        window.addEventListener('load', () => {
            loadDashboard();
            listRooms();
            listSchedules();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api-proxy/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_proxy(endpoint):
    """Proxy API requests to avoid CORS issues"""
    method = request.method
    data = request.get_json() if request.method in ['POST', 'PUT'] else None
    
    try:
        if method == 'GET':
            response = client.session.get(f"{client.base_url}/{endpoint}")
        elif method == 'POST':
            response = client.session.post(f"{client.base_url}/{endpoint}", json=data)
        elif method == 'PUT':
            response = client.session.put(f"{client.base_url}/{endpoint}", json=data)
        elif method == 'DELETE':
            response = client.session.delete(f"{client.base_url}/{endpoint}")
        
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*80)
    print("Schedule Management System - Web Dashboard")
    print("="*80)
    print("\n📊 Dashboard Server Starting...")
    print(f"🌐 Access Dashboard at: http://localhost:5001")
    print(f"📡 Connected to API: http://localhost:5000/api")
    print("\n" + "="*80 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True,
        use_reloader=False
    )
