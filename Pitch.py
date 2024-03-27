import azure.functions as func
import json

bp_pitches = func.Blueprint()
@bp_pitches.route('pitches', methods=['GET', 'POST'])
@bp_pitches.generic_input_binding(arg_name="Pitches", type="sql", CommandText="SELECT * FROM dbo.Pitch",
                                  ConnectionStringSetting="SqlConnectionString")
def pitch(req: func.HttpRequest, Pitches: func.SqlRowList) -> func.HttpResponse:
    method = req.method
    if method == 'GET':
        # Handle GET request
        return handle_get(req, Pitches)
    elif method == 'POST':
        # Handle POST request
        return handle_post(req)
    else:
        return func.HttpResponse(
            "Method not allowed",
            status_code=405
        )

def handle_get(req: func.HttpRequest, Pitches: func.SqlRowList) -> func.HttpResponse:
    # Logic for handling GET request
    # Retrieve pitches from database or any other data source
    pitches = list(map(lambda r: json.loads(r.to_json()), Pitches))
    return func.HttpResponse(
        body=json.dumps(pitches),
        mimetype="application/json",
        status_code=200
    )

def handle_post(req: func.HttpRequest) -> func.HttpResponse:
    # Logic for handling POST request
    # Parse the request body
    try:
        req_body = req.get_json()
        # Validate and process the request body
        # Save the new pitch to the database or any other data source
        new_pitch = {"id": 4, "name": "Pitch 4"}
        return func.HttpResponse(
            body=json.dumps(new_pitch),
            mimetype="application/json",
            status_code=201
        )
    except ValueError:
        return func.HttpResponse(
            "Invalid request body",
            status_code=400
        )