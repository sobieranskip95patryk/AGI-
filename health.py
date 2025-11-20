"""
Health endpoint for MIGI_7G system monitoring
Provides system status, readiness checks, and basic metrics
"""

from flask import Flask, jsonify, request
import time
import os
import json
import psutil


app = Flask(__name__)
START_TIME = time.time()

@app.route("/health")
def health():
    """Main health check endpoint"""
    uptime = time.time() - START_TIME
    
    # Basic system metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('.')
    
    status = {
        "status": "healthy",
        "timestamp": time.time(),
        "uptime_seconds": int(uptime),
        "version": "1.0.0",
        "system": {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "disk_free_gb": round(disk.free / (1024**3), 2)
        }
    }
    
    # Check for critical issues
    if cpu_percent > 90:
        status["warnings"] = status.get("warnings", [])
        status["warnings"].append("High CPU usage")
    
    if memory.percent > 90:
        status["warnings"] = status.get("warnings", [])
        status["warnings"].append("High memory usage")
    
    return jsonify(status), 200

@app.route("/readiness")
def readiness():
    """Readiness check for container orchestration"""
    try:
        # Check if core modules can be imported
        from core.migi7g_core_directives import directive_engine
        from FUNCTION_CALLING.migi_integration import migi_function_calling
        
        # Test basic functionality
        health = directive_engine.get_system_health()
        tools_count = len(migi_function_calling.get_available_tools())
        
        return jsonify({
            "ready": True,
            "core_directives": health["system_status"],
            "function_calling_tools": tools_count,
            "timestamp": time.time()
        }), 200
        
    except Exception as e:
        return jsonify({
            "ready": False,
            "error": str(e),
            "timestamp": time.time()
        }), 503

@app.route("/metrics")
def metrics():
    """Prometheus-style metrics endpoint"""
    uptime = time.time() - START_TIME
    
    try:
        from core.migi7g_core_directives import directive_engine
        health = directive_engine.get_system_health()
        
        metrics_text = f"""# HELP migi7g_uptime_seconds System uptime in seconds
# TYPE migi7g_uptime_seconds counter
migi7g_uptime_seconds {int(uptime)}

# HELP migi7g_health_score System health score
# TYPE migi7g_health_score gauge
migi7g_health_score {health.get('health_score', 0)}

# HELP migi7g_active_goals Number of active goals
# TYPE migi7g_active_goals gauge
migi7g_active_goals {health.get('active_goals', 0)}

# HELP migi7g_kpis_passed Number of KPIs currently passing
# TYPE migi7g_kpis_passed gauge
migi7g_kpis_passed {health.get('passed_kpis', 0)}

# HELP migi7g_kpis_total Total number of KPIs
# TYPE migi7g_kpis_total gauge
migi7g_kpis_total {health.get('total_kpis', 0)}
"""
        
        return metrics_text, 200, {'Content-Type': 'text/plain; charset=utf-8'}
        
    except Exception as e:
        return f"# Error generating metrics: {str(e)}", 500, {'Content-Type': 'text/plain'}

@app.route("/snapshot/current")
def snapshot_current():
    """Get current system snapshot"""
    try:
        # Look for latest snapshot
        snapshot_dir = "snapshots"
        if os.path.exists(snapshot_dir):
            snapshots = [f for f in os.listdir(snapshot_dir) if f.endswith('.json')]
            if snapshots:
                latest = max(snapshots, key=lambda x: os.path.getctime(os.path.join(snapshot_dir, x)))
                
                with open(os.path.join(snapshot_dir, latest), 'r', encoding='utf-8') as f:
                    snapshot_data = json.load(f)
                
                return jsonify({
                    "snapshot": snapshot_data,
                    "filename": latest,
                    "timestamp": time.time()
                }), 200
        
        return jsonify({
            "error": "No snapshots available",
            "timestamp": time.time()
        }), 404
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "timestamp": time.time()
        }), 500

@app.route("/directives/status")
def directives_status():
    """Get current directives status"""
    try:
        from core.migi7g_core_directives import directive_engine, get_directive_summary
        
        summary = get_directive_summary()
        return jsonify(summary), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "timestamp": time.time()
        }), 500

@app.route("/tools/available")
def tools_available():
    """Get list of available function calling tools"""
    try:
        from FUNCTION_CALLING.migi_integration import migi_function_calling
        
        tools = migi_function_calling.get_available_tools()
        return jsonify({
            "tools": tools,
            "count": len(tools),
            "timestamp": time.time()
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "timestamp": time.time()
        }), 500

@app.route("/test/alignment", methods=['POST'])
def test_alignment():
    """Test action alignment with planetary directives"""
    try:
        data = request.get_json()
        if not data or 'action' not in data:
            return jsonify({"error": "Missing 'action' in request body"}), 400
        
        from core.migi7g_core_directives import evaluate_action_alignment
        
        result = evaluate_action_alignment(
            data['action'], 
            data.get('context', {})
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "timestamp": time.time()
        }), 500

@app.route("/system/info")
def system_info():
    """Comprehensive system information"""
    uptime = time.time() - START_TIME
    
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('.')
        
        # MIGI_7G specific info
        from core.migi7g_core_directives import directive_engine
        from FUNCTION_CALLING.migi_integration import migi_function_calling
        
        health = directive_engine.get_system_health()
        tools_count = len(migi_function_calling.get_available_tools())
        
        return jsonify({
            "system": {
                "uptime_seconds": int(uptime),
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_total_gb": round(memory.total / (1024**3), 2),
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "disk_total_gb": round(disk.total / (1024**3), 2),
                "disk_free_gb": round(disk.free / (1024**3), 2)
            },
            "migi7g": {
                "version": "1.0.0",
                "directives_health": health,
                "function_calling_tools": tools_count,
                "components": {
                    "core_directives": True,
                    "function_calling": True,
                    "eq_bench_integration": True,
                    "dashboard_kalibracyjny": True,
                    "telemetry_websocket": True
                }
            },
            "timestamp": time.time()
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "timestamp": time.time()
        }), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"🏥 MIGI_7G Health Server starting on port {port}")
    print("📊 Available endpoints:")
    print("  - GET  /health          - Basic health check")
    print("  - GET  /readiness       - Kubernetes readiness probe")
    print("  - GET  /metrics         - Prometheus metrics")
    print("  - GET  /snapshot/current - Current system snapshot")
    print("  - GET  /directives/status - Planetary directives status")
    print("  - GET  /tools/available - Function calling tools")
    print("  - POST /test/alignment  - Test action alignment")
    print("  - GET  /system/info     - Comprehensive system info")
    
    app.run(host="0.0.0.0", port=port, debug=debug)