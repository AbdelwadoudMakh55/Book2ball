import azure.functions as func
import json
from crud.city import *
from crud.pitch import *
from crud.user import *
from crud.pitch_owner import *
from auth.firebase_config import firebase_auth

bp_cities = func.Blueprint()

@bp_cities.route('cities', methods=['GET', 'POST'])
@firebase_auth
def city(req: func.HttpRequest) -> func.HttpResponse:
    method = req.method
    if method == 'GET':
        cities = get_all_cities()
        return func.HttpResponse(
            body=json.dumps(cities),
            mimetype="application/json",
            status_code=200
        )
    elif method == 'POST':
        return handle_post(req)

def handle_post(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        # Validate and process the request body
        if 'name' not in req_body:
            return func.HttpResponse(
                "Missing required field: name",
                status_code=400
            )
        # Insert the city into the database
        new_city = create_city(**req_body)
        return func.HttpResponse(
            body=json.dumps(new_city.to_dict()),
            mimetype="application/json",
            status_code=201
        )
    except ValueError:
        return func.HttpResponse(
            "Invalid request body",
            status_code=400
        )
    
@bp_cities.route('cities/{city_id}', methods=['GET', 'DELETE', 'PUT'])
def city_by_id(req: func.HttpRequest) -> func.HttpResponse:
    method = req.method
    city_id = req.route_params.get('city_id')
    city = get_city_by_id(city_id)
    if not city:
        return func.HttpResponse(
            "City not found",
            status_code=404
        )
    if method == 'GET':
        return func.HttpResponse(
            body=json.dumps(city.to_dict()),
            mimetype="application/json",
            status_code=200
        )
    elif method == 'DELETE':
        delete_city(city_id)
        return func.HttpResponse(
            "City deleted successfully",
            status_code=200
        )
    elif method == 'PUT':
        return handle_put(city_id, req)

def handle_put(city_id, req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        # Validate and process the request body
        if 'name'  not in req_body:
            return func.HttpResponse(
                "Missing required field: name",
                status_code=400
            )
        # Update the city in the database
        updated_city = update_city(city_id, **req_body)
        return func.HttpResponse(
            body=json.dumps(updated_city.to_dict()),
            mimetype="application/json",
            status_code=200
        )
    except ValueError:
        return func.HttpResponse(
            "Invalid request body",
            status_code=400
        )
    
@bp_cities.route('cities/{city_id}/pitches', methods=['GET'])
def pitches_by_city_id(req: func.HttpRequest) -> func.HttpResponse:
    city_id = req.route_params.get('city_id')
    city = get_city_by_id(city_id)
    if not city:
        return func.HttpResponse(
            "City not found",
            status_code=404
        )
    pitches = get_pitches_by_city_id(city_id)
    return func.HttpResponse(
        body=json.dumps(pitches),
        mimetype="application/json",
        status_code=200
    )

# TODO: Test this route after adding pitches to the Database
@bp_cities.route('cities/{city_id}/pitches/{pitch_id}', methods=['GET'])
def pitch_by_city_id(req: func.HttpRequest) -> func.HttpResponse:
    city_id = req.route_params.get('city_id')
    pitch_id = req.route_params.get('pitch_id')
    city = get_city_by_id(city_id)
    if not city:
        return func.HttpResponse(
            "City not found",
            status_code=404
        )
    pitch = get_pitch_by_id(pitch_id)
    if not pitch:
        return func.HttpResponse(
            "Pitch not found",
            status_code=404
        )
    return func.HttpResponse(
        body=json.dumps(pitch.to_dict()),
        mimetype="application/json",
        status_code=200
    )

@bp_cities.route('cities/{city_id}/users', methods=['GET'])
def users_by_city_id(req: func.HttpRequest) -> func.HttpResponse:
    city_id = req.route_params.get('city_id')
    city = get_city_by_id(city_id)
    if not city:
        return func.HttpResponse(
            "City not found",
            status_code=404
        )
    users = get_users_by_city_id(city_id)
    return func.HttpResponse(
        body=json.dumps(users),
        mimetype="application/json",
        status_code=200
    )

# TODO: Test this route after adding users to the Database
@bp_cities.route('cities/{city_id}/users/{user_id}', methods=['GET'])
def user_by_city_id(req: func.HttpRequest) -> func.HttpResponse:
    city_id = req.route_params.get('city_id')
    user_id = req.route_params.get('user_id')
    city = get_city_by_id(city_id)
    if not city:
        return func.HttpResponse(
            "City not found",
            status_code=404
        )
    user = get_user_by_id(user_id)
    if not user.city_id == city_id:
        return func.HttpResponse(
            "User not found",
            status_code=404
        )
    return func.HttpResponse(
        body=json.dumps(user.to_dict()),
        mimetype="application/json",
        status_code=200
    )

@bp_cities.route('cities/{city_id}/pitch-owners', methods=['GET'])
def pitch_owners_by_city_id(req: func.HttpRequest) -> func.HttpResponse:
    city_id = req.route_params.get('city_id')
    city = get_city_by_id(city_id)
    if not city:
        return func.HttpResponse(
            "City not found",
            status_code=404
        )
    pitch_owners = get_pitch_owners_by_city_id(city_id)
    return func.HttpResponse(
        body=json.dumps(pitch_owners),
        mimetype="application/json",
        status_code=200
    )

# TODO: Test this route after adding pitch owners to the Database
@bp_cities.route('cities/{city_id}/pitch-owners/{pitch_owner_id}', methods=['GET'])
def pitch_owner_by_city_id(req: func.HttpRequest) -> func.HttpResponse:
    city_id = req.route_params.get('city_id')
    pitch_owner_id = req.route_params.get('pitch_owner_id')
    city = get_city_by_id(city_id)
    if not city:
        return func.HttpResponse(
            "City not found",
            status_code=404
        )
    pitch_owner = get_pitch_owner_by_id(pitch_owner_id)
    if not pitch_owner.city_id == city_id:
        return func.HttpResponse(
            "PitchOwner not found",
            status_code=404
        )
    return func.HttpResponse(
        body=json.dumps(pitch_owner.to_dict()),
        mimetype="application/json",
        status_code=200
    )