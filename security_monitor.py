#!/usr/bin/env python3
"""
Security Monitoring Dashboard
Real-time security monitoring and threat detection dashboard.
"""

from flask import Flask, render_template_string, jsonify, request
import random
from datetime import datetime, timedelta
import json

app = Flask(__name__)

class SecurityMonitor:
    def __init__(self):
        self.generate_sample_data()
    
    def generate_sample_data(self):
        # Generate sample security events
        self.security_events = []
        event_types = [
            {'type': 'Failed Login', 'severity': 'Medium', 'source': 'Authentication'},
            {'type': 'Malware Detected', 'severity': 'High', 'source': 'Antivirus'},
            {'type': 'Suspicious Network Activity', 'severity': 'High', 'source': 'Network Monitor'},
            {'type': 'Unauthorized Access Attempt', 'severity': 'Critical', 'source': 'Access Control'},
            {'type': 'Port Scan Detected', 'severity': 'Medium', 'source': 'Firewall'},
            {'type': 'Data Exfiltration Alert', 'severity': 'Critical', 'source': 'DLP'},
            {'type': 'Phishing Email Blocked', 'severity': 'Low', 'source': 'Email Security'},
            {'type': 'Vulnerability Scan Alert', 'severity': 'Medium', 'source': 'Vulnerability Scanner'}
        ]
        
        for i in range(50):
            event = random.choice(event_types)
            timestamp = datetime.now() - timedelta(hours=random.randint(0, 72))
            
            self.security_events.append({
                'id': i + 1,
                'timestamp': timestamp.isoformat(),
                'type': event['type'],
                'severity': event['severity'],
                'source': event['source'],
                'ip_address': f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                'status': random.choice(['Active', 'Resolved', 'Investigating']),
                'description': f"{event['type']} detected from {event['source']}"
            })
        
        # Sort by timestamp (newest first)
        self.security_events.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Generate system metrics
        self.system_metrics = {
            'cpu_usage': random.randint(15, 85),
            'memory_usage': random.randint(40, 90),
            'disk_usage': random.randint(30, 80),
            'network_traffic': random.randint(100, 1000),
            'active_connections': random.randint(50, 200),
            'blocked_threats': random.randint(10, 50)
        }
        
        # Generate threat intelligence
        self.threat_intel = [
            {'indicator': '192.168.100.50', 'type': 'IP Address', 'threat_level': 'High', 'last_seen': '2024-01-15'},
            {'indicator': 'malware.exe', 'type': 'File Hash', 'threat_level': 'Critical', 'last_seen': '2024-01-14'},
            {'indicator': 'evil.com', 'type': 'Domain', 'threat_level': 'Medium', 'last_seen': '2024-01-13'},
            {'indicator': '10.0.0.100', 'type': 'IP Address', 'threat_level': 'Low', 'last_seen': '2024-01-12'}
        ]
    
    def get_dashboard_stats(self):
        total_events = len(self.security_events)
        critical_events = len([e for e in self.security_events if e['severity'] == 'Critical'])
        high_events = len([e for e in self.security_events if e['severity'] == 'High'])
        active_threats = len([e for e in self.security_events if e['status'] == 'Active'])
        
        return {
            'total_events': total_events,
            'critical_events': critical_events,
            'high_events': high_events,
            'active_threats': active_threats,
            'system_metrics': self.system_metrics
        }
    
    def get_recent_events(self, limit=10):
        return self.security_events[:limit]
    
    def get_events_by_severity(self):
        severity_counts = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
        for event in self.security_events:
            severity_counts[event['severity']] += 1
        return severity_counts

