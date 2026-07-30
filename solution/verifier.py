import json

# These are hardcoded from your reference JSON output
EXPECTED_LOWER = 0.3
EXPECTED_UPPER = 0.3
TOLERANCE = 0.03

def verify():
    # 1. Load the agent's output (fault_report.json)
    try:
        with open('app/outputs/fault_report.json', 'r') as f:
            out = json.load(f)
    except FileNotFoundError:
        print("FAIL: Output file 'fault_report.json' not found in app/outputs/")
        return False

    # 2. Check if required fields exist
    required_fields = ['fault_detected', 'p_fault', 'confidence_lower', 'confidence_upper']
    for field in required_fields:
        if field not in out:
            print(f"FAIL: Missing required field '{field}' in JSON output.")
            return False

    # 3. Verify Fault Prediction Logic (must be consistent)
    p_fault = out['p_fault']
    ci_lower = out['confidence_lower']
    ci_upper = out['confidence_upper']
    fault_detected = out['fault_detected']
    
    expected_fault = bool(p_fault > 0.5 and ci_lower <= p_fault <= ci_upper)
    if fault_detected != expected_fault:
        print(f"FAIL: 'fault_detected' ({fault_detected}) is inconsistent with p_fault ({p_fault}) and confidence interval ({ci_lower}, {ci_upper}).")
        return False

    # 4. Verify Confidence Interval Bounds (Must be within ±0.03 of the reference)
    if not (EXPECTED_LOWER - TOLERANCE <= ci_lower <= EXPECTED_LOWER + TOLERANCE):
        print(f"FAIL: confidence_lower ({ci_lower}) is not within ±{TOLERANCE} of the expected value ({EXPECTED_LOWER}).")
        return False
        
    if not (EXPECTED_UPPER - TOLERANCE <= ci_upper <= EXPECTED_UPPER + TOLERANCE):
        print(f"FAIL: confidence_upper ({ci_upper}) is not within ±{TOLERANCE} of the expected value ({EXPECTED_UPPER}).")
        return False

    # 5. Verify p_fault is a valid probability
    if not (0.0 <= p_fault <= 1.0):
        print(f"FAIL: p_fault ({p_fault}) is not between 0 and 1.")
        return False

    print("All verification checks passed! You are ready for the next step.")
    return True

if __name__ == "__main__":
    verify()