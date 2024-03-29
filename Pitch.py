import azure.functions as func
import json
import os
import pyodbc

bp_pitches = func.Blueprint()
@bp_pitches.route('pitches', methods=['GET', 'POST'])
@bp_pitches.generic_input_binding(arg_name="Pitches", type="sql", CommandText="SELECT * FROM dbo.Pitch",
                                  ConnectionStringSetting="SqlConnectionString")
@bp_pitches.generic_output_binding(arg_name="PitchesPost", type="sql", CommandText="dbo.Pitch",
                                   ConnectionStringSetting="SqlConnectionString")
@bp_pitches.generic_input_binding(arg_name="PitchOwners", type="sql", CommandText="SELECT * FROM dbo.PitchOwner",
                                  ConnectionStringSetting="SqlConnectionString")
@bp_pitches.generic_input_binding(arg_name="Cities", type="sql", CommandText="SELECT * FROM dbo.City",
                                  ConnectionStringSetting="SqlConnectionString")
def pitch(req: func.HttpRequest, Pitches: func.SqlRowList, PitchesPost: func.Out[func.SqlRow], PitchOwners: func.SqlRowList, Cities: func.SqlRowList) -> func.HttpResponse:
    method = req.method
    if method == 'GET':
        # Handle GET request
        return handle_get(Pitches)
    elif method == 'POST':
        # Handle POST request
        return handle_post(req, PitchesPost, PitchOwners, Cities)
    else:
        return func.HttpResponse(
            "Method not allowed",
            status_code=405
        )

def handle_get(Pitches: func.SqlRowList) -> func.HttpResponse:
    # Logic for handling GET request
    # Retrieve pitches from database
    pitches = list(map(lambda r: json.loads(r.to_json()), Pitches))
    return func.HttpResponse(
        body=json.dumps(pitches),
        mimetype="application/json",
        status_code=200
    )

def handle_post(req: func.HttpRequest, PitchesPost: func.Out[func.SqlRow], PitchOwners: func.SqlRowList, Cities: func.SqlRowList) -> func.HttpResponse:
    # Logic for handling POST request
    # Parse the request body
    try:
        req_body = req.get_json()
        # Validate and process the request body
        if 'Name' not in req_body:
            return func.HttpResponse(
                "Missing required field: Name",
                status_code=400
            )
        if 'Location' not in req_body:
            return func.HttpResponse(
                "Missing required field: Location",
                status_code=400
            )
        if 'Type' not in req_body:
            return func.HttpResponse(
                "Missing required field: Type",
                status_code=400
            )
        if 'Capacity' not in req_body:
            return func.HttpResponse(
                "Missing required field: Capacity",
                status_code=400
            )
        if 'Availability' not in req_body:
            return func.HttpResponse(
                "Missing required field: Availability",
                status_code=400
            )
        if 'PitchOwnerID' not in req_body:
            return func.HttpResponse(
                "Missing required field: PitchOwnerID",
                status_code=400
            )
        if 'CityID' not in req_body:
            return func.HttpResponse(
                "Missing required field: CityID",
                status_code=400
            )
        if not any(pitch_owner['PitchOwnerID'] == req_body['PitchOwnerID'] for pitch_owner in PitchOwners):
            return func.HttpResponse(
                "Invalid PitchOwnerID",
                status_code=400
            )
        if not any(city['CityID'] == req_body['CityID'] for city in Cities):
            return func.HttpResponse(
                "Invalid CityID",
                status_code=400
            ) 
        # Save the new pitch to the database
        new_pitch = PitchesPost.set(func.SqlRow(req_body))
        return func.HttpResponse(
            body=json.dumps(req_body),
            mimetype="application/json",
            status_code=201
        )
    except ValueError as e:
        return func.HttpResponse(
            f"Invalid request body",
            status_code=400
        )
    
@bp_pitches.route('pitches/{pitch_id}', methods=['GET', 'PUT', 'DELETE'])
@bp_pitches.generic_input_binding(arg_name="Pitches", type="sql", CommandText="SELECT * FROM dbo.Pitch",
                                  ConnectionStringSetting="SqlConnectionString")
def pitch_by_id(req: func.HttpRequest, Pitches: func.SqlRowList) -> func.HttpResponse:
    method = req.method
    pitch_id = req.route_params.get('pitch_id')
    pitches = list(map(lambda r: json.loads(r.to_json()), Pitches))
    pitch = list(pitch for pitch in pitches if pitch['PitchID'] == pitch_id)
    if len(pitch) == 0:
        return func.HttpResponse(
            "Pitch not found",
            status_code=404
        )
    conn_str = os.getenv("ODBCConnectionString")
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    if method == 'GET':
        # Handle GET request
        return func.HttpResponse(
            body=json.dumps(pitch),
            mimetype="application/json",
            status_code=200
        )
    elif method == 'PUT':
        # Handle PUT request
        return handle_put(req, pitch_id, Pitches, conn)
    elif method == 'DELETE':
        # Handle DELETE request
        return handle_delete(pitch_id, Pitches, conn)
    else:
        return func.HttpResponse(
            "Method not allowed",
            status_code=405
        )


def handle_put(req: func.HttpRequest, pitch_id: str, Pitches: func.SqlRowList, connection) -> func.HttpResponse:
    req_body = req.get_json()
    cursor = connection.cursor()


def handle_delete(pitch_id: str, Pitches: func.SqlRowList, connection) -> func.HttpResponse:
    cursor = connection.cursor()
    cursor.execute("DELETE FROM dbo.Pitch WHERE PitchID = ?", pitch_id)
    connection.commit()
    return func.HttpResponse(
        "Pitch deleted successfully",
        status_code=200
    )
    

    