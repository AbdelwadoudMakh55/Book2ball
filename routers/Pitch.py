import azure.functions as func
import json
from crud.pitch import *
from crud.reservation import *
from services.firebase_config import firebase_auth


bp_pitches = func.Blueprint()


@bp_pitches.route('pitches', methods=['GET'])
@firebase_auth
def pitch(req: func.HttpRequest) -> func.HttpResponse:
    # Handle GET request
    pitches = get_all_pitches()
    return func.HttpResponse(
        body=json.dumps(pitches),
        mimetype="application/json",
        status_code=200
    )
    
@bp_pitches.route('pitches/{pitch_id}', methods=['GET'])
@firebase_auth
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
@firebase_auth
def reservations_by_pitch_id(req: func.HttpRequest) -> func.HttpResponse:
    pitch_id = req.route_params.get('pitch_id')
    pitch = get_pitch_by_id(pitch_id)
    if not pitch:
        return func.HttpResponse(
            "Pitch not found",
            status_code=404
        )
    reservations = get_reservations_by_pitch_id(pitch_id)
    return func.HttpResponse(
        body=json.dumps(reservations),
        mimetype="application/json",
        status_code=200
    )


@bp_pitches.route('pitches/{pitch_id}/reservations/{reservation_id}', methods=['GET'])
@firebase_auth
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