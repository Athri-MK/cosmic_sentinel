"""
Root Orchestration Driver: app.py
Execution Mode: Low-Level, Deterministic, Line-by-Line Console Logging Engine
"""

import json
from typing import Dict, Any, List, Optional

# Cross-directory tracking operations import
from src.predictor import fetch_live_telemetry, process_neo_data


# -----------------------------------------------------------------------------
# MANAGEMENT PIPELINE
# -----------------------------------------------------------------------------
def run_dashboard_api_pipeline() -> None:
    """
    Coordinates the ingestion sequence, validates the data boundary, processes the 
    transformation matrix, and streams the formatted JSON payload to the console shell.
    """
    print("[ORCHESTRATOR] [INIT] Starting dashboard API pipeline execution.")

    # Trigger the telemetry ingestion sequence
    print("[ORCHESTRATOR] [INGEST_CALL] Invoking fetch_live_telemetry() across module boundary.")
    raw_telemetry: Optional[Dict[str, Any]] = fetch_live_telemetry()

    # Validation gate check
    if raw_telemetry is None:
        print("[ORCHESTRATOR] [GATE_FAILED] Raw payload is None. Aborting transformation pipeline.")
        fallback_payload: Dict[str, Any] = {
            "status": "FAILURE",
            "venue_node": "JNNCE_SHIVAMOGGA_INDIA",
            "total_monitored_objects": 0,
            "payload_data": []
        }
        print("[ORCHESTRATOR] [OUTPUT_STREAM] Streaming fallback diagnostic state:")
        print(json.dumps(fallback_payload, indent=2))
        return

    print("[ORCHESTRATOR] [GATE_PASSED] Raw payload verified. Passing stream to processing loop matrix.")
    
    # Process data matrix array
    dashboard_dataset: List[Dict[str, Any]] = process_neo_data(raw_telemetry)
    
    # Extract verification metrics
    total_objects: int = len(dashboard_dataset)
    print(f"[ORCHESTRATOR] [VERIFICATION] Total monitored objects successfully compiled: {total_objects}")

    # Web Dashboard Payload Formatting
    master_payload: Dict[str, Any] = {
        "status": "SUCCESS",
        "venue_node": "JNNCE_SHIVAMOGGA_INDIA",
        "total_monitored_objects": total_objects,
        "payload_data": dashboard_dataset
    }

    print("[ORCHESTRATOR] [FORMATTING] Serializing master payload dictionary to JSON string matrix.")
    
    # Console Verification Gate - Stream directly to system stdout
    json_output: str = json.dumps(master_payload, indent=2)
    print("\n[ORCHESTRATOR] [SYSTEM_OUT] ========================================")
    print(json_output)
    print("======================================================================\n")
    
    print("[ORCHESTRATOR] [COMPLETE] Pipeline execution node terminated cleanly.")


# -----------------------------------------------------------------------------
# CONSOLE VERIFICATION GATE
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("================================================================================")
    print("SYSTEM BOOT: app.py ORCHESTRATION FRAMEWORK")
    print("================================================================================")
    run_dashboard_api_pipeline()