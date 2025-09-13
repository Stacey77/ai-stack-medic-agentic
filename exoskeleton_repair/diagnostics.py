"""Simple diagnostic algorithms for exoskeletons."""

from dataclasses import dataclass
from typing import Dict, List

@dataclass
class SensorData:
    """Represents telemetry from exoskeleton sensors."""
    joint_torque: float
    battery_voltage: float
    temperature: float

FAULT_THRESHOLDS: Dict[str, float] = {
    "joint_torque": 5.0,    # Nm
    "battery_voltage": 20.0, # Volts
    "temperature": 70.0,    # Celsius
}

FAULT_MESSAGES: Dict[str, str] = {
    "joint_torque": "Joint motor torque too low. Check mechanical linkage.",
    "battery_voltage": "Battery voltage below safe operating threshold.",
    "temperature": "System temperature too high. Inspect cooling system.",
}

def diagnose(data: SensorData) -> List[str]:
    """Analyzes sensor data and returns a list of detected issues."""
    issues: List[str] = []
    if data.joint_torque < FAULT_THRESHOLDS["joint_torque"]:
        issues.append(FAULT_MESSAGES["joint_torque"])
    if data.battery_voltage < FAULT_THRESHOLDS["battery_voltage"]:
        issues.append(FAULT_MESSAGES["battery_voltage"])
    if data.temperature > FAULT_THRESHOLDS["temperature"]:
        issues.append(FAULT_MESSAGES["temperature"])
    if not issues:
        issues.append("No faults detected.")
    return issues
