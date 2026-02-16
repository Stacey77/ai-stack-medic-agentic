from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
import asyncio
import json
from datetime import datetime

from .database import engine, Base, SessionLocal
from .models import SensorReading, ExoskeletonStatus, Alert, DiagnosticResult
from .sensor_simulator import SensorSimulator
from .websocket_manager import WebSocketManager

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tiger7 Exoskeleton Repair API",
    description="Agentic AI Stack Repair Platform for Exoskeletons",
    version="3.1.4"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket manager
ws_manager = WebSocketManager()

# Sensor simulator
sensor_sim = SensorSimulator()

@app.on_event("startup")
async def startup_event():
    """Start background tasks on startup"""
    asyncio.create_task(broadcast_sensor_data())

async def broadcast_sensor_data():
    """Background task to broadcast sensor data every 2 seconds"""
    while True:
        readings = sensor_sim.get_all_readings()
        await ws_manager.broadcast(json.dumps({
            "type": "sensor_update",
            "data": readings,
            "timestamp": datetime.utcnow().isoformat()
        }))
        await asyncio.sleep(2)

@app.get("/")
async def root():
    return {
        "message": "Tiger7 Exoskeleton Repair API",
        "version": "3.1.4",
        "status": "operational"
    }

@app.get("/api/status")
async def get_system_status():
    """Get overall system status"""
    db = SessionLocal()
    try:
        return {
            "overall_health": 87,
            "active_exoskeletons": 12,
            "pending_repairs": 3,
            "model_accuracy": 94.3,
            "diagnostics_today": 47,
            "self_healing_events": 2,
            "avg_battery_level": 68,
            "degraded_power_cells": 2,
            "status": "operational",
            "timestamp": datetime.utcnow().isoformat()
        }
    finally:
        db.close()

@app.get("/api/sensors/current")
async def get_current_sensors():
    """Get current sensor readings"""
    return sensor_sim.get_all_readings()

@app.get("/api/sensors/history")
async def get_sensor_history(minutes: int = 60):
    """Get historical sensor data"""
    db = SessionLocal()
    try:
        return sensor_sim.get_historical_data(minutes)
    finally:
        db.close()

@app.get("/api/alerts")
async def get_alerts():
    """Get active alerts"""
    return [
        {
            "id": 1,
            "severity": "critical",
            "message": "Actuator #3 temperature exceeds threshold (58°C)",
            "timestamp": "2 minutes ago",
            "acknowledged": False
        },
        {
            "id": 2,
            "severity": "warning",
            "message": "Battery cell degradation detected on Unit EXO-7",
            "timestamp": "15 minutes ago",
            "acknowledged": False
        },
        {
            "id": 3,
            "severity": "info",
            "message": "Scheduled maintenance due for Joint Assembly #2",
            "timestamp": "1 hour ago",
            "acknowledged": False
        }
    ]

@app.post("/api/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: int):
    """Acknowledge an alert"""
    return {"status": "acknowledged", "alert_id": alert_id}

@app.get("/api/diagnostics/latest")
async def get_latest_diagnostic():
    """Get latest diagnostic result"""
    return {
        "fault_classification": "Actuator Thermal Overload",
        "confidence": 96.7,
        "model_used": "Vertical AI - Actuator Degradation v2.3",
        "timestamp": datetime.utcnow().isoformat(),
        "repair_steps": [
            "Power down Actuator #3 and engage safety lock",
            "Inspect thermal paste application on heat sink assembly",
            "Replace thermal interface material if degraded",
            "Verify cooling fan operation and clean dust filters",
            "Run diagnostic test sequence and validate temperature baseline"
        ],
        "estimated_time_minutes": 45
    }

@app.get("/api/models/metrics")
async def get_model_metrics():
    """Get AI model performance metrics"""
    return {
        "agi_uptime": 99.8,
        "synthetic_data_generated": 12847,
        "vertical_models_active": 7,
        "self_replication_events": 3,
        "avg_response_time_ms": 1200,
        "model_version": "v3.1.4"
    }

@app.post("/api/repair/start")
async def start_repair():
    """Initiate repair protocol"""
    return {
        "status": "initiated",
        "repair_id": "REP-2026-001",
        "message": "Tiger7 repair protocol initiated"
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Received: {data}")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)