monitor = SecurityMonitor()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Monitoring Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f1419; color: #ffffff; min-height: 100vh; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #1a1f2e 0%, #16213e 100%); border-radius: 15px; padding: 30px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); text-align: center; border: 1px solid #2d3748; }
        .dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .metric-card { background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%); border-radius: 15px; padding: 25px; text-align: center; border: 1px solid #4a5568; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        .metric-value { font-size: 2.5rem; font-weight: bold; margin-bottom: 10px; }
        .metric-label { font-size: 1rem; opacity: 0.8; }
        .critical { color: #fc8181; }
        .high { color: #f6ad55; }
        .medium { color: #68d391; }
        .low { color: #63b3ed; }
        .card { background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%); border-radius: 15px; padding: 25px; margin-bottom: 20px; border: 1px solid #4a5568; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        .btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: 600; margin: 5px; }
        .btn:hover { opacity: 0.9; }
        .data-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        .data-table th, .data-table td { padding: 12px; text-align: left; border-bottom: 1px solid #4a5568; }
        .data-table th { background: #2d3748; font-weight: 600; }
        .data-table tr:hover { background: #2d3748; }
        .status-active { color: #fc8181; font-weight: bold; }
        .status-resolved { color: #68d391; font-weight: bold; }
        .status-investigating { color: #f6ad55; font-weight: bold; }
        .severity-critical { background: #fc8181; color: #1a202c; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .severity-high { background: #f6ad55; color: #1a202c; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .severity-medium { background: #68d391; color: #1a202c; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .severity-low { background: #63b3ed; color: #1a202c; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .system-metric { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .progress-bar { background: #4a5568; border-radius: 10px; height: 8px; flex-grow: 1; margin-left: 15px; overflow: hidden; }
        .progress-fill { height: 100%; border-radius: 10px; transition: width 0.3s ease; }
        .progress-normal { background: linear-gradient(135deg, #68d391, #38a169); }
        .progress-warning { background: linear-gradient(135deg, #f6ad55, #ed8936); }
        .progress-danger { background: linear-gradient(135deg, #fc8181, #e53e3e); }
        .threat-item { padding: 15px; border-left: 4px solid #667eea; margin-bottom: 15px; background: #2d3748; border-radius: 0 8px 8px 0; }
        .auto-refresh { position: fixed; top: 20px; right: 20px; background: #2d3748; padding: 10px; border-radius: 8px; border: 1px solid #4a5568; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Security Monitoring Dashboard</h1>
            <p>Real-time security monitoring and threat detection</p>
        </div>
        
        <div class="auto-refresh">
            <label>
                <input type="checkbox" id="autoRefresh" checked> Auto-refresh (30s)
            </label>
        </div>
        
        <div class="dashboard-grid" id="metricsGrid">
            <!-- Metrics will be populated here -->
        </div>
        
        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 30px;">
            <div class="card">
                <h3>🚨 Recent Security Events</h3>
                <button onclick="loadEvents()" class="btn">🔄 Refresh Events</button>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Event Type</th>
                            <th>Severity</th>
                            <th>Source</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody id="eventsBody">
                        <!-- Events will be populated here -->
                    </tbody>
                </table>
            </div>
            
            <div class="card">
                <h3>📊 System Metrics</h3>
                <div id="systemMetrics">
                    <!-- System metrics will be populated here -->
                </div>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div class="card">
                <h3>📈 Event Distribution</h3>
                <div id="eventDistribution">
                    <!-- Event distribution will be populated here -->
                </div>
            </div>
            
            <div class="card">
                <h3>🎯 Threat Intelligence</h3>
                <div id="threatIntel">
                    <!-- Threat intelligence will be populated here -->
                </div>
            </div>
        </div>
    </div>

    <script>
        let refreshInterval;
        
        async function loadDashboard() {
            try {
                const response = await fetch('/api/dashboard');
                const data = await response.json();
                
                document.getElementById('metricsGrid').innerHTML = `
                    <div class="metric-card">
                        <div class="metric-value">${data.total_events}</div>
                        <div class="metric-label">Total Events</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value critical">${data.critical_events}</div>
                        <div class="metric-label">Critical Events</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value high">${data.high_events}</div>
                        <div class="metric-label">High Priority</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value medium">${data.active_threats}</div>
                        <div class="metric-label">Active Threats</div>
                    </div>
                `;
                
                // Load system metrics
                const metrics = data.system_metrics;
                document.getElementById('systemMetrics').innerHTML = `
                    <div class="system-metric">
                        <span>CPU Usage</span>
                        <div class="progress-bar">
                            <div class="progress-fill ${getProgressClass(metrics.cpu_usage)}" style="width: ${metrics.cpu_usage}%"></div>
                        </div>
                        <span>${metrics.cpu_usage}%</span>
                    </div>
                    <div class="system-metric">
                        <span>Memory</span>
                        <div class="progress-bar">
                            <div class="progress-fill ${getProgressClass(metrics.memory_usage)}" style="width: ${metrics.memory_usage}%"></div>
                        </div>
                        <span>${metrics.memory_usage}%</span>
                    </div>
                    <div class="system-metric">
                        <span>Disk Usage</span>
                        <div class="progress-bar">
                            <div class="progress-fill ${getProgressClass(metrics.disk_usage)}" style="width: ${metrics.disk_usage}%"></div>
                        </div>
                        <span>${metrics.disk_usage}%</span>
                    </div>
                    <div class="system-metric">
                        <span>Network Traffic</span>
                        <span>${metrics.network_traffic} MB/s</span>
                    </div>
                    <div class="system-metric">
                        <span>Active Connections</span>
                        <span>${metrics.active_connections}</span>
                    </div>
                    <div class="system-metric">
                        <span>Blocked Threats</span>
                        <span>${metrics.blocked_threats}</span>
                    </div>
                `;
                
            } catch (error) {
                console.error('Error loading dashboard:', error);
            }
        }
        
        async function loadEvents() {
            try {
                const response = await fetch('/api/events');
                const events = await response.json();
                
                document.getElementById('eventsBody').innerHTML = events.map(event => `
                    <tr>
                        <td>${new Date(event.timestamp).toLocaleString()}</td>
                        <td>${event.type}</td>
                        <td><span class="severity-${event.severity.toLowerCase()}">${event.severity}</span></td>
                        <td>${event.source}</td>
                        <td class="status-${event.status.toLowerCase()}">${event.status}</td>
                    </tr>
                `).join('');
            } catch (error) {
                console.error('Error loading events:', error);
            }
        }
        
        async function loadEventDistribution() {
            try {
                const response = await fetch('/api/events/distribution');
                const distribution = await response.json();
                
                document.getElementById('eventDistribution').innerHTML = Object.entries(distribution).map(([severity, count]) => `
                    <div class="system-metric">
                        <span class="${severity.toLowerCase()}">${severity}</span>
                        <span>${count} events</span>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Error loading event distribution:', error);
            }
        }
        
        async function loadThreatIntel() {
            try {
                const response = await fetch('/api/threat-intel');
                const threats = await response.json();
                
                document.getElementById('threatIntel').innerHTML = threats.map(threat => `
                    <div class="threat-item">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <strong>${threat.indicator}</strong>
                            <span class="severity-${threat.threat_level.toLowerCase()}">${threat.threat_level}</span>
                        </div>
                        <div style="font-size: 14px; opacity: 0.8;">
                            Type: ${threat.type} | Last seen: ${threat.last_seen}
                        </div>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Error loading threat intel:', error);
            }
        }
        
        function getProgressClass(value) {
            if (value >= 80) return 'progress-danger';
            if (value >= 60) return 'progress-warning';
            return 'progress-normal';
        }
        
        function setupAutoRefresh() {
            const checkbox = document.getElementById('autoRefresh');
            
            if (checkbox.checked) {
                refreshInterval = setInterval(() => {
                    loadDashboard();
                    loadEvents();
                    loadEventDistribution();
                    loadThreatIntel();
                }, 30000);
            } else {
                clearInterval(refreshInterval);
            }
        }
        
        // Load data on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadDashboard();
            loadEvents();
            loadEventDistribution();
            loadThreatIntel();
            
            // Setup auto-refresh
            document.getElementById('autoRefresh').addEventListener('change', setupAutoRefresh);
            setupAutoRefresh();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/dashboard')
def get_dashboard():
    return jsonify(monitor.get_dashboard_stats())

@app.route('/api/events')
def get_events():
    return jsonify(monitor.get_recent_events())

@app.route('/api/events/distribution')
def get_event_distribution():
    return jsonify(monitor.get_events_by_severity())

@app.route('/api/threat-intel')
def get_threat_intel():
    return jsonify(monitor.threat_intel)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

