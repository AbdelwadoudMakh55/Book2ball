import azure.functions as func
import json

bp_pitch_owners = func.Blueprint()
@bp_pitch_owners.route('pitch-owners', methods=['GET', 'POST'])
@bp_pitch_owners.generic_input_binding(arg_name="PitchOwners", type="sql", CommandText="SELECT * FROM dbo.PitchOwner",
                                        ConnectionStringSetting="SqlConnectionString")
@bp_pitch_owners.generic_output_binding(arg_name="PitchOwnersPost", type="sql", CommandText="dbo.PitchOwner",
                                        ConnectionStringSetting="SqlConnectionString")
def pitch_owner(req: func.HttpRequest, PitchOwners: func.SqlRowList, PitchOwnersPost: func.Out[func.SqlRow]) -> func.HttpResponse:
    method = req.method
    if method == 'GET':
        # Handle GET request
        return handle_get(req, PitchOwners)
    elif method == 'POST':
        # Handle POST request
        return handle_post(req, PitchOwnersPost)
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

def handle_post(req: func.HttpRequest, PitchOwnersPost: func.Out[func.SqlRow]) -> func.HttpResponse:
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
        if 'Email' not in req_body:
            return func.HttpResponse(
                "Missing required field: Email",
                status_code=400
            )
        if 'Phone' not in req_body:
            return func.HttpResponse(
                "Missing required field: Phone",
                status_code=400
            )
        if 'Address' not in req_body:
            return func.HttpResponse(
                "Missing required field: Address",
                status_code=400
            )
        # Save the new pitch owner to the database
        new_pitch_owner = PitchOwnersPost.set(func.SqlRow(req_body))    
        return func.HttpResponse(
            body=json.dumps(req_body),
            mimetype="application/json",
            status_code=201
        )
    except ValueError:
        return func.HttpResponse(
            "Invalid request body",
            status_code=400
        )