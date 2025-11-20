"""
Health endpoint for MIGI_7G system monitoring
Provides system status, readiness checks, and basic metrics
"""

from flask import Flask, jsonify, request
import time
import os
import json
import psutil
from typing import Dict, Any

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
        health_info = directive_engine.get_system_health()
        tools_count = len(migi_function_calling.get_available_tools())
        
        return jsonify({
            "ready": True,
            "core_directives": health_info["system_status"],
            "function_calling_tools": tools_count,
            "timestamp": time.time()
        }), 200
        
    except Exception as e:
        return jsonify({
            "ready": False,
            "error": str(e),
            "timestamp": time.time()
        }), 503

@app.route("/system/info")
def system_info():
    """Comprehensive system information"""
    uptime = time.time() - START_TIME
    
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('.')
        
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
    print("  - GET  /system/info     - Comprehensive system info")
    app.run(host="0.0.0.0", port=port, debug=debug)