import azure.functions as func
import json
from crud.reservation import *
from crud.pitch import *
from crud.user import *
from services.firebase_config import firebase_auth


bp_reservations = func.Blueprint()
@bp_reservations.route('reservations', methods=['GET'])
def reservation(req: func.HttpRequest) -> func.HttpResponse:
    reservations = get_all_reservations()
    return func.HttpResponse(
        body=json.dumps(reservations),
        mimetype="application/json",
        status_code=200
    )
    
@bp_reservations.route('reservations/{pitch_id}/{date}')
def reservations_today(req: func.HttpRequest) -> func.HttpResponse:
    pitch_id = req.route_params.get('pitch_id')
    date = req.route_params.get('date')
    pitch = get_pitch_by_id(pitch_id)
    if not pitch:
        return func.HttpResponse(
            "Pitch not found",
            status_code=404
        )
    reservations = get_reservations_by_pitch_id(pitch_id, date)
    return func.HttpResponse(
        body=json.dumps([res.to_dict() for res in reservations]),
        mimetype="application/json",
        status_code=200
    )


@bp_reservations.route('reservations/{reservation_id}', methods=['GET'])
def reservation_by_id(req: func.HttpRequest) -> func.HttpResponse:
    reservation_id = req.route_params.get('reservation_id')
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