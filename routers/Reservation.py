import azure.functions as func
import json
from crud.reservation import *

bp_reservations = func.Blueprint()
@bp_reservations.route('reservations', methods=['GET'])
def reservation(req: func.HttpRequest) -> func.HttpResponse:
    reservations = get_all_reservations()
    reservations = [reservation.to_dict() for reservation in reservations]
    return func.HttpResponse(
        body=json.dumps(reservations),
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
    