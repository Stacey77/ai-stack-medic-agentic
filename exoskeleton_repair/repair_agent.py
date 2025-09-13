"""Agent that recommends repair steps based on diagnostics."""

from dataclasses import dataclass
from typing import List

from .diagnostics import SensorData, diagnose

@dataclass
class RepairAgent:
    """Uses diagnostic results to generate repair instructions."""

    def analyze(self, data: SensorData) -> List[str]:
        issues = diagnose(data)
        steps: List[str] = []
        for issue in issues:
            if issue == "No faults detected.":
                steps.append("System is operating normally.")
            elif "torque" in issue:
                steps.append("Tighten joint bolts and inspect motor connections.")
            elif "voltage" in issue:
                steps.append("Replace or recharge the battery pack.")
            elif "temperature" in issue:
                steps.append("Check cooling vents and fans for obstructions.")
            else:
                steps.append("Further investigation required.")
        return steps
