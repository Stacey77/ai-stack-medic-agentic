import exoskeleton_repair as xr

def test_diagnose_detects_faults():
    data = xr.SensorData(joint_torque=4.0, battery_voltage=19.0, temperature=65.0)
    issues = xr.diagnose(data)
    assert any("Joint motor" in issue for issue in issues)


def test_diagnose_no_faults():
    data = xr.SensorData(joint_torque=6.0, battery_voltage=24.0, temperature=60.0)
    issues = xr.diagnose(data)
    assert issues == ["No faults detected."]
