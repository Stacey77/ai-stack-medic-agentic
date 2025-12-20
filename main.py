"""Example command-line interface for the repair platform."""

from exoskeleton_repair import RepairAgent, SensorData

def main() -> None:
    # Example sensor data; in a real system, this would come from hardware.
    data = SensorData(joint_torque=4.5, battery_voltage=19.0, temperature=65.0)
    agent = RepairAgent()
    steps = agent.analyze(data)
    print("Detected issues and recommended steps:")
    for step in steps:
        print(f"- {step}")

if __name__ == "__main__":
    main()
