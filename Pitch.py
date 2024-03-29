import azure.functions as func
import json

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
    

    