import azure.functions as func
import json
from models import storage
from models.pitch_owner import PitchOwner
from models.city import City
from models.pitch import Pitch

bp_pitch_owners = func.Blueprint()
@bp_pitch_owners.route('pitch-owners', methods=['GET', 'POST'])
def pitch_owner(req: func.HttpRequest) -> func.HttpResponse:
    method = req.method
    if method == 'GET':
        # Handle GET request
        pitch_owners = storage.all(PitchOwner).values()
        pitch_owners = [pitch_owner.to_dict() for pitch_owner in pitch_owners]
        return func.HttpResponse(
            body=json.dumps(pitch_owners),
            mimetype="application/json",
            status_code=200
        )
    elif method == 'POST':
        # Handle POST request
        return handle_post(req)


def handle_post(req: func.HttpRequest) -> func.HttpResponse:
    # Logic for handling POST request
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
        if 'address' not in req_body:
            return func.HttpResponse(
                "Missing required field: address",
                status_code=400
            )
        if 'city_id' not in req_body:
            return func.HttpResponse(
                "Missing required field: city_id",
                status_code=400
            )
        city = storage.get(City, req_body['city_id'])
        if not city:
            return func.HttpResponse(
                "City not found",
                status_code=404
            )
        # Save the new pitch owner to the database
        new_pitch_owner = PitchOwner(**req_body)
        new_pitch_owner.save()    
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
    
@bp_pitch_owners.route('pitch-owners/{pitch_owner_id}', methods=['GET', 'DELETE'])
def pitch_owner_by_id(req: func.HttpRequest) -> func.HttpResponse:
    method = req.method
    pitch_owner_id = req.route_params.get('pitch_owner_id')
    pitch_owner = storage.get(PitchOwner, pitch_owner_id)
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
        storage.delete(pitch_owner)
        storage.save()
        return func.HttpResponse(
            "Pitch owner deleted successfully",
            status_code=200
        )
    
@bp_pitch_owners.route('pitch-owners/{pitch_owner_id}/pitches', methods=['GET'])
def pitches_by_pitch_owner_id(req: func.HttpRequest) -> func.HttpResponse:
    pitch_owner_id = req.route_params.get('pitch_owner_id')
    pitch_owner = storage.get(PitchOwner, pitch_owner_id)
    if not pitch_owner:
        return func.HttpResponse(
            "Pitch owner not found",
            status_code=404
        )
    list_pitches = []
    for pitch in pitch_owner.pitches:
        list_pitches.append(pitch.to_dict())
    return func.HttpResponse(
        body=json.dumps(list_pitches),
        mimetype="application/json",
        status_code=200
    )

@bp_pitch_owners.route('pitch-owners/{pitch_owner_id}/pitches', methods=['POST'])
def create_pitch(req: func.HttpRequest) -> func.HttpResponse:
    pitch_owner_id = req.route_params.get('pitch_owner_id')
    pitch_owner = storage.get(PitchOwner, pitch_owner_id)
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
        if 'type' not in req_body:
            return func.HttpResponse(
                "Missing required field: Type",
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
        city = storage.get(City, req_body['city_id'])
        if not city:
            return func.HttpResponse(
                "City not found",
                status_code=404
            )
        # Save the new pitch to the database
        req_body['pitchOwner_id'] = pitch_owner_id
        new_pitch = Pitch(**req_body)
        new_pitch.save()
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
def pitch_by_pitch_owner_id(req: func.HttpRequest) -> func.HttpResponse:
    pitch_owner_id = req.route_params.get('pitch_owner_id')
    pitch_id = req.route_params.get('pitch_id')
    pitch_owner = storage.get(PitchOwner, pitch_owner_id)
    if not pitch_owner:
        return func.HttpResponse(
            "Pitch owner not found",
            status_code=404
        )
    for pitch in pitch_owner.pitches:
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
    