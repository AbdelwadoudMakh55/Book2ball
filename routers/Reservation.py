import azure.functions as func
import json
from crud.reservation import *
from crud.pitch import *
from datetime import datetime

bp_reservations = func.Blueprint()
@bp_reservations.route('reservations', methods=['GET'])
def reservation(req: func.HttpRequest) -> func.HttpResponse:
    reservations = get_all_reservations()
    return func.HttpResponse(
        body=json.dumps(reservations),
        mimetype="application/json",
        status_code=200
    )

# TODO: Test this endpoint after adding pitches in the database
@bp_reservations.route('reservations/{pitch_id}', methods=['POST'])
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
        try:
            start_time = datetime.strptime(req_body['start_time'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return func.HttpResponse(
                "Invalid date format for start_time. Expected format: YYYY-MM-DD HH:MM:SS",
                status_code=400
            )
        reservation_start_time = get_reservation_by_start_time(pitch_id, req_body['start_time'])
        if reservation_start_time:
            return func.HttpResponse(
                "Reservation already exists for this start_time",
                status_code=400
            )
        if start_time < datetime.now():
            return func.HttpResponse(
                "Invalid start_time. It must be in the future",
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
        new_reservation = create_reservation_db(**req_body)
        return func.HttpResponse(
            body=json.dumps(new_reservation.to_dict()),
            mimetype="application/json",
            status_code=201
        )
    except ValueError as e:
        return func.HttpResponse(
            f"Invalid request body: {e}",
            status_code=400
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
    