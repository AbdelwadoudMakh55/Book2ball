import azure.functions as func
import json
from crud.pitch import *
from crud.reservation import *


bp_pitches = func.Blueprint()


@bp_pitches.route('pitches', methods=['GET'])
def pitch(req: func.HttpRequest) -> func.HttpResponse:
    # Handle GET request
    pitches = get_all_pitches()
    return func.HttpResponse(
        body=json.dumps(pitches),
        mimetype="application/json",
        status_code=200
    )
    
@bp_pitches.route('pitches/{pitch_id}', methods=['GET'])
def pitch_by_id(req: func.HttpRequest) -> func.HttpResponse:
    pitch_id = req.route_params.get('pitch_id')
    pitch = get_pitch_by_id(pitch_id)
    if not pitch:
        return func.HttpResponse(
            "Pitch not found",
            status_code=404
        )
    # Handle GET request
    return func.HttpResponse(
        body=json.dumps(pitch.to_dict()),
        mimetype="application/json",
        status_code=200
    )

@bp_pitches.route('pitches/{pitch_id}/reservations', methods=['GET'])
def reservations_by_pitch_id(req: func.HttpRequest) -> func.HttpResponse:
    pitch_id = req.route_params.get('pitch_id')
    pitch = get_pitch_by_id(pitch_id)
    if not pitch:
        return func.HttpResponse(
            "Pitch not found",
            status_code=404
        )
    reservations = pitch.reservations
    return func.HttpResponse(
        body=json.dumps(reservations),
        mimetype="application/json",
        status_code=200
    )

@bp_pitches.route('pitches/{pitch_id}/reservations', methods=['POST'])
def create_reservation(req: func.HttpRequest) -> func.HttpResponse:
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
        if 'status' not in req_body:
            return func.HttpResponse(
                "Missing required field: status",
                status_code=400
            )
        req_body['pitch_id'] = pitch_id
        new_reservation = create_reservation(req_body)
        return func.HttpResponse(
            body=json.dumps(new_reservation.to_dict()),
            mimetype="application/json",
            status_code=201
        )
    except ValueError:
        return func.HttpResponse(
            "Invalid request body",
            status_code=400
        )

@bp_pitches.route('pitches/{pitch_id}/reservations/{reservation_id}', methods=['GET'])
def reservation_by_pitch_id(req: func.HttpRequest) -> func.HttpResponse:
    pitch_id = req.route_params.get('pitch_id')
    reservation_id = req.route_params.get('reservation_id')
    pitch = get_pitch_by_id(pitch_id)
    if not pitch:
        return func.HttpResponse(
            "Pitch not found",
            status_code=404
        )
    reservation = get_reservation_by_id(reservation_id)
    if not reservation.pitch_id == pitch_id:
        return func.HttpResponse(
            "Reservation not found",
            status_code=404
        )
    return func.HttpResponse(
        body=json.dumps(reservation.to_dict()),
        mimetype="application/json",
        status_code=200
    )