"""
Master Entry Manager: backend/app.py
Execution Mode: Lightweight Live Flask API Server Endpoint
"""

import json
from flask import Flask, jsonify, Response
from flask_cors import CORS

# Inter-directory tracking operations import from custom logic module
from src.predictor import fetch_live_telemetry, process_neo_data


# -----------------------------------------------------------------------------
# WEB SERVER INITIALIZATION ROUTINE
# -----------------------------------------------------------------------------
app: Flask = Flask(__name__)
CORS(app)


# -----------------------------------------------------------------------------
# API ENDPOINT ROUTING TREE
# -----------------------------------------------------------------------------
@app.route('/api/telemetry', methods=['GET'])
def get_telemetry_data() -> Response:
    """
    HTTP GET route handler. Triggers the ingestion loop sequence, validates the payload, 
    processes the transformation matrix, and serializes the structured response array.
    """
    print("[API_ENDPOINT] [GET] Request received at pathway: /api/telemetry")
    
    try:
        # Trigger ingestion logic loop sequence
        print("[API_ENDPOINT] [INGESTION] Triggering telemetry fetch from upstream network.")
        raw_telemetry_matrix = fetch_live_telemetry()

        # Input Validation Gate Check
        if raw_telemetry_matrix is None:
            print("[API_ENDPOINT] [GATE_FAILED] Ingestion sequence returned None. Outputting failure state.")
            fallback_payload = {
                "status": "FAILURE",
                "venue_node": "JNNCE_SHIVAMOGGA_INDIA",
                "total_monitored_objects": 0,
                "payload_data": []
            }
            # Stream explicit error response cleanly
            return jsonify(fallback_payload), 502

        print("[API_ENDPOINT] [GATE_PASSED] Raw JSON matrix validated. Executing transformation engine loop.")
        
        # Traverse and compile tracking matrix array
        dashboard_dataset = process_neo_data(raw_telemetry_matrix)
        total_objects = len(dashboard_dataset)
        
        print(f"[API_ENDPOINT] [VERIFICATION] Transformation complete. Tracking array populated with {total_objects} items.")

        # Construct dashboard payload dictionary to exact layout specifications
        master_payload = {
            "status": "SUCCESS",
            "venue_node": "JNNCE_SHIVAMOGGA_INDIA",
            "total_monitored_objects": total_objects,
            "payload_data": dashboard_dataset
        }

        print("[API_ENDPOINT] [SERIALIZATION] Encoding payload dictionary via jsonify() and opening response socket.")
        return jsonify(master_payload), 200

    except Exception as runtime_error:
        print(f"[API_ENDPOINT] [EXCEPT_FAULT] Unhandled exception in routing tree: {runtime_error}")
        error_payload = {
            "status": "SERVER_FAULT",
            "venue_node": "JNNCE_SHIVAMOGGA_INDIA",
            "total_monitored_objects": 0,
            "error_details": str(runtime_error)
        }
        return jsonify(error_payload), 500


# -----------------------------------------------------------------------------
# ENGINE SYSTEM BOOT BLOCK
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("================================================================================")
    print("SYSTEM BOOT: backend/app.py FLASK SERVER NODE")
    print("ACTIVE ENDPOINT MAPPING PATH: http://0.0.0.0:8000/api/telemetry")
    print("================================================================================")
    
    # Launch server framework
    app.run(host='0.0.0.0', port=8000, debug=True)