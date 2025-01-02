import azure.functions as func
import json
from crud.pitch import *
from crud.reservation import *
from crud.user import *
from services.firebase_config import firebase_auth
from services.reservation_verification_email import send_email_for_reservation_verification
from datetime import datetime, timedelta
from math import radians, cos, sin, sqrt, atan2


bp_pitches = func.Blueprint()

@bp_pitches.route('pitches', methods=['GET'], auth_level=func.AuthLevel.FUNCTION)
def pitches_by_location(req: func.HttpRequest) -> func.HttpResponse:
    auth_response = firebase_auth()(req)
    if isinstance(auth_response, func.HttpResponse):
        return auth_response
    
    try:
        latitude = float(req.params.get('lat'))
        longitude = float(req.params.get('long'))
    except (TypeError, ValueError):
        return func.HttpResponse(
            "Invalid latitude or longitude",
            status_code=400
        )

    pitches = get_all_pitches()
    closest_pitches = sorted(pitches, key=lambda pitch: distance(latitude, longitude, pitch['latitude'], pitch['longitude']))

    return func.HttpResponse(
        body=json.dumps(closest_pitches),
        mimetype="application/json",
        status_code=200
    )

def distance(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate the distance between two points on the Earth
    R = 6371.0  # Earth radius in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


@bp_pitches.route('pitches/{pitch_id?}', methods=['GET'], auth_level=func.AuthLevel.FUNCTION)
def pitch(req: func.HttpRequest) -> func.HttpResponse:
    auth_response = firebase_auth()(req)
    if isinstance(auth_response, func.HttpResponse):
        return auth_response

    pitch_id = req.route_params.get('pitch_id')
    if not pitch_id:
        return func.HttpResponse(
            body=json.dumps(get_all_pitches()),
            mimetype="application/json",
            status_code=200
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


@bp_pitches.route('pitches/{pitch_id}/reservations/{reservation_id?}', methods=['GET'], auth_level=func.AuthLevel.FUNCTION)
def reservations_by_pitch_id(req: func.HttpRequest) -> func.HttpResponse:
    auth_response = firebase_auth()(req)
    if isinstance(auth_response, func.HttpResponse):
        return auth_response

    pitch_id = req.route_params.get('pitch_id')
    pitch = get_pitch_by_id(pitch_id)
    if not pitch:
        return func.HttpResponse(
            "Pitch not found",
            status_code=404
        )
    reservation_id = req.route_params.get('reservation_id')
    if not reservation_id:
        reservations = [res.to_dict() for res in get_reservations_by_pitch_id(pitch_id)]
        return func.HttpResponse(
            body=json.dumps(reservations),
            mimetype="application/json",
            status_code=200
        )
    reservation = get_reservation_by_id(reservation_id)
    if not reservation:
        return func.HttpResponse(
            "Reservation not found",
            status_code=404
        )
    return func.HttpResponse(
        body=json.dumps(reservation.to_dict()),
        mimetype="application/json",
        status_code=200
    )
    
@bp_pitches.route('pitches/{pitch_id}/reservations', methods=['POST'], auth_level=func.AuthLevel.FUNCTION)
def create_reservation(req: func.HttpRequest) -> func.HttpResponse:
    auth_response = firebase_auth()(req)
    if isinstance(auth_response, func.HttpResponse):
        return auth_response

    pitch_id = req.route_params.get('pitch_id')
    pitch = get_pitch_by_id(pitch_id)
    if not pitch:
        return func.HttpResponse(
            "Pitch not found",
            status_code=404
        )
    try:
        req_body = req.get_json()
        if 'user_id' not in req_body:
            return func.HttpResponse(
                "Missing required field: user_id",
                status_code=400
            )
        if 'start_time' not in req_body:
            return func.HttpResponse(
                "Missing required field: start_time",
                status_code=400
            )
        start_time_str = req_body['start_time']
        user = get_user_by_id(req_body['user_id'])
        try:
            start_time = datetime.strptime(req_body['start_time'], '%Y-%m-%d %H:00:00')
        except ValueError:
            return func.HttpResponse(
                "Invalid date format for start_time. Expected format: YYYY-MM-DD HH:00:00",
                status_code=400
            )
        reservation_start_time = get_reservation_by_start_time(pitch_id, req_body['start_time'])
        if reservation_start_time:
            return func.HttpResponse(
                "Reservation already exists for this start_time",
                status_code=400
            )
        if start_time < datetime.now() + timedelta(hours=1):
            return func.HttpResponse(
                "Invalid start_time. It must be in the future at earliest 1 hour from now",
                status_code=400
            )
        pitch_reservations = get_reservations_by_pitch_id(pitch_id)
        res_day = [
            res for res in pitch_reservations
            if res.start_time.date() == start_time.date()
        ]
        if len(res_day) == 17:
            return func.HttpResponse(
                "Pitch is fully booked for this day",
                status_code=400
            )
        req_body['pitch_id'] = pitch_id
        req_body['start_time'] = start_time
        try:
            new_reservation = create_reservation_db(**req_body)
            result = send_email_for_reservation_verification(user, pitch.name, start_time_str, new_reservation.id)
            return func.HttpResponse(
                body=json.dumps(new_reservation.to_dict()),
                mimetype="application/json",
                status_code=201
            )
        except Exception as e:
            return func.HttpResponse(
                f"Failed to create reservation: {e}",
                status_code=500
            )
    except ValueError as e:
        return func.HttpResponse(
            f"Invalid request body: {e}",
            status_code=400
        )