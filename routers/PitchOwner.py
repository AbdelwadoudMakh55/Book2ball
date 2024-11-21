import azure.functions as func
import json
from crud.pitch_owner import *
from crud.city import *
from crud.pitch import *
from services.firebase_config import firebase_auth

bp_pitch_owners = func.Blueprint()

@bp_pitch_owners.route('pitch-owners', methods=['GET', 'POST'])
def pitch_owner(req: func.HttpRequest) -> func.HttpResponse:
    method = req.method
    if method == 'GET':
        # Handle GET request
        pitch_owners = get_all_pitch_owners()
        return func.HttpResponse(
            body=json.dumps(pitch_owners),
            mimetype="application/json",
            status_code=200
        )
    elif method == 'POST':
        # Handle POST request
        return handle_post(req)


def handle_post(req: func.HttpRequest) -> func.HttpResponse:
    # Parse the request body
    try:
        req_body = req.get_json()
        # Validate and process the request body
        if 'name' not in req_body:
            return func.HttpResponse(
                "Missing required field: name",
                status_code=400
            )
        if 'email' not in req_body:
            return func.HttpResponse(
                "Missing required field: email",
                status_code=400
            )
        if 'phone' not in req_body:
            return func.HttpResponse(
                "Missing required field: phone",
                status_code=400
            )
        if 'city_id' not in req_body:
            return func.HttpResponse(
                "Missing required field: city_id",
                status_code=400
            )
        city = get_city_by_id(req_body['city_id'])
        if not city:
            return func.HttpResponse(
                "City not found",
                status_code=404
            )
        # Save the new pitch owner to the database
        new_pitch_owner = create_pitch_owner(**req_body)
        return func.HttpResponse(
            body=json.dumps(new_pitch_owner.to_dict()),
            mimetype="application/json",
            status_code=201
        )
    except ValueError:
        return func.HttpResponse(
            "Invalid request body",
            status_code=400
        )
    
@bp_pitch_owners.route('pitch-owners/{pitch_owner_id}', methods=['GET', 'DELETE', 'PUT'])
@firebase_auth
def pitch_owner_by_id(req: func.HttpRequest) -> func.HttpResponse:
    method = req.method
    pitch_owner_id = req.route_params.get('pitch_owner_id')
    pitch_owner = get_pitch_owner_by_id(pitch_owner_id)
    if not pitch_owner:
        return func.HttpResponse(
            "Pitch owner not found",
            status_code=404
        )
    if method == 'GET':
        # Handle GET request
        return func.HttpResponse(
            body=json.dumps(pitch_owner.to_dict()),
            mimetype="application/json",
            status_code=200
        )
    elif method == 'DELETE':
        # Handle DELETE request
        delete_pitch_owner(pitch_owner_id)
        return func.HttpResponse(
            "Pitch owner deleted successfully",
            status_code=200
        )
    elif method == 'PUT':
        # Handle PUT request
        return handle_put(pitch_owner_id, req)
    
def handle_put(pitch_owner_id: str, req: func.HttpRequest) -> func.HttpResponse:
    # Parse the request body
    try:
        req_body = req.get_json()
        # Validate and process the request body
        if 'name' not in req_body:
            return func.HttpResponse(
                "Missing required field: name",
                status_code=400
            )
        if 'email' not in req_body:
            return func.HttpResponse(
                "Missing required field: email",
                status_code=400
            )
        if 'phone' not in req_body:
            return func.HttpResponse(
                "Missing required field: phone",
                status_code=400
            )
        if 'city_id' not in req_body:
            return func.HttpResponse(
                "Missing required field: city_id",
                status_code=400
            )
        city = get_city_by_id(req_body['city_id'])
        if not city:
            return func.HttpResponse(
                "City not found",
                status_code=404
            )
        # Update the pitch owner in the database
        updated_pitch_owner = update_pitch_owner(pitch_owner_id, **req_body)
        return func.HttpResponse(
            body=json.dumps(updated_pitch_owner.to_dict()),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            str(e),
            status_code=400
        )
    
@bp_pitch_owners.route('pitch-owners/{pitch_owner_id}/pitches', methods=['GET'])
@firebase_auth
def pitches_by_pitch_owner_id(req: func.HttpRequest) -> func.HttpResponse:
    pitch_owner_id = req.route_params.get('pitch_owner_id')
    pitch_owner = get_pitch_owner_by_id(pitch_owner_id)
    if not pitch_owner:
        return func.HttpResponse(
            "Pitch owner not found",
            status_code=404
        )
    pitches = get_pitches_by_pitch_owner_id(pitch_owner_id)
    return func.HttpResponse(
        body=json.dumps(pitches),
        mimetype="application/json",
        status_code=200
    )

# TODO: Implement logic for posting Pitch to the database and saving the images in Blob Storage
@bp_pitch_owners.route('pitch-owners/{pitch_owner_id}/pitches', methods=['POST'])
@firebase_auth
def create_pitch(req: func.HttpRequest) -> func.HttpResponse:
    pitch_owner_id = req.route_params.get('pitch_owner_id')
    pitch_owner = pitch_owner_by_id(pitch_owner_id)
    if not pitch_owner:
        return func.HttpResponse(
            "Pitch owner not found",
            status_code=404
        )
    # Logic for handling POST request
    # Parse the request body
    try:
        req_body = req.get_json()
        # Validate and process the request body
        if 'name' not in req_body:
            return func.HttpResponse(
                "Missing required field: Name",
                status_code=400
            )
        if 'location' not in req_body:
            return func.HttpResponse(
                "Missing required field: Location",
                status_code=400
            )
        if 'capacity' not in req_body:
            return func.HttpResponse(
                "Missing required field: Capacity",
                status_code=400
            )
        if 'availability' not in req_body:
            return func.HttpResponse(
                "Missing required field: Availability",
                status_code=400
            )
        if 'city_id' not in req_body:
            return func.HttpResponse(
                "Missing required field: city_id",
                status_code=400
            )
        req_body['pitchOwner_id'] = pitch_owner_id
        new_pitch = Pitch(**req_body)
        # Save the new pitch to the database
        new_pitch = create_pitch_db(new_pitch)
        return func.HttpResponse(
            body=json.dumps(new_pitch.to_dict()),
            mimetype="application/json",
            status_code=201
        )
    except ValueError as e:
        return func.HttpResponse(
            f"Invalid request body",
            status_code=400
        )

@bp_pitch_owners.route('pitch-owners/{pitch_owner_id}/pitches/{pitch_id}', methods=['GET'])
@firebase_auth
def pitch_by_pitch_owner_id(req: func.HttpRequest) -> func.HttpResponse:
    pitch_owner_id = req.route_params.get('pitch_owner_id')
    pitch_id = req.route_params.get('pitch_id')
    pitch_owner = get_pitch_owner_by_id(pitch_owner_id)
    if not pitch_owner:
        return func.HttpResponse(
            "Pitch owner not found",
            status_code=404
        )
    pitches = pitch_owner.pitches
    for pitch in pitches:
        if pitch.id == pitch_id:
            return func.HttpResponse(
                body=json.dumps(pitch.to_dict()),
                mimetype="application/json",
                status_code=200
            )
    return func.HttpResponse(
        "Pitch not found",
        status_code=404
    )