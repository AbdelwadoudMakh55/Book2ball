import azure.functions as func
import json

bp_pitche_owners = func.Blueprint()
@bp_pitche_owners.route('pitch-owners', methods=['GET', 'POST'])
@bp_pitche_owners.generic_input_binding(arg_name="PitchOwners", type="sql", CommandText="SELECT * FROM dbo.PitchOwner",
                                        ConnectionStringSetting="SqlConnectionString")
def pitch_owner(req: func.HttpRequest, PitchOwners: func.SqlRowList) -> func.HttpResponse:
    method = req.method
    if method == 'GET':
        # Handle GET request
        return handle_get(req, PitchOwners)
    elif method == 'POST':
        # Handle POST request
        return handle_post(req)
    else:
        return func.HttpResponse(
            "Method not allowed",
            status_code=405
        )
    
def handle_get(req: func.HttpRequest, PitchOwners: func.SqlRowList) -> func.HttpResponse:
    # Logic for handling GET request
    # Retrieve pitch owners from database or any other data source
    pitch_owners = list(map(lambda r: json.loads(r.to_json()), PitchOwners))
    return func.HttpResponse(
        body=json.dumps(pitch_owners),
        mimetype="application/json",
        status_code=200
    )

def handle_post(req: func.HttpRequest) -> func.HttpResponse:
    # Logic for handling POST request
    # Parse the request body
    try:
        req_body = req.get_json()
        # Validate and process the request body
        # Save the new pitch owner to the database or any other data source
        new_pitch_owner = {"id": 4, "name": "Pitch Owner 4"}
        return func.HttpResponse(
            body=json.dumps(new_pitch_owner),
            mimetype="application/json",
            status_code=201
        )
    except ValueError:
        return func.HttpResponse(
            "Invalid request body",
            status_code=400
        )