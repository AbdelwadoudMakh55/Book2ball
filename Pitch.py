import azure.functions as func
import json

bp_pitches = func.Blueprint()
@bp_pitches.route('pitches', methods=['GET', 'POST'])
@bp_pitches.generic_input_binding(arg_name="Pitches", type="sql", CommandText="SELECT * FROM dbo.Pitch",
                                  ConnectionStringSetting="SqlConnectionString")
@bp_pitches.generic_output_binding(arg_name="PitchesPost", type="sql", CommandText="dbo.Pitch",
                                   ConnectionStringSetting="SqlConnectionString")
def pitch(req: func.HttpRequest, Pitches: func.SqlRowList, PitchesPost: func.Out[func.SqlRow]) -> func.HttpResponse:
    method = req.method
    if method == 'GET':
        # Handle GET request
        return handle_get(req, Pitches)
    elif method == 'POST':
        # Handle POST request
        return handle_post(req, PitchesPost)
    else:
        return func.HttpResponse(
            "Method not allowed",
            status_code=405
        )

def handle_get(req: func.HttpRequest, Pitches: func.SqlRowList) -> func.HttpResponse:
    # Logic for handling GET request
    # Retrieve pitches from database
    pitches = list(map(lambda r: json.loads(r.to_json()), Pitches))
    return func.HttpResponse(
        body=json.dumps(pitches),
        mimetype="application/json",
        status_code=200
    )

def handle_post(req: func.HttpRequest, PitchesPost: func.Out[func.SqlRow]) -> func.HttpResponse:
    # Logic for handling POST request
    # Parse the request body
    try:
        req_body = req.get_json()
        # Validate and process the request body
        # Save the new pitch to the database
        new_pitch = PitchesPost.set(func.SqlRow(req_body))
        return func.HttpResponse(
            body=json.dumps(req_body),
            mimetype="application/json",
            status_code=201
        )
    except ValueError as e:
        return func.HttpResponse(
            f"Invalid request body: {e}",
            status_code=400
        )