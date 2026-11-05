"""
Isolated File Container: src/predictor.py
Baseline Profile: Intel i3 Architecture / 8 GB RAM / Python 3
Execution Mode: Low-Level, Deterministic, Line-by-Line Console Logging Engine
"""

import sys
from typing import Dict, List, Any, Optional
import requests

# -----------------------------------------------------------------------------
# 1. CORE PIPELINE DEPENDENCY & GLOBAL CONFIGURATION
# -----------------------------------------------------------------------------
HTTP_TIMEOUT: int = 10
TARGET_ENDPOINT_URL: str = "https://api.nasa.gov/neo/rest/v1/feed?api_key=DEMO_KEY"


# -----------------------------------------------------------------------------
# 2. TELEMETRY INGESTION SEQUENCE
# -----------------------------------------------------------------------------
def fetch_live_telemetry(endpoint_url: str = TARGET_ENDPOINT_URL) -> Optional[Dict[str, Any]]:
    """
    Establishes an explicit HTTP GET connection to NASA's NeoWs API endpoint,
    logs network telemetry, and returns the parsed JSON response dictionary.
    """
    print(f"[TELEMETRY_INGESTION] [INIT] Socket connection attempt to endpoint: {endpoint_url}")
    print(f"[TELEMETRY_INGESTION] [CONFIG] Hardcoded response timeout: {HTTP_TIMEOUT} seconds")

    try:
        response: requests.Response = requests.get(endpoint_url, timeout=HTTP_TIMEOUT)
        print(f"[TELEMETRY_INGESTION] [SOCKET_STATUS] Server HTTP response code: {response.status_code}")

        if response.status_code == 200:
            print("[TELEMETRY_INGESTION] [PARSING] HTTP 200 OK received. Directing text stream to JSON parser.")
            parsed_json: Dict[str, Any] = response.json()
            print(f"[TELEMETRY_INGESTION] [SUCCESS] Data buffer parsed into JSON dict structure. Top-level keys: {list(parsed_json.keys())}")
            return parsed_json
        else:
            print(f"[TELEMETRY_INGESTION] [FAILURE] Non-200 HTTP state returned: {response.status_code}. Aborting payload read.")
            return None

    except requests.exceptions.Timeout as timeout_err:
        print(f"[TELEMETRY_INGESTION] [EXCEPT_TIMEOUT] Network request exceeded limit ({HTTP_TIMEOUT}s): {timeout_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"[TELEMETRY_INGESTION] [EXCEPT_NETWORK] Socket error occurred during payload fetch: {req_err}")
        return None
    except Exception as general_err:
        print(f"[TELEMETRY_INGESTION] [EXCEPT_UNKNOWN] Unhandled extraction exception: {general_err}")
        return None


# -----------------------------------------------------------------------------
# 3. LOGIC ENGINE BOUNDARY EVALUATION
# -----------------------------------------------------------------------------
def evaluate_hazard_boundaries(estimated_diameter_max: Any, relative_velocity: Any) -> Dict[str, Any]:
    """
    Converts incoming telemetry metrics to floats, calculates tracking factor weights,
    and applies explicit hazard threshold conditions.
    """
    print(f"[HAZARD_EVAL] [ENTRY] Raw metrics -> estimated_diameter_max: {estimated_diameter_max}, relative_velocity: {relative_velocity}")

    # Explicit numerical float transformations
    try:
        val_diameter: float = float(estimated_diameter_max)
        print(f"[HAZARD_EVAL] [CAST] Cast diameter metric to float: {val_diameter}")
    except (ValueError, TypeError) as cast_err_d:
        print(f"[HAZARD_EVAL] [CAST_ERROR] Failed float conversion for diameter ({estimated_diameter_max}): {cast_err_d}. Defaulting to 0.0")
        val_diameter = 0.0

    try:
        val_velocity: float = float(relative_velocity)
        print(f"[HAZARD_EVAL] [CAST] Cast velocity metric to float: {val_velocity}")
    except (ValueError, TypeError) as cast_err_v:
        print(f"[HAZARD_EVAL] [CAST_ERROR] Failed float conversion for velocity ({relative_velocity}): {cast_err_v}. Defaulting to 0.0")
        val_velocity = 0.0

    # Computational Gravity Tracking Weights
    diameter_weight: float = val_diameter / 0.1
    velocity_weight: float = val_velocity / 80000.0

    print(f"[HAZARD_EVAL] [METRICS] Computed factor weights -> diameter_weight: {diameter_weight:.6f}, velocity_weight: {velocity_weight:.6f}")

    # Deterministic Boundary Evaluation Gates
    cond_diameter: bool = (val_diameter > 0.1)
    cond_velocity: bool = (val_velocity > 80000.0)

    print(f"[HAZARD_EVAL] [GATE] Evaluate Condition (diameter > 0.1): {cond_diameter} [{val_diameter} > 0.1]")
    print(f"[HAZARD_EVAL] [GATE] Evaluate Condition (velocity > 80000.0): {cond_velocity} [{val_velocity} > 80000.0]")

    if cond_diameter or cond_velocity:
        hazard_state: str = "CRITICAL HAZARD"
        print(f"[HAZARD_EVAL] [STATE] Logical condition met (OR match = True). Assigned state: '{hazard_state}'")
    else:
        hazard_state = "SAFE / LOW RISK"
        print(f"[HAZARD_EVAL] [STATE] Logical condition failed (OR match = False). Assigned state: '{hazard_state}'")

    return {
        "hazard_state": hazard_state,
        "diameter_weight": diameter_weight,
        "velocity_weight": velocity_weight
    }


# -----------------------------------------------------------------------------
# 4. DATA TRANSFORMATION MATRIX
# -----------------------------------------------------------------------------
def process_neo_data(raw_json_payload: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Traverses the JSON tree, extracts metric vectors per Near-Earth Object item,
    invokes boundary check gates, and packages structured records into a master list.
    """
    master_dashboard_array: List[Dict[str, Any]] = []

    print("[TRANSFORMATION_MATRIX] [INIT] Starting payload traversal...")

    if not raw_json_payload:
        print("[TRANSFORMATION_MATRIX] [ABORT] Provided raw_json_payload is empty or None. Returning empty array.")
        return master_dashboard_array

    # Validate base index root: near_earth_objects
    if "near_earth_objects" not in raw_json_payload:
        print("[TRANSFORMATION_MATRIX] [ABORT] Missing base root index 'near_earth_objects' in JSON structure.")
        return master_dashboard_array

    neo_dates_map: Dict[str, Any] = raw_json_payload["near_earth_objects"]
    print(f"[TRANSFORMATION_MATRIX] [ROOT_FOUND] Identified 'near_earth_objects' root key. Date partitions count: {len(neo_dates_map)}")

    item_counter: int = 0

    # Date bucket traversal loop
    for date_key, object_array in neo_dates_map.items():
        print(f"[TRANSFORMATION_MATRIX] [DATE_LOOP] Partition date: '{date_key}' | Object list count: {len(object_array)}")

        # Item array loop
        for index, item in enumerate(object_array):
            item_counter += 1
            print(f"[TRANSFORMATION_MATRIX] [ITEM_LOOP] [#{item_counter}] Processing date element at index [{index}]")

            try:
                # Metric 1 Extraction: name
                neo_name: str = str(item.get("name", "UNNAMED_OBJECT"))
                print(f"[TRANSFORMATION_MATRIX] [PULL_KEY] Metric 'name': '{neo_name}'")

                # Metric 2 Extraction: estimated_diameter_max (km)
                raw_diameter_max: float = 0.0
                if "estimated_diameter" in item and "kilometers" in item["estimated_diameter"]:
                    raw_diameter_max = item["estimated_diameter"]["kilometers"].get("estimated_diameter_max", 0.0)
                    print(f"[TRANSFORMATION_MATRIX] [PULL_KEY] Metric 'estimated_diameter_max' (km): {raw_diameter_max}")
                else:
                    print(f"[TRANSFORMATION_MATRIX] [WARN] 'estimated_diameter.kilometers' path missing at item index [{index}]. Defaulting to 0.0")

                # Metric 3 Extraction: relative_velocity (km/h)
                raw_velocity_kmh: float = 0.0
                if "close_approach_data" in item and isinstance(item["close_approach_data"], list) and len(item["close_approach_data"]) > 0:
                    first_approach: Dict[str, Any] = item["close_approach_data"][0]
                    if "relative_velocity" in first_approach:
                        raw_velocity_kmh = first_approach["relative_velocity"].get("kilometers_per_hour", 0.0)
                        print(f"[TRANSFORMATION_MATRIX] [PULL_KEY] Metric 'relative_velocity' (km/h): {raw_velocity_kmh}")
                    else:
                        print(f"[TRANSFORMATION_MATRIX] [WARN] Key 'relative_velocity' missing inside 'close_approach_data[0]'. Defaulting to 0.0")
                else:
                    print(f"[TRANSFORMATION_MATRIX] [WARN] Array 'close_approach_data' missing or empty at item index [{index}]. Defaulting to 0.0")

                # Evaluate Boundary Decision Gate
                eval_output: Dict[str, Any] = evaluate_hazard_boundaries(
                    estimated_diameter_max=raw_diameter_max,
                    relative_velocity=raw_velocity_kmh
                )

                # Structure Output Container for React Dashboard
                structured_record: Dict[str, Any] = {
                    "observation_date": date_key,
                    "name": neo_name,
                    "estimated_diameter_max_km": float(raw_diameter_max),
                    "relative_velocity_kmh": float(raw_velocity_kmh),
                    "hazard_state": eval_output["hazard_state"],
                    "diameter_weight": eval_output["diameter_weight"],
                    "velocity_weight": eval_output["velocity_weight"]
                }

                master_dashboard_array.append(structured_record)
                print(f"[TRANSFORMATION_MATRIX] [PACKAGED] Record successfully added to master list. Total elements: {len(master_dashboard_array)}")

            except KeyError as key_err:
                print(f"[TRANSFORMATION_MATRIX] [CATCH_KEY] Element index [{index}] raised missing key error: {key_err}. Bypassing item.")
                continue
            except Exception as item_err:
                print(f"[TRANSFORMATION_MATRIX] [CATCH_EXCEPT] Element index [{index}] unexpected processing fault: {item_err}. Bypassing item.")
                continue

    print(f"[TRANSFORMATION_MATRIX] [COMPLETE] Traversal finished. Processed {item_counter} total items into {len(master_dashboard_array)} dashboard dict records.")
    return master_dashboard_array


# -----------------------------------------------------------------------------
# ENGINE MAIN EXECUTION BLOCK
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("================================================================================")
    print("STARTING ENGINE EXECUTION: src/predictor.py")
    print("================================================================================")

    # Step 1: Ingestion
    telemetry_payload: Optional[Dict[str, Any]] = fetch_live_telemetry()

    # Step 2: Transformation & Boundary Evaluation
    dashboard_dataset: List[Dict[str, Any]] = process_neo_data(telemetry_payload)

    # Step 3: Terminal Summarisation
    print("================================================================================")
    print(f"PIPELINE COMPLETE: Generated {len(dashboard_dataset)} verified dashboard objects.")
    print("================================================================================")